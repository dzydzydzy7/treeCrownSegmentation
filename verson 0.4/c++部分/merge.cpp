#include <iostream>
#include <fstream>
using namespace std;

#define WIDTH 1322	//1322 1087
#define HEIGHT 993	//993 774
#define RADIUS 30	//30 40
#define SR 30

int height_tops[HEIGHT][WIDTH];
int img_tops[HEIGHT][WIDTH];
int all_tops[HEIGHT][WIDTH];

void init_height()
{
	ifstream in("cttop.txt");	// cttop.txt cctop2.txt
	int a, b;
	while (in >> a >> b)
	{
		height_tops[a][b] = 1;
	}
	in.close();
}

void init_pic()
{
	ifstream in("img_ttop.txt");	//img_ttop.txt img_ttop2.txt
	double a, b;
	int c, d;
	while (in >> a >> b)
	{
		c = a * HEIGHT / 1000.0;	//1000 800
		d = b * WIDTH / 1400.0;	//1400 1100
		img_tops[c][d] = 1;
	}
	in.close();
	for (size_t i = 0; i < HEIGHT; i++)
		for (size_t j = 0; j < WIDTH; j++)
			if (img_tops[i][j] == 1)
			{
				int xmin = j - SR >= 0 ? j - SR : 0;
				int xmax = j + SR < WIDTH ? j + SR : WIDTH - 1;
				int ymin = i - SR >= 0 ? i - SR : 0;
				int ymax = i + SR < HEIGHT ? i + SR : HEIGHT - 1;
				for (int k = ymin; k <= ymax; k++)
				{
					for (int q = xmin; q <= xmax; q++)
					{
						img_tops[k][q] = 0;
					}
				}
				img_tops[i][j] = 1;
			}

}

void deduplicate()
{
	for (size_t i = 0; i < HEIGHT; i++)
	{
		for (size_t j = 0; j < WIDTH; j++)
		{
			if (height_tops[i][j] == 1) {
				int xmin = j - RADIUS >= 0 ? j - RADIUS : 0;
				int xmax = j + RADIUS < WIDTH ? j + RADIUS : WIDTH - 1;
				int ymin = i - RADIUS >= 0 ? i - RADIUS : 0;
				int ymax = i + RADIUS < HEIGHT ? i + RADIUS : HEIGHT - 1;
				for (int k = ymin; k <= ymax; k++)
				{
					for (int q = xmin; q <= xmax; q++)
					{
						img_tops[k][q] = 0;
					}
				}
			}
		}
	}
}

void out_merge()
{
	ofstream out("out_merge.txt");
	for (size_t i = 0; i < HEIGHT; i++)
	{
		for (size_t j = 0; j < WIDTH; j++)
		{
			if (height_tops[i][j] == 1)
			{
				out << i << "\t" << j << endl;
				all_tops[i][j] = 1;
			}
		}
	}
	for (size_t i = 0; i < HEIGHT; i++)
	{
		for (size_t j = 0; j < WIDTH; j++)
		{
			if (img_tops[i][j] == 1)
			{
				out << i << "\t" << j << endl;
				all_tops[i][j] = 1;
			}
		}
	}
	out.close();

	int count = 0;
	ofstream outMatrix("seeds.txt");
	for (size_t i = 0; i < HEIGHT; i++)
	{
		for (size_t j = 0; j < WIDTH; j++)
		{
			if (all_tops[i][j])outMatrix << all_tops[i][j] + count++ << " ";
			else outMatrix << "0 ";
		}
		outMatrix << endl;
	}
}

void function_merge()
{
	init_height();
	init_pic();
	deduplicate();
	out_merge();
}

int main()
{
	function_merge();
	return 0;
}