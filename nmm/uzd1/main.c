#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cells.h"

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
	char rule = 90;
	char *input;
	input = read_input("input2.txt");

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
	for (i = 0; i < strlen(input); i++)
	{
		printf("%s\n", input);
		char* output = malloc(strlen(input) * sizeof(char));
		process_all(input, output, rule);
		free(input);
		input = output;
	}
	free(input);
}
