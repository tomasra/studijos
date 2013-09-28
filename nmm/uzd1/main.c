#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cells.h"
#include "png_utils.h"

// nuskaito pradine eilute
char* read_input(char* filename)
{
	FILE* file;
	file = fopen(filename, "r");
	if (file == NULL)
		return -1;
	else
	{
		// eilutes ilgis
		int length;
		fseek(file, 0L, SEEK_END);
		length = ftell(file);
		fseek(file, 0, SEEK_SET);

		// skaitymas
		char* data;
		int datalength = (length + 1) * sizeof(char);
		data = (char*)malloc(datalength);
		memset(data, 0, datalength);

		int i = 0;
		char ch = fgetc(file);
		while (ch != EOF)
		{
			data[i] = ch;
			i++;
			ch = fgetc(file);
		}
		fclose(file);
		return data;
	}
}

int main(int argc, char *argv[])
{
	// TODO - taisykle pasiimti is parametru?
	unsigned char rule = 110;
	char *input;
	//input = read_input("tests/input2.txt");
	input = get_random_input(100);

	if (input == -1)
	{
		printf("Nepavyko nuskaityti duomenu\n");
		return -1;
	}
	if (input_valid(input) != 0)
	{
		printf("Nekorektiski duomenys\n");
		return -1;
	}

	// pradedam
	int i;
	char* output;

	// paveikslelio matmenys - gaminam kvadratini
	int width = strlen(input);
	int height = strlen(input);

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
	printf("Baigta\n");
}
