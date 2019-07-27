#include <iostream>
#include <fstream>
#include <iomanip>

using namespace std;

#define LEFT 378098.221  // 378098.221  378135.147
#define BOTTOM 4410402.375 // 4410402.375  4410435.655
#define WIDTH  1322 // 1322 1087
#define HEIGHT 993 // 993 774

int main()
{
	ifstream in("out_merge.txt");
	ofstream out("top_pointsA.txt");
	int x, y;
	double dx, dy;
	out << fixed << setprecision(3);
	while (!in.eof()) {
		in >> x >> y;
		dy = y * 0.05 + LEFT;
		dx = (HEIGHT - x) * 0.05 + BOTTOM;
		out << dy << "\t" << dx << endl;
	}
	in.close();
	out.close();
	return 0;
}