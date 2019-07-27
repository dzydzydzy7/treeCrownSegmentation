#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
using namespace std;
#define LEFT 378135.147  // 378098.221  378135.147
#define BOTTOM 4410435.655 // 4410402.375  4410435.655
#define WIDTH  1087 // 1322 1087
#define HEIGHT 774 // 993 774
#define PI 3.1415926535

int seg[HEIGHT][WIDTH];

class TreeTop
{
public:
	double x;
	double y;
	double area;
	bool isMatched;
	TreeTop() {}
	TreeTop(double x, double y, double area) : x(x), y(y), area(area) { isMatched = false; }
	TreeTop operator = (const TreeTop &t)
	{
		x = t.x;
		y = t.y;
		area = t.area;
		isMatched = t.isMatched;
	}
};

void init(vector<TreeTop>& manual, vector<TreeTop>& algo)
{
	//ifstream segIn("E:/RStudio/workplace/res_seeds2.txt"); // res_seeds res_seeds2
	ifstream segIn("E:/console/shiyan1/shiyan1/out.txt");
	for (int i = 0; i < HEIGHT; i++)
	{
		for (int j = 0; j < WIDTH; j++)
		{
			segIn >> seg[i][j];
		}
	}
	segIn.close();
	ifstream manualIn("manual2c.txt"); //2
	ifstream algoIn("out_merge2.txt");//2 读入矩阵就搜索每一个点的号，x值平均，y值pj作为输入
	//ifstream algoIn("cttop.txt");
	ofstream mtopOut("mtop.txt");
	double x, y, area;
	double areaSum = 0;
	while (!manualIn.eof())
	{
		manualIn >> x >> y >> area;
		areaSum += area;
		manual.push_back(TreeTop(x, y, area));
		mtopOut << (int)((x - LEFT) * 10) << "\t"<< (int)(HEIGHT - (y - BOTTOM) * 10) <<endl;
	}
	cout << areaSum / 216<<"\t";

	areaSum = 0;
	while (!algoIn.eof())
	{
		algoIn >> x >> y;
		//cout << x << "\t" << y <<endl;
		if (x < HEIGHT && y < WIDTH) {
			int id = seg[int(x)][int(y)];
			area = 0;
			if (id != 0)
				for (size_t i = 0; i < HEIGHT; i++)
					for (size_t j = 0; j < WIDTH; j++)
						if (seg[i][j] == id) area++;
			area /= 400;
			areaSum += area;
			y = y * 0.05 + LEFT;
			x = (HEIGHT - x) * 0.05 + BOTTOM;
			algo.push_back(TreeTop(y, x, area));
		}
	}
	cout << areaSum / 416<<endl;
}

void matchPrint(TreeTop &t1, TreeTop &t2, ofstream & outFile)
{
	cout << t1.x << "\t" << t2.x << "\t";
	cout << t1.y << "\t" << t2.y << "\t";
	cout << fabs(t1.x - t2.x) << " \t" << fabs(t1.y - t2.y) << "\t\t" << t1.area - t2.area << endl;
	outFile <<fixed<< setprecision(3);
	outFile << t1.x << "\t" << t2.x << "\t";
	outFile << t1.y << "\t" << t2.y << "\t";
	outFile << fabs(t1.x - t2.x) << " \t" << fabs(t1.y - t2.y) << "\t\t" << t1.area - t2.area <<"\t";
	outFile << t1.area << "\t" << t2.area << "\t" << fabs((t1.area - t2.area) / t1.area) << endl;
	//outFile << sqrt(t1.area/PI) << "\t" << sqrt(t2.area/PI) << "\t" << fabs(sqrt(t1.area / PI) - sqrt(t2.area / PI))/ sqrt(t1.area / PI) <<endl;
	//outFile << (int)((t2.x - LEFT) * 10) << "\t" << (int)(646 - (t2.y - BOTTOM) * 10) << endl;
}

void match(vector<TreeTop>& manual, vector<TreeTop>& algo)
{
	int count = 0;
	int n = 0;
	double errorSum = 0;
	ofstream outFile("out_s2.txt");	//out1 out2 out_ws
	for (int i = 0; i < manual.size(); i++)
	{
		TreeTop minDisTop;
		double minDis = 9999;
		int minIndex = 0;
		for (int j = 0; j < algo.size(); j++)
		{
			double dis = (manual[i].x - algo[j].x)*(manual[i].x - algo[j].x) + (manual[i].y - algo[j].y)*(manual[i].y - algo[j].y);
			if (dis < minDis)
			{
				minDis = dis;
				minIndex = j;
			}
		}
		
		if (!algo[minIndex].isMatched && minDis < 4)
		{
			matchPrint(manual[i], algo[minIndex],outFile);
			errorSum += fabs(manual[i].area - algo[minIndex].area);
			manual[i].isMatched = true;
			algo[minIndex].isMatched = true;
			count++;
		}
	}
	cout << count << "\t" << errorSum / count << endl;
}

int main()
{
	vector<TreeTop> manual;
	vector<TreeTop> algo;
	init(manual, algo);
	cout << manual.size() << "\t" << algo.size() << endl;
	match(manual, algo);
	return 0;
}