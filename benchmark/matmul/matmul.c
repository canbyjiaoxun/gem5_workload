// Matrix multiplication example

//#include "LPC11xx.h"
//#include "loctypes.h"

//#include "arm_math.h"

#define MATRIX_SIZE 18

//#define PORTBASE 0x20000000
//unsigned int volatile * const port = (unsigned int *) PORTBASE;

int main (void) {
	//arm_status status;
	int i,j,k,itr;
	int m1[MATRIX_SIZE][MATRIX_SIZE],m2[MATRIX_SIZE][MATRIX_SIZE],add[MATRIX_SIZE][MATRIX_SIZE],mult[MATRIX_SIZE][MATRIX_SIZE];
	int sum = 0;	

	for(i=0; i < MATRIX_SIZE; i++)
	{
    	for(j=0; j < MATRIX_SIZE; j++)
      {
		     m1[i][j] = i+j;
		     m2[i][j] = i-j + 10;
		     mult[i][j] = 0;
		     add[i][j] = 0;
	    }
	 }

	for(i=0;i<MATRIX_SIZE;i++)
	{
					for(j=0;j<MATRIX_SIZE;j++)
					{
									add[i][j]=m1[i][j]+m2[i][j];
					}
	}



	for(itr =0;itr<1;itr++)
	{
					sum = 0;
					for(i=0;i<MATRIX_SIZE;i++)
					{
									for(j=0;j<MATRIX_SIZE;j++)
									{
													mult[i][j]=0;
													for(k=0;k<MATRIX_SIZE;k++)
													{
																	mult[i][j]+=m1[i][k]*m2[k][j];
																	sum += mult[i][j];
													}
									}
					}
	}

	if(sum == 30555)
	{  // expected result for checking correctness
	 mult[0][0] = 1;
	 //*port = mult[0][0];
	 //status = ARM_MATH_SUCCESS;
	} else 
	{
	  //status = ARM_MATH_TEST_FAILURE;
	}
	//* port = sum;
	
}


