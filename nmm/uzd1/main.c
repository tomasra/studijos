#include <mpi.h>
#include <time.h>
#include "cells.h"
#include "png_utils.h"

#define DEBUG 0

// algoritmo vykdymui reikalingi pradiniai duomenys
typedef struct
{
	char* input;
	int length;
	int iterations;
	unsigned char rule;
	unsigned char export_to_png;	// 0/1
	char* output_file;
	s_png_file* png;
} s_args;

// argumentai lygiagretiems procesams
typedef struct
{
	int start;
	int length;
} cell_args;

// paruosiamieji veiksmai, bendri tiek nuosekliam, tiek lygiagreciam programos variantui
// pradiniu duomenu surinkimas, validacija ir t.t.
s_args* init(int argc, char* argv[])
{
	s_args* result = (s_args*)malloc(sizeof(s_args));
	if (argc >= 4 && argc <= 6)
	{
		int status;
		s_args* result = (s_args*)malloc(sizeof(s_args));

		// taisykle
		status = sscanf(argv[1], "%d", &(result->rule));
		if (status != 1 || result->rule < 0 || result->rule > 255)
		{
			printf("Taisyklė turi būti sveikas skaičius nuo 0 iki 255\n");
			return -1;
		}

		// eilutes_ilgis
		status = sscanf(argv[2], "%d", &(result->length));
		if (status != 1)
		{
			printf("Eilutės ilgis turi būti sveikas skaičius\n");
			return -1;
		}

		// iteraciju skaicius
		status = sscanf(argv[3], "%d", &(result->iterations));
		if (status != 1)
		{
			printf("Iteracijų kiekis turi būti sveikas skaičius\n");
			return -1;
		}

		// generuojama atsitiktine pradine eilute
		if (argc == 4 || argc == 5)
		{
			result->input = get_random_input(result->length);

			// rezultatai nebuna issaugomi png faile
			if (argc == 4)
			{
				result->export_to_png = 0;
				result->png = NULL;
			}
			// rezultatai issaugomi png faile
			else
			{
				result->export_to_png = 1;
				result->output_file = (char*)malloc(strlen(argv[4]) + 1);
				strcpy(result->output_file, argv[4]);
				result->png = create_png_file(argv[4], result->length, result->iterations);
				if (result->png == -1)
				{
					printf("Nepavyko sukurti nurodyto PNG failo rezultatams\n");
					return -1;
				}
			}

		}
		// pradine eilute imama is failo, rezultatai issaugomi png faile
		else
		{
			char* file_input = get_input_from_file(argv[5]);
			if (file_input != -1)
				result->input = file_input;
			else
			{
				printf("Nepavyko nuskaityti failo su pradine eilute\n");
				return -1;
			}
		}

		return result;
	}
	else
	{
		printf("Naudojimas: uzd1 taisyklė eilutės_ilgis iteracijų_skaičius [rezultatų png failas] [pradinės eilutės failas]");
		return -1;
	}
}

void finalize(s_args* init_args, char** results)
{
	// eksportavimas i png
	if (init_args->export_to_png == 1)
	{
		printf("Rezultatai rašomi į %s\n", init_args->output_file);
		write_file(results, init_args->iterations, init_args->png);
		finalize_png_file(init_args->png);
	}

	// atminties atlaisvinimas
	int i;
	for (i = 0; i < init_args->iterations; i++)
		free(results[i]);
	free(results);
}

int main_serial(int argc, char* argv[])
{
	s_args* args = init(argc, argv);
	if (args == -1)
		return -1;

	int i;

	// buferio paruosimas
//	int input_length = sizeof(char) * strlen(args->input);
	int input_length = sizeof(char) * args->length;
	char** buffer = (char**)calloc(sizeof(char*), args->iterations);
	for (i = 0; i < args->iterations; i++)
		buffer[i] = (char*)calloc(sizeof(char), input_length + 1);

	// pradine eilute
	memcpy(buffer[0], args->input, input_length);

	// vykdymo pradzia
	printf("Skaičiavimų pradžia\n");
	clock_t start = clock();

	for (i = 1; i < args->iterations; i++)
		process_all(buffer[i - 1], buffer[i], args->rule);

	// vykdymo pabaiga
	clock_t end = clock();
	double total_time = (double)(end - start) / CLOCKS_PER_SEC;
	printf("Skaičiavimai baigti per%5.2f sek.\n", total_time);

	// cleanup
	finalize(args, buffer);
	printf("Baigta\n");
}

int main_parallel(int argc, char* argv[])
{
	MPI_Status status;

	// pagrindinis procesas su 0-iniu rangu
	int root = 0;

	// pranesimu tipu nenaudojam?
	int tag = 0;

	// einamojo proceso numeris ir bendras procesu skaicius
	int rank, size;

	// inicializacija
	MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);

	// vykdymo parametrai
	s_args* args = init(argc, argv);
	if (args == -1)
		return -1;

	// pagrindinio proceso darbas
	if (rank == root)
	{
		int i, w;

		// buferio paruosimas
//		int input_length = sizeof(char) * strlen(args->input);
		int input_length = sizeof(char) * args->length;
		char** buffer = (char**)calloc(sizeof(char*), args->iterations);
		for (i = 0; i < args->iterations; i++)
			buffer[i] = (char*)calloc(sizeof(char), input_length + 1);

		// pradine eilute
		memcpy(buffer[0], args->input, input_length);

		// vykdymo pradzia
		clock_t start = clock();

		// argumentu paruosimas kitiems procesams
		int worker_count = size - 1;
		cell_args* worker_args[worker_count];

		for (i = 0; i < worker_count; i++)
		{
			// salutiniu procesu ID prasideda nuo 1
			int worker_id = i + 1;
			int chunk_length = input_length / worker_count;

			// nustatomi apdorojomos eilutes reziai kiekvienam procesui
			worker_args[i] = (cell_args*)malloc(sizeof(cell_args));
			worker_args[i]->start = i * chunk_length;

			if (i == worker_count - 1)
				// paskutinis pasiima visa likusia dali
				worker_args[i]->length = input_length - worker_args[i]->start;
			else
				worker_args[i]->length = chunk_length;

			if (DEBUG)
				printf("Worker params%d: %d %d\n", worker_id, worker_args[i]->start, worker_args[i]->length);

			// pradzioje kiekvienam procesui pasiunciama taisykle
			// bei jo apdorojamu lasteliu skaicius
			MPI_Send(&(args->rule), 1, MPI_UNSIGNED_CHAR, worker_id, tag, MPI_COMM_WORLD);
			MPI_Send(&(worker_args[i]->length), 1, MPI_INT, worker_id, tag, MPI_COMM_WORLD);
		}

		for (i = 1; i < args->iterations; i++)
		{
			// duomenu paskirstymas procesams
			for (w = 0; w < worker_count; w++)
			{
				int worker_id = w + 1;

				// kairiosios ir desiniosios lasteles
				char left, right;

				// kairioji
				if (worker_args[w]->start == 0)
					left = buffer[i - 1][input_length - 1];
				else
					left = buffer[i - 1][worker_args[w]->start - 1];

				// desinioji
				if (worker_args[w]->start + worker_args[w]->length == input_length)
					right = buffer[i - 1][0];
				else
					right = buffer[i - 1][worker_args[w]->start + worker_args[w]->length];

				// duodam procesui veiklos!
				MPI_Send(buffer[i - 1] + worker_args[w]->start, worker_args[w]->length, MPI_CHAR, worker_id, tag, MPI_COMM_WORLD);
				MPI_Send(&left, 1, MPI_CHAR, worker_id, tag, MPI_COMM_WORLD);
				MPI_Send(&right, 1, MPI_CHAR, worker_id, tag, MPI_COMM_WORLD);
			}

			// rezultatu surinkimas is procesu
			for (w = 0; w < worker_count; w++)
			{
				int worker_id = w + 1;
				MPI_Recv(buffer[i] + worker_args[w]->start, worker_args[w]->length, MPI_CHAR, worker_id, tag, MPI_COMM_WORLD, &status);
			}
		}

		// fiksuojam vykdymo pabaiga
		clock_t end = clock();
		double total_time = (double)(end - start) / CLOCKS_PER_SEC;
		printf("Skaičiavimai baigti per%5.2f sek.\n", total_time);

		// cleanup
		finalize(args, buffer);
		printf("Baigta\n");
	}
	// salutiniu procesu darbai
	else
	{
		unsigned char rule;
		int length;

		// taisykles ir apdorojamu eiluciu daliu ilgio gavimas
		MPI_Recv(&rule, 1, MPI_UNSIGNED_CHAR, root, tag, MPI_COMM_WORLD, &status);
		MPI_Recv(&length, 1, MPI_INT, root, tag, MPI_COMM_WORLD, &status);

		if (DEBUG)
			printf("Procesas %d inicializuotas su taisykle %d, ilgiu %d\n", rank, rule, length);

		char* input = (char*)calloc(length + 1, sizeof(char));
		char* output = (char*)calloc(length + 1, sizeof(char));

		// darbas
		int i;
		for (i = 1; i < args->iterations; i++)
		{
			// duomenu gavimas
			char left, right;
			MPI_Recv(input, length, MPI_CHAR, root, tag, MPI_COMM_WORLD, &status);
			MPI_Recv(&left, 1, MPI_CHAR, root, tag, MPI_COMM_WORLD, &status);
			MPI_Recv(&right, 1, MPI_CHAR, root, tag, MPI_COMM_WORLD, &status);

			if (DEBUG)
				printf("Procesas %d gavo veiklos iteracijai %d: %s, %c, %c\n", rank, i, input, left, right);

			// atliekami skaiciavimai ir rezultatas siunciamas root procesui
			process(input, left, right, length, output, rule);
			MPI_Send(output, length, MPI_CHAR, root, tag, MPI_COMM_WORLD);
		}
		free(input);
		free(output);
	}

	MPI_Finalize();
}

int main(int argc, char *argv[])
{
//	return main_serial(argc, argv);
	return main_parallel(argc, argv);
}
