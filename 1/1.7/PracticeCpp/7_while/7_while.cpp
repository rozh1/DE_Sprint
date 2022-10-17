#include <iostream>
using namespace std;

int main()
{
	float x = -4;
	while (x < 4 + 0.5f)
	{

		cout << "x=" << x << "\ty=" << (-2 * x * x - 5 * x - 8) << endl;
		x += 0.5f;
	}
}
