#include <iostream>
#include <conio.h>
using namespace std;

struct train
{
	char destination[50];
	char number[4];
	char dep_time[6];

	void print()
	{
		std::cout << number << "\t" << destination << "\t" << dep_time << std::endl;
	}

	int compare_dest(train other)
	{
		int result = strcmp(destination, other.destination);
		if (result == 0)
		{
			result = strcmp(dep_time, other.dep_time);
		}
		return result;
	}
};

void sort_by_number(train* t, int len)
{
	for (int i = 0; i < len; i++)
	{
		for (int j = i; j < len; j++)
		{
			if (strcmp(t[i].number, t[j].number) > 0)
			{
				train tmp = t[j];
				t[j] = t[i];
				t[i] = tmp;
			}
		}
	}
}
void sort_by_destination(train* t, int len)
{
	for (int i = 0; i < len; i++)
	{
		for (int j = i; j < len; j++)
		{
			if (t[i].compare_dest(t[j]) > 0)
			{
				train tmp = t[j];
				t[j] = t[i];
				t[i] = tmp;
			}
		}
	}
}
void find_train(train* t, int len)
{
	char train_number[5] = { 0 };
	int count = 0;
	cout << "Enter train number: ";
	cin >> train_number;
	for (int i = 0; i < len; i++)
	{
		if (strcmp(train_number, t[i].number) == 0)
		{
			t[i].print();
			count++;
		}
	}
	if (count == 0) cout << "Not found" << endl;
}

int main()
{
	train trains[5] = {
		{
			"Moscow", "A12", "12:30"
		},
		{
			"Kazan", "A13", "22:00"
		},
		{
			"Kazan", "A10", "12:00"
		},
		{
			"Ufa", "D01", "14:15"
		},
		{
			"Moscow", "B04", "06:45"
		},
	};

	char input;

	while (true)
	{
		system("cls");
		cout << "Select action" << endl;
		cout << "[1] Print train table" << endl;
		cout << "[2] Print train info" << endl;
		cout << "[3] Print destination table" << endl;
		cout << "[q] Exit" << endl;

		input = _getch();
		cout << endl;

		switch (input)
		{
		case '1':
			sort_by_number(trains, 5);
			for (int i = 0; i < 5; i++)
			{
				trains[i].print();
			}
			break;
		case '2':
			find_train(trains, 5);
			break;
		case '3':
			sort_by_destination(trains, 5);
			for (int i = 0; i < 5; i++)
			{
				trains[i].print();
			}
			break;
		case 'q':
			exit(0);
			break;
		default:
			cout << "Wrong option" << endl;
		}
		cout << endl << "Press any key to continue" << endl;
		_getch();
	}
}
