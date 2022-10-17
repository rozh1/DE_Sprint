#include <iostream>
using namespace std;

int main()
{
    int year = 0;
    cout << "Input year: ";
    cin >> year;

    if (year % 4 == 0) cout << "Is leap year";
    else cout << "Is NOT leap year";
}
