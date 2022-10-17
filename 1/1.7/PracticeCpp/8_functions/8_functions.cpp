#include <iostream>
using namespace std;

void randomize(int** m, int rows, int cols)
{
	for (int i = 0; i < rows; i++)
	{
		for (int j = 0; j < cols; j++)
		{
			m[i][j] = 30 + rand() % 30;
		}
	}
}

int min(int** m, int rows, int cols)
{
	int min = m[0][0];
	for (int i = 0; i < rows; i++)
	{
		for (int j = 0; j < cols; j++)
		{
			if (min > m[i][j]) min = m[i][j];
		}
	}
	return min;
}

int max(int** m, int rows, int cols)
{
	int max = m[0][0];
	for (int i = 0; i < rows; i++)
	{
		for (int j = 0; j < cols; j++)
		{
			if (max < m[i][j]) max = m[i][j];
		}
	}
	return max;
}

int main()
{
	int** m = new int* [5];
	for (int i = 0; i < 5; i++)
	{
		m[i] = new int[5];
	}

	randomize(m, 5, 5);

	cout << "Matrix: " << endl;
	for (int i = 0; i < 5; i++)
	{
		for (int j = 0; j < 5; j++)
		{
			cout << m[i][j] << "\t";
		}
		cout << endl;
	}
	cout << "Min: " << min(m, 5, 5) << endl;
	cout << "Max: " << max(m, 5, 5) << endl;
}
