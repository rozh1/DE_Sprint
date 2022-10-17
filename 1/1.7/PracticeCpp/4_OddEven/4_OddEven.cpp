#include <iostream>
using namespace std;

int main()
{
	int a = 0;
	cout << "Input a: ";
	cin >> a;

	cout << (a % 2 == 0 ? "Is Odd" : "Is Even");

}