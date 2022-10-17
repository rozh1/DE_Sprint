#include <iostream>
using namespace std;

int main() {
	int a, b = 0;
	cout << "Input a: ";
	cin >> a;
	cout << "Input b: ";
	cin >> b;

	if (a > b) {
		cout << "a>b" << "\n";
	}
	else if (a < b) {
		cout << "a<b" << "\n";
	}
	else {
		cout << "a=b" << "\n";
	}
}