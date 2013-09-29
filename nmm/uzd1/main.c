#include "cells.h"
#include "png_utils.h"
#include <mpi.h>
#include <time.h>

#define DEBUG 0

#define LINE_LENGTH 5000
#define ITERATIONS 5000

// komunikacijai tarp procesu
#define P_CALC_START 0
#define P_CALC_END 1

// algoritmo vykdymui reikalingi pradiniai duomenys
typedef struct
{
	char* input;
	unsigned char rule;
	s_png_file* png;
} s_args;

// argumentai lygiagretiems procesams
typedef struct
{
	int start;
	int length;
} cell_args;

/*
// nuoseklus vykdymas
void run_normal(char* input, s_png_file* png, unsigned char rule, int iterations)
{

}

// lygiagretus vykdymas
void run_parallel(char* input, s_png_file* png, unsigned char rule, int iterations,
		int argc, char* argv[], unsigned int cpu_count)
{
	int rank;
	int size;

	MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);
	printf("CPU %d of %d", rank, size);
	MPI_Finalize();
}
*/

// paruosiamieji veiksmai, bendri tiek nuosekliam, tiek lygiagreciam programos variantui
s_args* init(int argc, char* argv[])
{
	s_args* result = (s_args*)malloc(sizeof(s_args));

	char *input;
	unsigned char rule;

	if (argc == 2 || argc == 3)
	{
		int r = -1;
		sscanf(argv[1], "%d", &r);
		if (r >= 0 && r <= 255)
			rule = r;
		else
		{
			printf("taisyklė turi būti sveikas skaičius nuo 0 iki 255\n");
			return -1;
		}

		// naudojama atsitiktine eilute
		if (argc == 2)
			input = get_random_input(LINE_LENGTH);
		// pradine eilute skaitoma is nurodyto failo
		else
			input = get_input_from_file(argv[2]);
	}
	else
	{
		printf("Naudojimas: ./uzd1 taisyklė [failas]\n");
		return -1;
	}

	if (input == -1)
	{
		printf("Nepavyko nuskaityti duomenu\n");
		return -1;
	}
//	if (input_valid(input) != 0)
//	{
//		printf("Nekorektiski duomenys\n");
//		return -1;
//	}

	// paveikslelio matmenys - gaminam kvadratini
	s_png_file* png = create_png_file("output.png", strlen(input), ITERATIONS);
	if (png == -1)
	{
		printf("Nepavyko sukurti PNG failo\n");
		return -1;
	}

	result->input = input;
	result->rule = rule;
	result->png = png;
	return result;
}

int main_serial(int argc, char* argv[])
{
	s_args* args = init(argc, argv);
	if (args == -1)
		return -1;

	// pasikopijavimas pradines eilutes
	int input_length = sizeof(char) * strlen(args->input);
	char* input = (char*)malloc(input_length);
	memcpy(input, args->input, input_length);

	// vykdymas
	clock_t start = clock();

	int i;
	for (i = 0; i < ITERATIONS; i++)
	{
		write_line(input, args->png);
		char* output = malloc(strlen(input) * sizeof(char));
		process_all(input, output, args->rule);
		free(input);
		input = output;
	}
	free(input);
	finalize_png_file(args->png);

	clock_t end = clock();
	double total_time = (double)(end - start) / CLOCKS_PER_SEC;

	printf("Baigta per%5.2f sek.\n", total_time);
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

	// pagrindinio proceso darbas
	if (rank == root)
	{
		int i, w;
		s_args* args = init(argc, argv);
		if (args == -1)
			return -1;

		// pasikopijavimas pradines eilutes
		int input_length = sizeof(char) * strlen(args->input);
		char* input = (char*)calloc(input_length + 1, sizeof(char));
		memcpy(input, args->input, input_length);

		// vykdymas
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

//			printf("Worker %d: %d %d\n", worker_id, worker_args[i]->start, worker_args[i]->length);

			// pradzioje kiekvienam procesui pasiunciama taisykle
			// bei jo apdorojamu lasteliu skaicius
			MPI_Send(&(args->rule), 1, MPI_UNSIGNED_CHAR, worker_id, tag, MPI_COMM_WORLD);
			MPI_Send(&(worker_args[i]->length), 1, MPI_INT, worker_id, tag, MPI_COMM_WORLD);
		}

		for (i = 0; i < ITERATIONS; i++)
		{
			write_line(input, args->png);
			char* output = (char*)calloc(input_length + 1, sizeof(char));

			// duomenu paskirstymas procesams
			for (w = 0; w < worker_count; w++)
			{
				int worker_id = w + 1;

				// kairiosios ir desiniosios lasteles
				char left, right;

				// kairioji
				if (worker_args[w]->start == 0)
					left = input[input_length - 1];
				else
					left = input[worker_args[w]->start - 1];

				// desinioji
				if (worker_args[w]->start + worker_args[w]->length == input_length)
					right = input[0];
				else
					right = input[worker_args[w]->start + worker_args[w]->length];

				// duodam procesui veiklos!
				MPI_Send(input + worker_args[w]->start, worker_args[w]->length,	MPI_CHAR, worker_id, tag, MPI_COMM_WORLD);
				MPI_Send(&left, 1, MPI_CHAR, worker_id, tag, MPI_COMM_WORLD);
				MPI_Send(&right, 1, MPI_CHAR, worker_id, tag, MPI_COMM_WORLD);
			}

			// rezultatu surinkimas is procesu
			for (w = 0; w < worker_count; w++)
			{
				int worker_id = w + 1;
				MPI_Recv(output + worker_args[w]->start, worker_args[w]->length, MPI_CHAR, worker_id, tag, MPI_COMM_WORLD, &status);
			}

			free(input);
			input = output;
		}
		free(input);
		finalize_png_file(args->png);

		clock_t end = clock();
		double total_time = (double)(end - start) / CLOCKS_PER_SEC;

		printf("Baigta per%5.2f sek.\n", total_time);
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
		for (i = 0; i < ITERATIONS; i++)
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
