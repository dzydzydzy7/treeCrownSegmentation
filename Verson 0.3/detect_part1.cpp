#include <Rcpp.h>
using namespace Rcpp;

bool isInCricle(int x, int y, int centerx, int centery, int radius)
{
  int dx2 = (x - centerx)*(x - centerx);
  int dy2 = (y - centery)*(y - centery);
  int r2 = radius * radius;
  if(dx2 + dy2 <= r2)return true;
  else return false;
}

// [[Rcpp::export]]
IntegerMatrix detect_part1(NumericMatrix chm) {
  int radius = chm.ncol()/8;
  
  IntegerMatrix isTop(chm.nrow(), chm.ncol());
  for(int i = 0; i < chm.nrow(); i++)
    for(int j = 0; j < chm.ncol(); j++)
      isTop(i, j) = 1;
  
  for(int i = 0; i < chm.nrow(); i++)
    for(int j = 0; j < chm.ncol(); j++)
    {
      int xmin = i - radius >= 0 ? i - radius : 0;
      int xmax = i + radius < chm.nrow() ? i + radius : chm.nrow() - 1;
      int ymin = j - radius >= 0 ? j - radius : 0;
      int ymax = j + radius < chm.ncol() ? j + radius : chm.ncol() - 1;
      for(int x = xmin; x <= xmax; x++)
        for(int y = ymin; y <= ymax; y++)
        {
          if(chm(x,y) > chm(i, j)&&isInCricle(x,y,i,j,radius)) isTop(i, j) = 0;
        }
    }
  return isTop;
}

