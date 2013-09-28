#include "cells.h"
#include "png_utils.h"

#define LINE_LENGTH 100
#define ITERATIONS 100

int main(int argc, char *argv[])
{
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

	// pradedam
	int i;
	char* output;

	// paveikslelio matmenys - gaminam kvadratini
	int width = strlen(input);
	int height = ITERATIONS;

	s_png_file* png = create_png_file("output.png", width, height);
	if (png == -1)
	{
		printf("Nepavyko sukurti PNG failo\n");
		return -1;
	}

	for (i = 0; i < height; i++)
	{
//		printf("%s\n", input);
		write_line(input, png);

		char* output = malloc(strlen(input) * sizeof(char));
		process_all(input, output, rule);
		free(input);
		input = output;
	}
	free(input);

	finalize_png_file(png);
	printf("Rezultatas įrašytas į output.png\n");
}
