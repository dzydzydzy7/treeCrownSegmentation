#include <Rcpp.h>
using namespace Rcpp;

// [[Rcpp::export]]
IntegerMatrix detect_part2(IntegerMatrix isTop) {
  int radius = isTop.ncol()/8 - 1;
  for(int i = 0; i < isTop.nrow(); i++)
    for(int j = 0; j < isTop.ncol(); j++)
    {
      int xmin = i - radius >= 0 ? i - radius : 0;
      int xmax = i + radius < isTop.nrow() ? i + radius : isTop.nrow() - 1;
      int ymin = j - radius >= 0 ? j - radius : 0;
      int ymax = j + radius < isTop.ncol() ? j + radius : isTop.ncol() - 1;
      if(isTop(i, j) == 1){
        for(int x = xmin; x <= xmax; x++)
          for(int y = ymin; y <= ymax; y++)
          {
            isTop(x, y) = 0;
          }
        isTop(i, j) = 1;
      }
    }
  return isTop;
}

