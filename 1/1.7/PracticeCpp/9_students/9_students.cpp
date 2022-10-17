#include <iostream>

struct student
{
	char fio[50];
	char group[6];
	int scores[5];

	double avg_score()
	{
		int sum = 0;
		for (int i=0; i< 5; i++)
		{
			sum += scores[i];
		}

		return sum / 5.0;
	}

	void print()
	{
		std::cout << fio << "\t" << group << "\t" << avg_score() << "\t";
		for (int i = 0; i < 5; i++)
		{
			std::cout << scores[i] << " ";
		}
		std::cout << std::endl;
	}

	bool is_only_5_4()
	{
		for (int i = 0; i < 5; i++)
		{
			if (scores[i] < 4) return false;
		}
		return true;
	}
};

int main()
{
	student students[10] = {
		{
			"Student 1", "123-a", { 3, 4, 4, 5, 3}
		},
		{
			"Student 2", "321-a", { 4, 5, 5, 4, 2}
		},
		{
			"Student 3", "123-a", { 5, 3, 4, 5, 5}
		},
		{
			"Student 4", "321-a", { 2, 4, 5, 4, 5}
		},
		{
			"Student 5", "123-a", { 3, 3, 4, 5, 5}
		},
		{
			"Student 6", "312-a", { 4, 4, 5, 5, 4}
		},
		{
			"Student 7", "123-a", { 5, 3, 4, 4, 3}
		},
		{
			"Student 8", "312-a", { 2, 4, 5, 4, 5}
		},
		{
			"Student 9", "123-a", { 3, 3, 4, 5, 3}
		},
		{
			"Student 10", "312-a", { 4, 5, 5, 4, 4}
		},
	};

	//sort by avg score
	for (int i = 0; i<10; i++)
	{
		for (int j = i; j < 10; j++)
		{
			if (students[i].avg_score() < students[j].avg_score())
			{
				student tmp = students[j];
				students[j] = students[i];
				students[i] = tmp;
			}
		}
	}

	for (int i = 0; i < 10; i++)
	{
		students[i].print();
	}

	std::cout << std::endl << std::endl << "Only 5 or 4" << std::endl;

	for (int i = 0; i < 10; i++)
	{
		if (students[i].is_only_5_4())
			students[i].print();
	}
}
