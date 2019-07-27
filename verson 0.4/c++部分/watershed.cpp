#include <iostream>
#include <fstream>
#include <cmath>
#include <cstring>
#include <vector>
#include <algorithm>

#define HEIGHT 993 //56.388
#define WIDTH 1322	//97.706 每个px视为0.1m
#define RADIUS 1
using namespace std;

double dsm[HEIGHT][WIDTH];
int seeds[HEIGHT][WIDTH];
int is_used[HEIGHT][WIDTH];
int ttops[500][2];
int tt_index = 0;

void init_dsm()
{
	ifstream in("dsm.txt");
	for (size_t i = 0; i < HEIGHT; i++)
	{
		for (size_t j = 0; j < WIDTH; j++)
		{
			in >> dsm[i][j];
		}
	}
	in.close();
}

void init_treetop()
{
	ifstream in("treeTop.txt");
	int a, b;
	while (in >> a >> b)
	{
		ttops[tt_index][0] = a;
		ttops[tt_index][1] = b;
		tt_index++;
	}
	memset(seeds, 0, sizeof(seeds));
	for (int i = 0; i < tt_index; i++)
	{
		seeds[ttops[i][0]][ttops[i][1]] = i + 1;//树的标号
	}
	in.close();
}

double region_min(int izs, int jzs, int iyx, int jyx)//i左上,i左上,j右下,j右下，前闭后开
{
	double minn = 0x3f3f3f3f;
	for (int i = izs; i < iyx; i++)
		for (int j = jzs; j < jyx; j++)
		{
			if (dsm[i][j] < minn)
				minn = dsm[i][j];
		}
	return minn;
}

double get_threshold(int i_idx, int j_idx)
{
	vector<double> points;
	for (int i = i_idx - 30; i < i_idx + 30; i++)
	{
		for (int j = j_idx - 30; j < j_idx + 30; j++)
		{
			points.push_back(dsm[i][j]);
		}
	}
	sort(points.begin(), points.end());
	int res_idx = points.size() * 0.4;
	return points[res_idx];
}

void segment(int i_idx, int j_idx)
{
	//double minn = region_min(i_idx - 10, j_idx - 10, i_idx + 10, j_idx + 10);
	double threshold = get_threshold(i_idx, j_idx);
	for (int i = i_idx - 30; i < i_idx + 30; i++)
	{
		for (int j = j_idx - 30; j < j_idx + 30; j++)
		{
			if (dsm[i][j] > threshold)
			{
				seeds[i][j] = seeds[i_idx][j_idx];
			}
		}
	}
}

void get_center_treetop()//去掉边缘的树顶
{
	ofstream out("cttop.txt");
	for (size_t i = 0; i < tt_index; i++)
	{
		out << ttops[i][0] << "\t" << ttops[i][1] << endl;
		/*if(ttops[i][1]>RADIUS && ttops[i][1] < WIDTH - RADIUS)
			if (ttops[i][0] > RADIUS && ttops[i][0] < HEIGHT - RADIUS)
			{
				out << ttops[i][0] << "\t" << ttops[i][1] << endl;
			}*/
	}
	out.close();
}

void write_seeds(int x, int y)//按照分水岭结果扩展点
{
	int points[RADIUS * 2][RADIUS * 2];
	ifstream in("res.txt");
	for (size_t i = 0; i < RADIUS * 2; i++)
	{
		for (size_t j = 0; j < RADIUS * 2; j++)
		{
			in >> points[i][j];
		}
	}
	in.close();
	int label = points[RADIUS][RADIUS];
	int s = seeds[x][y];
	for (size_t i = 0; i < RADIUS * 2; i++)
	{
		for (size_t j = 0; j < RADIUS * 2; j++)
		{
			if (points[i][j] == label)
			{
				seeds[i + x - RADIUS][j + y - RADIUS] = s;
			}
		}
	}
}

void creat_data(int x, int y)//输出一个方框的点到文件
{
	ofstream out("out.txt");
	double dsm_r[RADIUS * 2][RADIUS * 2];
	vector<double> p;
	for (int i = x - RADIUS; i < x + RADIUS; i++)
	{
		for (int j = y - RADIUS; j < y + RADIUS; j++)
		{
			p.push_back(dsm[i][j]);
		}
	}
	sort(p.begin(),p.end());
	int idx = RADIUS * RADIUS * 0.5 * 4;
	double s = p[idx];
	for (size_t i = 0; i < RADIUS * 2; i++)
	{
		for (size_t j = 0; j < RADIUS * 2; j++)
		{
			dsm_r[i][j] = dsm[i + x - RADIUS][j + y - RADIUS];
			//if (dsm_r[i][j] > s) dsm_r[i][j]++;
			out << dsm_r[i][j] << "\t";
		}
		out << endl;
	}
	out.close();

	/*ofstream out2("seeds.txt");
	for (int i = 384 - 40; i < 384 + 40; i++)
	{
		for (int j = 590 - 40; j < 590 + 40; j++)
		{
			out2 << seeds[i][j] << "\t";
		}
		out2 << endl;
	}
	out2.close();*/
}

void seeds_for_py()//写出整个seeds
{
	ofstream out("seeds.txt");
	for (int i = 0; i < HEIGHT; i++)
	{
		for (int j = 0; j < WIDTH; j++)
		{
			out << seeds[i][j] << " ";
		}
		out << endl;
	}
	out.close();
}

int main()
{
	init_dsm();
	init_treetop();
	//memset(is_used, 0, sizeof(is_used));
	//segment(336, 461);
	//segment(384, 590);
	//segment(64, 474);
	//segment(195, 410);
	//segment(100, 268);

	get_center_treetop();
	//creat_data(384, 590);
	//creat_data(195, 410);
	//write_seeds(384, 590);
	seeds_for_py();

	return 0;
}
//蓝色是高于阈值的部分，树之间的间隔高于部分树冠