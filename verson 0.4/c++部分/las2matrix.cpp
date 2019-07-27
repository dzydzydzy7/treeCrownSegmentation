#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <set>

using namespace std;

#define LEFT 378098.221  // 378098.221  378135.147
#define BOTTOM 4410402.375 // 4410402.375  4410435.655
#define POINT_SIZE 0.05

#define WIDTH 1322	// 1322 1087
#define HEIGHT 993	// 993 774

int treeID[HEIGHT][WIDTH];
int idCounter[2000];	//可能需要扩大

void preProcess()
{
	ifstream in("all.txt");		//
	ofstream out("in.txt");
	double x;	// 378XXX.XXX
	double y;	// 4410XXX.XXX
	double z;
	string id;
	while (!in.eof())
	{
		in >> x >> y >> z >> id;
		if (id == "NA")
			id = "0";
		out << x << y << z << id;
	}
	in.close();
	out.close();
}

void init()
{
	ifstream in("in.txt");
	double x;	// 378XXX.XXX
	double y;	// 4410XXX.XXX
	double z;
	int id;
	double RIGHT = LEFT + WIDTH * 0.05;
	double TOP = BOTTOM + HEIGHT * 0.05;
	while (!in.eof())
	{
		in >> x >> y >> z >> id;
		if (x >= LEFT && x < RIGHT && y >= BOTTOM && y < TOP)
		{
			int xindex = (x - LEFT) / 0.05;
			int yindex = HEIGHT - ((y - BOTTOM) / 0.05);
			treeID[yindex][xindex] = id;	// need process the value "NA"
			idCounter[id]++;
		}
	}
	in.close();
}

void getTops()
{
	ofstream liTop("li_tops1.txt");	//
	/*set<int> id_set;
	for (size_t i = 0; i < HEIGHT; i++)
	{
		for (size_t j = 0; j < WIDTH; j++)
		{
			id_set.insert(treeID[i][j]);

		}
	}*/
	for (int k = 0; k < 2000; k++)
	{
		vector<int> xcollection;
		vector<int> ycollection;
		if (idCounter[k])
		{
			for (size_t i = 0; i < HEIGHT; i++)
			{
				for (size_t j = 0; j < WIDTH; j++)
				{
					if (treeID[i][j] == k) {
						xcollection.push_back(j);
						ycollection.push_back(i);
					}
				}
			}
		}
		int xSum = 0;
		int ySum = 0;
		for (size_t i = 0; i < xcollection.size(); i++)
			xSum += xcollection[i];
		for (size_t i = 0; i < ycollection.size(); i++)
			ySum += ycollection[i];
		if (xcollection.size())liTop << ySum / ycollection.size() << "\t" << xSum / xcollection.size() << endl;
		liTop.close();
	}
}

void outTrees()
{
	ofstream outSeeds("res_seeds_li1.txt");	//
	for (size_t i = 0; i < HEIGHT; i++)
	{
		for (size_t j = 0; j < WIDTH; j++)
		{
			outSeeds << treeID << " ";
		}
		outSeeds << endl;
	}
	outSeeds.close();
}

int main()
{
	preProcess();
	init();
	getTops();
	outTrees();
	return 0;
}