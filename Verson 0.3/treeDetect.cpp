#include <Rcpp.h>
using namespace Rcpp;

// [[Rcpp::export]]
IntegerMatrix treeDetect(NumericMatrix chm) {
  int radius = chm.ncol()/3;
  int remove = radius - 1;
  
  bool isTop[50][50];
  for(int i = 0; i < 50; i++)
    for(int j = 0; j < 50; j++)
      isTop[i][j] = true;
  
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
          if(chm(x,y) > chm(i, j)) isTop[i][j] = false;
        }
    }
  
  for(int i = 0; i < chm.nrow(); i++)
    for(int j = 0; j < chm.ncol(); j++)
    {
      int xmin = i - remove >= 0 ? i - remove : 0;
      int xmax = i + remove < chm.nrow() ? i + remove : chm.nrow() - 1;
      int ymin = j - remove >= 0 ? j - remove : 0;
      int ymax = j + remove < chm.ncol() ? j + remove : chm.ncol() - 1;
      if(isTop[i][j]){
        for(int x = xmin; x <= xmax; x++)
          for(int y = ymin; y <= ymax; y++)
          {
            isTop[x][y] = false;
          }
        isTop[i][j] = true;
      }
    }

  int count = 0;
  for(int i = 0; i < chm.nrow(); i++)
    for(int j = 0; j < chm.ncol(); j++)
    {
      if(isTop[i][j])count++;
    }
  
  //µÃµ½Ê÷¶¥µÄx, y
  IntegerMatrix topPoint(10, 2);
  int n = 0;
  for(int i = 0; i < chm.nrow(); i++)
    for(int j = 0; j < chm.ncol(); j++)
    {
      if(isTop[i][j])
      {
        topPoint(n, 0) = i;
        topPoint(n, 1) = j;
      }
    }
  return topPoint;
}


