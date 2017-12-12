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
/* aes.c */
/*
 * Copyright (C) 2005
 * Akira Iwata & Masayuki Sato
 * Akira Iwata Laboratory,
 * Nagoya Institute of Technology in Japan.
 *
 * All rights reserved.
 *
 * This software is written by Masayuki Sato.
 * And if you want to contact us, send an email to Kimitake Wakayama
 * (wakayama@elcom.nitech.ac.jp)
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. All advertising materials mentioning features or use of this software must
 *    display the following acknowledgment:
 *    "This product includes software developed by Akira Iwata Laboratory,
 *    Nagoya Institute of Technology in Japan (http://mars.elcom.nitech.ac.jp/)."
 *
 * 4. Redistributions of any form whatsoever must retain the following
 *    acknowledgment:
 *    "This product includes software developed by Akira Iwata Laboratory,
 *     Nagoya Institute of Technology in Japan (http://mars.elcom.nitech.ac.jp/)."
 *
 *   THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT EXPRESS OR IMPLIED WARRANTY.
 *   AKIRA IWATA LABORATORY DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
 *   SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS,
 *   IN NO EVENT SHALL AKIRA IWATA LABORATORY BE LIABLE FOR ANY SPECIAL,
 *   INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
 *   FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
 *   NEGLIGENCE OR OTHER TORTUOUS ACTION, ARISING OUT OF OR IN CONNECTION
 *   WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 */
#include <stdio.h>


int main_result;

#include "aes.h"
#include "aes_enc.c"
#include "aes_dec.c"
#include "aes_key.c"
#include "aes_func.c"

/* ***************** main **************************** */
int
aes_main (void)
{
/*
+--------------------------------------------------------------------------+
| * Test Vectors (added for CHStone)                                       |
|     statemt, key : input data                                            |
+--------------------------------------------------------------------------+
*/
  int i, rand_seed; 
  FILE *input_value_file = fopen("./data/aes/input_value.txt","a"); 
  FILE *input_size_file = fopen("./data/aes/input_size.txt","a");
  FILE *rand_seed_file = fopen("rand_seed.txt", "r");
  fscanf(rand_seed_file, "%d", &rand_seed);
  srand(rand_seed); 
  int SIZE = rand() % 10 + 2; 
  printf("The SIZE is %d\n", SIZE);
  //int SIZE = 16; 
  fprintf(input_size_file, "%d\n", SIZE);
  for (i = 0; i < SIZE; i++)
  {
      statemt[i] = rand() % 10; 
      key[i] = rand() % 10; 
  }

  for (i = 0; i < SIZE; i++)
  {
      fprintf(input_value_file, "%d\t", statemt[i]);
  }
  for (i = 0; i < SIZE; i++)
  {
      fprintf(input_value_file, "%d\t", key[i]);
  }
  fprintf(input_value_file, "\n");
  fclose(input_value_file);
  fclose(input_size_file);

  encrypt (statemt, key, 128128);
  //decrypt (statemt, key, 128128);
  return 0;
}

int
main ()
{
      main_result = 0;
      aes_main ();
      printf ("\n%d\n", main_result);
      return main_result;
    }
