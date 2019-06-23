#include <Rcpp.h>
using namespace Rcpp;

// [[Rcpp::export]]
NumericMatrix detect_part3(IntegerMatrix isTop, NumericMatrix chm) {
  int count = 0;
  for(int i = 0; i < isTop.nrow(); i++)
    for(int j = 0; j < isTop.ncol(); j++)
    {
      if(isTop(i, j) == 1) count++;
    }
  NumericMatrix tops(count, 3);
  int index = 0;
  for(int i = 0; i < isTop.nrow(); i++)
    for(int j = 0; j < isTop.ncol(); j++)
    {
      if(isTop(i, j)){
        double dj = j;
        double di = i;
        tops(index, 0) =dj / isTop.ncol();
        tops(index, 1) = 1 - di/isTop.nrow();
        tops(index, 2) =  chm(i, j);
        index++;
      }
    }
  return tops;
}

