#include <iostream>
using namespace std;

int main() {
	double a, b, c, d, x1, x2 = 0;
	cout << "Input a: ";
	cin >> a;
	cout << "Input b: ";
	cin >> b;
	cout << "Input c: ";
	cin >> c;

	d = b * b - 4 * a * c;

	if (d >= 0) {
		x1 = (-b + sqrt(d)) / 2 * a;
		cout << "x1=" << x1 << "\n";
		x2 = (-b - sqrt(d)) / 2 * a;
		cout << "x2=" << x2 << "\n";
	}
	else {
		cout << "No roots" << "\n";
	}
}