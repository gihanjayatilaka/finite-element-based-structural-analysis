#define _USE_MATH_DEFINES

#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>

cudaError_t addWithCuda(int *c, const int *a, const int *b, unsigned int size);

void print_arr(int*, int, int);
void print_arr(double*, int, int);
double determinant(double* A, int n);
void adjoint(double* A, double* adj, int n);
bool inverse(double* A, double* inverse, int n);

__global__ void addKernel(int *c, const int *a, const int *b)
{
    int i = threadIdx.x;
    c[i] = a[i] + b[i];
}

int main() {
	//Nodal coordinates
	//-----------------

	const int x[] = { 0, 6, 12, 18, 24, 18, 12, 6 };
	const int y[] = { 0, 0, 0,  0,  0,  6,  6,  6 };

	//Element connectivity(ECM)
	// -------------------------

	const int ECM[2][13] = { {0, 1, 2, 3, 4, 5, 6, 0, 1, 1, 2, 3, 3},
						  {1, 2, 3, 4, 5, 6, 7, 7, 7, 6, 6, 6, 5} };

	//Material properites
	//--------------------

	const long	E = 200 * (1000000);

	//Geomatric properties
	//---------------------

	const double CArea[] = { .0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012, .0012 }; //cross section area
	const double	L[] = { 6,     6,     6,     6,  6 * sqrt(2), 6,    6,  6 * sqrt(2), 6, 6 * sqrt(2), 6,  6 * sqrt(2), 6 };

	//Additional input parameters required for coding
	//-----------------------------------------------

	const int	 nn = 8;	//number of nodes
	const int	nel = 13;   //number of el ements
	const int	nen = 2;	//number of nodes in an element
	const int  ndof = 2;	//number of dof per node

	int	tdof = nn*ndof;
	double Ang[] = { 0, 0, 0, 0, M_PI / 4 * 3, M_PI, M_PI, M_PI / 4 , M_PI / 2, M_PI / 4, M_PI / 2, M_PI / 4 * 3, M_PI / 2 };
	int LCM[2 * ndof][nel] = {}; //Local Coo matrix
	double K[nn*ndof][nn*ndof] = {}; //Global stiffness matrix

	//Restrained DOF to Apply BC
	//---------------------------

	int BC[] = { 1, 2, 10 }; //restrained dof

	//Local coordinate matrix(LCM)
	// -----------------------------
	int ind;
	for (int j = 0; j < nen; j++) {
		for (int e = 0; e < nel; e++) {
			for (int m = 0; m < ndof; m++) {
				ind = j*ndof + m;
				LCM[ind][e] = ndof*ECM[j][e] + m;
			}
		}
	}
	printf("LCM\n");
	print_arr((int *)LCM, 2 * ndof, nel);

	//Element local stiffness matrix ke
	//---------------------------------

	for (int k = 0; k < nel; k++) {
		double c = cos(Ang[k]);
		double s = sin(Ang[k]);
		double const_ = CArea[k] * E / L[k];
		double ke[4][4] = { {c*c, c*s, -c*c, -c*s},
					 {c*s, s*s, -c*s, -s*s},
					 {-c*c, -c*s, c*c, c*s},
					 {-c*s, -s*s, c*s, s*s} };

		for (int i = 0; i < 4; i++)
			for (int j = 0; j < 4; j++)
				ke[i][j] = ke[i][j] * const_;

		print_arr((double*)ke, 4, 4);
		// Structure Global stiffenss matrix
		// ---------------------------------

		for (int loop1 = 0; loop1 < nen*ndof; loop1++) {
			int i = LCM[loop1][k];
			for (int loop2 = 0; loop2 < nen*ndof; loop2++) {
				int j = LCM[loop2][k];
				K[i][j] = K[i][j] + ke[loop1][loop2];
			}
		}
	}
	printf("K\n");
	print_arr((double*)K, nn*ndof, nn*ndof);
	//correct upto here


	double Kf[nn*ndof][nn*ndof] = {};
	for (int i = 0; i < nn*ndof; i++){
		for (int j = 0; j < nn*ndof; j++) {
			Kf[i][j] = K[i][j];
		}
    }

	//int Kf[][] = K;

	//Applying Boundary conditions
	//----------------------------

	for (int p = 0; p < sizeof(BC) / sizeof(BC[0]); p++) {
		for (int q = 0; q < tdof; q++) {
			K[BC[p]][ q] = 0;
		}
		K[BC[p]][ BC[p]] = 1;
	}
	

	//Force vector
	//------------

	double f[] = { 0, 0, 0, -200, 0, -100, 0, -100, 0, 0, 0, 0, 0, 0, 0, 0 };

	//Displacement vector
	//-------------------
	const int z = 16;
	double inv[z][z];
	double tt[z][z];
	for (int i = 0; i < z; i++) {
		for (int j = 0; j < z; j++) {
			tt[i][j] = (10 * ((float)rand() / RAND_MAX));
		}
	}
	
	inverse((double*)tt, (double*)inv, z);

	printf("inv\n");
	print_arr((double*)inv, z,z);

	//mat_mul(inv,f);
	//d = K\f

	//Reaction forces
	//---------------

	//mat_mul(Kf,d);
	//fr = Kf*d

	//Axial forces
	//------------
	/*
	for (int e = 0; e < nel; e++) {
		de = d[LCM[:, e]];   //displacement of the current element
		const_ = CArea[e] * E / L[e]; //constant parameter with in the elementt
		p = Ang[e];
		c = cos(e);
		force[e] = const_*{ -c, -s, c, s } *de;
	}*/

	/*
	const int arraySize = 5;
    const int a[arraySize] = { 1, 2, 3, 4, 5 };
    const int b[arraySize] = { 10, 20, 30, 40, 50 };
    int c[arraySize] = { 0 };

    // Add vectors in parallel.
    cudaError_t cudaStatus = addWithCuda(c, a, b, arraySize);
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "addWithCuda failed!");
        return 1;
    }

    printf("{1,2,3,4,5} + {10,20,30,40,50} = {%d,%d,%d,%d,%d}\n",
        c[0], c[1], c[2], c[3], c[4]);

    // cudaDeviceReset must be called before exiting in order for profiling and
    // tracing tools such as Nsight and Visual Profiler to show complete traces.
    cudaStatus = cudaDeviceReset();
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaDeviceReset failed!");
        return 1;
    }*/
	scanf("%d", &ind);
    return 0;
}

// Helper function for using CUDA to add vectors in parallel.
cudaError_t addWithCuda(int *c, const int *a, const int *b, unsigned int size)
{
    int *dev_a = 0;
    int *dev_b = 0;
    int *dev_c = 0;
    cudaError_t cudaStatus;

    // Choose which GPU to run on, change this on a multi-GPU system.
    cudaStatus = cudaSetDevice(0);
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaSetDevice failed!  Do you have a CUDA-capable GPU installed?");
        goto Error;
    }

    // Allocate GPU buffers for three vectors (two input, one output)    .
    cudaStatus = cudaMalloc((void**)&dev_c, size * sizeof(int));
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaMalloc failed!");
        goto Error;
    }

    cudaStatus = cudaMalloc((void**)&dev_a, size * sizeof(int));
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaMalloc failed!");
        goto Error;
    }

    cudaStatus = cudaMalloc((void**)&dev_b, size * sizeof(int));
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaMalloc failed!");
        goto Error;
    }

    // Copy input vectors from host memory to GPU buffers.
    cudaStatus = cudaMemcpy(dev_a, a, size * sizeof(int), cudaMemcpyHostToDevice);
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaMemcpy failed!");
        goto Error;
    }

    cudaStatus = cudaMemcpy(dev_b, b, size * sizeof(int), cudaMemcpyHostToDevice);
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaMemcpy failed!");
        goto Error;
    }

    // Launch a kernel on the GPU with one thread for each element.
    addKernel<<<1, size>>>(dev_c, dev_a, dev_b);

    // Check for any errors launching the kernel
    cudaStatus = cudaGetLastError();
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "addKernel launch failed: %s\n", cudaGetErrorString(cudaStatus));
        goto Error;
    }
    
    // cudaDeviceSynchronize waits for the kernel to finish, and returns
    // any errors encountered during the launch.
    cudaStatus = cudaDeviceSynchronize();
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaDeviceSynchronize returned error code %d after launching addKernel!\n", cudaStatus);
        goto Error;
    }

    // Copy output vector from GPU buffer to host memory.
    cudaStatus = cudaMemcpy(c, dev_c, size * sizeof(int), cudaMemcpyDeviceToHost);
    if (cudaStatus != cudaSuccess) {
        fprintf(stderr, "cudaMemcpy failed!");
        goto Error;
    }

Error:
    cudaFree(dev_c);
    cudaFree(dev_a);
    cudaFree(dev_b);
    
    return cudaStatus;
}

// Function to get cofactor of A[p][q] in temp[][]. n is current dimension of A[][] 
void getCofactor(double* A, double* temp, int p, int q, int n){
	int i = 0, j = 0;

	// Looping for each element of the matrix 
	for (int row = 0; row < n; row++){
		for (int col = 0; col < n; col++){
			//  Copying into temporary matrix only those element 
			//  which are not in given row and column 
			if (row != p && col != q){
				temp[i*n + j] = A[row*n + col];
				j++;
				// Row is filled, so increase row index and 
				// reset col index 
				if (j == n - 1){
					j = 0;
					i++;
				}
			}
		}
	}
}

/* Recursive function for finding determinant of matrix.
n is current dimension of A[][]. */
double determinant(double* A, int n){
	double D = 0; // Initialize result 

	//  Base case : if matrix contains single element 
	if (n == 1)
		return A[0];

	double* temp =(double*) malloc(sizeof(double)*n*n); // To store cofactors 

	int sign = 1;  // To store sign multiplier 

	// Iterate for each element of first row 
	for (int f = 0; f < n; f++){
		// Getting Cofactor of A[0][f] 
		getCofactor(A, temp, 0, f, n);
		D += sign * A[0*n + f] * determinant(temp, n - 1);
		// terms are to be added with alternate sign 
		sign = -sign;
	}
	free(temp);
	return D;
}

// Function to get adjoint of A[N][N] in adj[N][N]. 
void adjoint(double* A, double* adj, int n){
	if (n == 1){
		adj[0] = 1;
		return;
	}

	// temp is used to store cofactors of A[][] 
	int sign = 1;
	double *temp = (double*) malloc(sizeof(double)*n*n);

	for (int i = 0; i<n; i++){
		for (int j = 0; j<n; j++){
			// Get cofactor of A[i][j] 
			getCofactor(A, temp, i, j, n);

			// sign of adj[j][i] positive if sum of row 
			// and column indexes is even. 
			sign = ((i + j) % 2 == 0) ? 1 : -1;

			// Interchanging rows and columns to get the 
			// transpose of the cofactor matrix 
			adj[j*n + i] = (sign)*(determinant(temp, n - 1));
		}
	}
	free(temp);
}

// Function to calculate and store inverse, returns false if 
// matrix is singular 
bool inverse(double* A, double* inverse, int n){
	// Find determinant of A[][] 
	double det = determinant(A, n);
	printf("%lf\n", det);
	if (det < (double)1e-6 && det > -(double)1e-6){
		//cout << "Singular matrix, can't find its inverse";
		return false;
	}
	// Find adjoint 
	double* adj = (double*)malloc(sizeof(double)*n*n);
	adjoint(A, adj,n);

	// Find Inverse using formula "inverse(A) = adj(A)/det(A)" 
	for (int i = 0; i<n; i++)
		for (int j = 0; j<n; j++)
			inverse[i*n + j] = adj[i*n + j] / double(det);
	free(adj);
	return true;
}

void print_arr(int *arr, int m, int n) {
	int i, j;
	for (i = 0; i < m; i++) {
		for (j = 0; j < n; j++)
			printf("%d ", *((arr + i*n) + j));
		printf("\n");
	}
}

void print_arr(double *arr, int m, int n) {
	int i, j;
	for (i = 0; i < m; i++) {
		for (j = 0; j < n; j++)
			printf("%lf ", *((arr + i*n) + j));
		printf("\n");
	}
}