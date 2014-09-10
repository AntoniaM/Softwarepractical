#include<stdio.h>

void fun(double x[], double y[])
{
   double v[9];
   v[0] = x[0];
   v[1] = x[1];
   v[2] = v[0] * 1.0;
   v[3] = v[1] * 0.0;
   v[4] = v[2] + v[3];
   v[8] = v[4] * 2.0;
   y[0] = v[8];
}

int main(){
	int nx = 2;
	double x[nx];
	x[0] = 11.1;
	x[1] = 2;
	int ny = 1;
	double y[ny];
	fun(x,y);
	printf("Ergebnis = \n%f",*y);
	for (int i=1; i<ny; i++)
		printf(",%f",*(y+i));
	printf("\n");
	return 0;

}
