/*
 * png_utils.h
 *
 *  Created on: Sep 21, 2013
 *      Author: tomas
 */

#ifndef PNG_UTILS_H_
#define PNG_UTILS_H_

#include <png.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// wrapperis patogesniam darbui su png failais
typedef struct
{
	FILE* file;
	png_structp png_ptr;
	png_infop png_info;
} s_png_file;

extern s_png_file* create_png_file(char* path, int width, int height);
extern void write_line(char* input, s_png_file* output);
extern void finalize_png_file(s_png_file* file);

#endif /* PNG_UTILS_H_ */
