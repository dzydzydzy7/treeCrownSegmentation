#include <Rcpp.h>
using namespace Rcpp;

// [[Rcpp::export]]
IntegerMatrix part2one(IntegerMatrix seeds, IntegerMatrix part, NumericMatrix chm,  int x, int y) {
  int radius = part.nrow()/2;
  int center_id = part(radius,radius);
  int seed = seeds(x, y);
  
  int count = 0;
  double maxn = -999;
  double minn = 0x3f3f3f;
  
  for(int i = 0; i < chm.nrow(); i++)
  {
    for(int j = 0; j < chm.ncol(); j++)
    {
      if(chm(i, j) > maxn) maxn = chm(i, j);
      if(chm(i, j) < minn) minn = chm(i, j);
    }
  }
  
  double thre;
  thre = minn + (maxn - minn) * 0.2;
  
  for(int i = 0; i < part.nrow(); i++)
  {
    for(int j = 0; j < part.ncol(); j++)
    {
      if(part(i,j) == center_id && chm(i, j) >= thre)
        //if(seeds(i + x - radius, j + y - radius) == 0)
          count++;
    }
  }
  
  if(count >= 700)
  {
    for(int i = 0; i < part.nrow(); i++)
    {
      for(int j = 0; j < part.ncol(); j++)
      {
        if(part(i,j) == center_id && chm(i, j) >= thre)
          //if(seeds(i + x - radius, j + y - radius) == 0)
          seeds(i + x - radius, j + y - radius) = seed;
      }
    }
  }
  
  return seeds;
}

