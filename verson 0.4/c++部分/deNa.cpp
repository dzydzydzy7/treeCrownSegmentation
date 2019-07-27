#include <iostream>
#include <fstream>
#include <string>
using namespace std;

#define WIDTH 1087 //1322 1087
#define HEIGHT 774	//993 774

int main()
{
	ifstream in("E:/RStudio/workplace/res_seeds_dal2.txt");
	ofstream out("out.txt");
	string temp = "";
	for (size_t i = 0; i < HEIGHT; i++)
	{
		for (size_t j = 0; j < WIDTH; j++)
		{
			in >> temp;
			if (temp == "NA") temp = "0";
			out << temp<<" ";
		}
		out << endl;
	}
	return 0;
}
