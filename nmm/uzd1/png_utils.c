/*
 * png_utils.c
 *
 *  Created on: Sep 21, 2013
 *      Author: tomas
 */

// ideju pasisemta is: http://www.lemoda.net/c/write-png/
#include "png_utils.h"

// sukuria ir atidaro nauja png faila
s_png_file* create_png_file(char* path, int width, int height)
{
	s_png_file* result = (s_png_file*)malloc(sizeof(s_png_file));

	// fizinio failo sukurimas
	result->file = fopen(path, "wb");
	if (!(result->file))
		return -1;

	// magic ahead
	result->png_ptr = png_create_write_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
	if (result->png_ptr == NULL)
		return -1;

	result->png_info = png_create_info_struct(result->png_ptr);
	if (result->png_info == NULL)
		return -1;

	int depth = 8;
	png_set_IHDR(result->png_ptr, result->png_info, width, height, depth,
			PNG_COLOR_TYPE_RGB,
			PNG_INTERLACE_NONE,
			PNG_COMPRESSION_TYPE_DEFAULT,
			PNG_FILTER_TYPE_DEFAULT);

	png_init_io(result->png_ptr, result->file);

	// matmenu reikes veliau
	result->png_ptr->width = width;
	result->png_ptr->height = height;
	png_write_info(result->png_ptr, result->png_info);
	//png_write_png(result->png_ptr, result->png_info, PNG_TRANSFORM_IDENTITY, NULL);
	return result;
}

// isspausdina lasteles atitinkancia vienetu/nuliu eilute i faila
// failas turi buti sukurtas ir atidarytas
void write_line(char* input, s_png_file* output)
{
	int i;
	int pixel_size = 3;
	int width = output->png_ptr->width;
	png_bytep row = png_malloc(output->png_ptr, width * sizeof(uint8_t) * pixel_size);
	for (i = 0; i < width; i++)
	{
		// juodas pikselis
		if (input[i] == '1')
		{
			row[pixel_size * i] = 0x00;
			row[pixel_size * i + 1] = 0x00;
			row[pixel_size * i + 2] = 0x00;
		}
		else
		// baltas pikselis
		{
			row[pixel_size * i] = 0xFF;
			row[pixel_size * i + 1] = 0xFF;
			row[pixel_size * i + 2] = 0xFF;
		}
	}

	png_write_row(output->png_ptr, row);
	free(row);
}

// uzdaro faila
void finalize_png_file(s_png_file* file)
{
	png_write_end(file->png_ptr, file->png_info);
	fclose(file->file);
}
