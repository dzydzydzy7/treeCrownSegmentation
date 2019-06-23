#include <Rcpp.h>
using namespace Rcpp;

// [[Rcpp::export]]
IntegerMatrix part2one(IntegerMatrix seeds, IntegerMatrix part, int x, int y) {
  int radius = part.nrow()/2;
  int center_id = part(radius,radius);
  int seed = seeds(x, y);
  
  for(int i = 0; i < part.nrow(); i++)
  {
    for(int j = 0; j < part.ncol(); j++)
    {
      if(part(i,j) == center_id)
        //if(seeds(i + x - radius, j + y - radius) == 0)
          seeds(i + x - radius, j + y - radius) = seed;
    }
  }
  return seeds;
}

