/*
 * cells.h
 *
 *  Created on: Sep 21, 2013
 *      Author: tomas
 */

#ifndef CELLS_H_
#define CELLS_H_

int input_valid(char *input);
char* get_random_input(int length);
char* get_input_from_file(char* filename);
void process(char* input, char left, char right, int count, char* output, unsigned char rule);
void process_all(char *input, char *output, unsigned char rule);
void process_range(char *input, char *output, int start, int end, unsigned char rule);

#endif /* CELLS_H_ */
