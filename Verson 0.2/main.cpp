#include <iostream>
#include <fstream>
#include <cmath>
#include <cstring>

using namespace std;

#define WIDTH 978
#define HEIGHT 564
#define WINDOW_WIDTH 163
#define WINDOW_HEIGHT 188
#define IGNORE_RATE 0.7
#define RADIUS 14
#define MINRAD 10
#define SHAPE 1  //1圆形 0方形

float _data[HEIGHT][WIDTH];
int flags[HEIGHT][WIDTH]; //0是树顶

int main() {
	memset(_data, 0, sizeof(_data));
	memset(flags, 0, sizeof(flags));
	//int count = 0;
	ifstream in("dsm.txt");
	ofstream out("treeTop.txt");

	
	if (!in.is_open())
	{
		cout << "can not open this file" << endl;
		return 0;
	}
	for (int i = 0; i < HEIGHT; i++)
	{
		for (int j = 0; j < WIDTH; j++)
		{
			in >> _data[i][j];
		}
	}
	for (int i = 0; i < HEIGHT; i++)
	{
		for (int j = 0; j < WIDTH; j++)
		{
			int xmin = j - RADIUS >= 0 ? j - RADIUS : 0;
			int xmax = j + RADIUS < WIDTH ? j + RADIUS : WIDTH - 1;
			int ymin = i - RADIUS >= 0 ? i - RADIUS : 0;
			int ymax = i + RADIUS < HEIGHT ? i + RADIUS : HEIGHT - 1;

			for (int k = ymin; k <= ymax; k++)
			{
				for (int q = xmin; q <= xmax; q++)
				{
					if (SHAPE)
					{
						int xx = abs(q - j);
						int yy = abs(k - i);

						if ((xx * xx + yy * yy <= RADIUS * RADIUS && _data[k][q] > _data[i][j]) || _data[i][j] < 20)
						{
							flags[i][j] = 1;
						}
					}
					else {
						if (_data[k][q] > _data[i][j])
						{
							flags[i][j] = 1;
						}
					}
				}
			}
		}
	}

	for (int i = MINRAD; i < HEIGHT - MINRAD; i++)
	{
		for (int j = MINRAD; j < WIDTH - MINRAD; j++)
		{
			if (flags[i][j] == 0)
			{
				for(int k = i - MINRAD; k < i + MINRAD; k++)
					for (int q = j - MINRAD; q < j + MINRAD; q++)
					{
						flags[k][q] = 1;
					}
				flags[i][j] = 0;
			}
		}
	}

	/*for (int i = 0; i < HEIGHT; i += WINDOW_HEIGHT)
	{
		for (int j = 0; j < WIDTH; j += WINDOW_WIDTH)
		{
			float sum = 0;
			float mean = 0;
			float th = 0;
			int count = 0;
			for (int k = i; k < i + WINDOW_HEIGHT; k++)
			{
				for (int q = j; q < j + WINDOW_WIDTH; q++)
				{
					if (!flags[k][q])
					{
						sum += _data[k][q];
						count++;
					}
				}
			}
			mean = sum / count;
			cout << mean << "\t" <<count << endl;
			th = mean * IGNORE_RATE;
			for (int k = i; k < i + WINDOW_HEIGHT; k++)
			{
				for (int q = j; q < j + WINDOW_WIDTH; q++)
				{
					if (!flags[k][q] && _data[k][q] < th)
					{
						flags[k][q] = 1;
					}
				}
			}
		}
	}*/

	for (int i = 1; i < HEIGHT; i++)
	{
		for (int j = 1; j < WIDTH; j++)
		{
			if (flags[i][j] == 0)
			{
				out << i << "\t" << j << endl;
			}
		}
	}

	//cout << count << endl;
	in.close();
	out.close();
	return 0;
}