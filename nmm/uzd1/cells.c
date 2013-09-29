/*
 * cells.c
 *
 *  Created on: Sep 21, 2013
 *      Author: tomas
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// sugeneruoja atsitiktine nurodyto ilgio eilute
char* get_random_input(int length)
{
	int i, c;
	char* data = (char*)calloc(length + 1, sizeof(char));
	srand(time(NULL));
	for (i = 0; i < length; i++)
	{
		c = rand() % 2;
		if (c == 0) data[i] = '0';
		if (c == 1) data[i] = '1';
	}
	return data;
}

// nuskaito pradine eilute is failo
char* get_input_from_file(char* filename)
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

// ar taisyklingas input'as
int input_valid(char *input)
{
	int i;
	int length = strlen(input);

	// per trumpas
	if (length < 3)
		return -1;

	// yra blogu simboliu
	for (i = 0; i < length; i++)
		if (input[i] != '1' && input[i] != '0')
			return -1;

	return 0;
}

// triju lasteliu grupes simbolius pavercia i 3 bitu skaiciu
unsigned char cells_to_bits(char cells[3])
{
	char result = 0;
	if (cells[0] == '1') result += 4;	// kaire lastele
	if (cells[1] == '1') result += 2;	// vidurine lastele
	if (cells[2] == '1') result += 1;	// desine lastele
	return result;
}

// pritaiko taisykle triju lasteliu grupei ir grazina rezultata
char process_cell(char cells[3], unsigned char rule)
{
	char bits = cells_to_bits(cells);
	// istraukiam reikiama bita is taisykles
	unsigned char result = (rule >> bits) % 2;
	if (result == 0)
		return '0';
	else if (result == 1)
		return '1';
	else
		return -1;
}

// input'as turi buti taisyklinga, bent jau triju simboliu ilgio null-terminated eilute
// output'as turi buti jau isskirta atminties dalis, tokio paties ilgio kaip input'as
// start/end numeravimas prasideda nuo nulio!
void process_range(char *input, char *output, int start, int end, unsigned char rule)
{
	int i;
	for (i = start; i <= end; i++)
	{
		// buferio pradzia - reikia kairiaja lastele imti is buferio galo
		if (i == 0)
		{
			// tenka suformuoti atskira masyva
			char cells[3];
			cells[0] = input[strlen(input) - 1];
			cells[1] = input[i];
			cells[2] = input[i + 1];
			output[i] = process_cell(cells, rule);
		}
		// buferio pabaiga - desine lastele imama is buferio pradzios
		else if (i == (strlen(input) - 1))
		{
			// irgi formuojamas atskiras masyvas
			char cells[3];
			cells[0] = input[i - 1];
			cells[1] = input[i];
			cells[2] = input[0];
			output[i] = process_cell(cells, rule);
		}
		// kitu atveju viskas ok
		else
		{
			// atitinkama buferio dalis
			char* cells = input + (i * sizeof(char)) - (1 * sizeof(char));
			output[i] = process_cell(cells, rule);
		}
	}
}

// tas pats kaip ir "process", tik visam buferiui
void process_all(char* input, char* output, unsigned char rule)
{
	process_range(input, output, 0, (strlen(input) - 1), rule);
}

void process(char* input, char left, char right, int count, char* output, unsigned char rule)
{
	int i;
	for (i = 0; i < count; i++)
	{
		// buferio pradzia - naudojama perduota kairioji lastele
		if (i == 0)
		{
			// tenka suformuoti atskira masyva
			char cells[3];
			cells[0] = left;
			cells[1] = input[i];
			cells[2] = input[i + 1];
			output[i] = process_cell(cells, rule);
		}
		// buferio pabaiga - naudojama perduota desinioji lastele
		else if (i == count - 1)
		{
			// irgi formuojamas atskiras masyvas
			char cells[3];
			cells[0] = input[i - 1];
			cells[1] = input[i];
			cells[2] = right;
			output[i] = process_cell(cells, rule);
		}
		// kitu atveju viskas ok
		else
		{
			// atitinkama buferio dalis
			char* cells = input + (i * sizeof(char)) - (1 * sizeof(char));
			output[i] = process_cell(cells, rule);
		}
	}
}
