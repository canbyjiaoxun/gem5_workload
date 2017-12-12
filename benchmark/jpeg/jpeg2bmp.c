/*
+--------------------------------------------------------------------------+
| CHStone : a suite of benchmark programs for C-based High-Level Synthesis |
| ======================================================================== |
|                                                                          |
| * Collected and Modified : Y. Hara, H. Tomiyama, S. Honda,               |
|                            H. Takada and K. Ishii                        |
|                            Nagoya University, Japan                      |
|                                                                          |
| * Remark :                                                               |
|    1. This source code is modified to unify the formats of the benchmark |
|       programs in CHStone.                                               |
|    2. Test vectors are added for CHStone.                                |
|    3. If "main_result" is 0 at the end of the program, the program is    |
|       correctly executed.                                                |
|    4. Please follow the copyright of each benchmark program.             |
+--------------------------------------------------------------------------+
*/
/*
 * Copyright (C) 2008
 * Y. Hara, H. Tomiyama, S. Honda, H. Takada and K. Ishii
 * Nagoya University, Japan
 * All rights reserved.
 *
 * Disclaimer of Warranty
 *
 * These software programs are available to the user without any license fee or
 * royalty on an "as is" basis. The authors disclaims any and all warranties, 
 * whether express, implied, or statuary, including any implied warranties or 
 * merchantability or of fitness for a particular purpose. In no event shall the
 * copyright-holder be liable for any incidental, punitive, or consequential damages
 * of any kind whatsoever arising from the use of these programs. This disclaimer
 * of warranty extends to the user of these programs and user's customers, employees,
 * agents, transferees, successors, and assigns.
 *
 */
/*
 *  Transformation: JPEG -> BMP
 *  
 *  @(#) $Id: jpeg2bmp.c,v 1.2 2003/07/18 10:19:21 honda Exp $ 
 */

/*
 * Buffer for reading JPEG file
 */
unsigned char JpegFileBuf[JPEG_FILE_SIZE];


int jpeg2bmp_main ()
{
  int ci;
  unsigned char *c;
  int i, j;
 
  
  /* randomly set the input data, Xun 08/08/17*/
  // set rand seed 
  int rand_seed, ii; 
  FILE *rand_seed_file = fopen("rand_seed.txt", "r");
  fscanf(rand_seed_file, "%d", &rand_seed);
  srand(rand_seed);
  fclose(rand_seed_file);
  // generate random input data 
  //int JPEGSIZE = rand() % 2000; 
  //int JPEGSIZE = 5207;
  int hana_jpg_test[JPEGSIZE];
  hana_jpg_test[0] = 255; 
  hana_jpg_test[1] = 216;
  for (ii = 2; ii < JPEGSIZE; ii++)
  {
      //hana_jpg[ii] = rand() % 255;   // RGB value 
      if(hana_jpg[ii] == 218 || hana_jpg[ii] == 217 || hana_jpg[ii] == 216 || hana_jpg[ii]
              == 192 || hana_jpg[ii] == 196 || hana_jpg[ii] == 219)
      {
          hana_jpg_test[ii] = hana_jpg[ii];   // RGB value 
          printf("original\n");
      }
      else
          hana_jpg_test[ii] = hana_jpg[ii]+2;   // RGB value 
  }
  //write input SIZE to a file 
  //FILE *input_size_file = fopen("./data/bf/input_size.txt", "a");
 //FILE *input_size_file = fopen("input_size.txt", "a");
  //fprintf(input_size_file, "%d\n", JPEGSIZE);
  //printf("HEHE\n");
  //fclose(input_size_file);
  
  
  /*
   * Store input data in buffer
   */
  c = JpegFileBuf;
  for (i = 0; i < JPEGSIZE; i++)
    
    {        ci = hana_jpg_test[i];
        *c++ = ci;
    }

  
  printf("HEHE2\n");
  jpeg_read (JpegFileBuf);
  printf("HEHE3\n");
  
  /*
  for (i = 0; i < RGB_NUM; i++)
    {
      for (j = 0; j < BMP_OUT_SIZE; j++)
	{
	  if (OutData_comp_buf[i][j] != hana_bmp[i][j])
	    {
	      main_result++;
	    }
	}
    }
  if (OutData_image_width != out_width)
    {
      main_result++;
    }
  if (OutData_image_height != out_length)
    {
      main_result++;
    }
    */
  return (0);
}
