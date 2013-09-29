/*
 * cells.h
 *
 *  Created on: Sep 21, 2013
 *      Author: tomas
 */

#ifndef CELLS_H_
#define CELLS_H_

extern int input_valid(char *input);
extern char* get_random_input(int length);
extern char* get_input_from_file(char* filename);
extern void process_all(char *input, char *output, unsigned char rule);
extern void process_range(char *input, char *output, int start, int end, unsigned char rule);

#endif /* CELLS_H_ */
