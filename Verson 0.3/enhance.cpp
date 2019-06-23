#include <Rcpp.h>
#include <vector>
#include <algorithm>
using namespace Rcpp;
using namespace std;

// This is a simple example of exporting a C++ function to R. You can
// source this function into an R session using the Rcpp::sourceCpp 
// function (or via the Source button on the editor toolbar). Learn
// more about Rcpp at:
//
//   http://www.rcpp.org/
//   http://adv-r.had.co.nz/Rcpp.html
//   http://gallery.rcpp.org/
//

// [[Rcpp::export]]
NumericMatrix enhance(NumericMatrix x) {
  vector<double>points;
  for(int i = 0; i < x.nrow(); i++)
  {
    for(int j = 0; j < x.ncol(); j++)
    {
      points.push_back(x(i,j));
    }
  }
  sort(points.begin(), points.end());
  double s = points[x.nrow()*x.ncol()/2.0];
  for(int i = 0; i < x.nrow(); i++)
  {
    for(int j = 0; j < x.ncol(); j++)
    {
      if(x(i, j) >= s)x(i, j)+=1;
    }
  }
  return x;
}

