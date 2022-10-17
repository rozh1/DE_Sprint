#include <iostream>
using namespace std;

int main()
{
    int n = 0;
    int max = 0;
    do
    {
        cout << "Input number: ";
        cin >> n;
        if (n > max) max = n;
    }
    while (n >= 0);


    cout << "Max number: " << max;
}
