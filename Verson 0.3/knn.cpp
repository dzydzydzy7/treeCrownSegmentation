#include <Rcpp.h>
using namespace Rcpp;

#define START 20

// [[Rcpp::export]]
int knn(NumericMatrix treeTopMap, int x, int y) {
  int radius = START;
  int nw = START;
  int ne = START;
  int sw = START;
  int se = START;
  while(nw < 50)
  {
    int tops = 0;
    for(int i = x - nw; i < x; i++)
      for(int j = y - nw; j < y; j++)
      {
        if(treeTopMap(i,j)) tops++;
      }
    if(tops>=1) break;
    else nw += 5;
  }
  
  while(ne < 50)
  {
    int tops = 0;
    for(int i = x - ne; i < x; i++)
      for(int j = y; j < y + ne; j++)
      {
        if(treeTopMap(i,j)) tops++;
      }
      if(tops>=1) break;
      else ne += 5;
  }
  
  while(sw < 50)
  {
    int tops = 0;
    for(int i = x; i < x + sw; i++)
      for(int j = y - sw; j < y; j++)
      {
        if(treeTopMap(i,j)) tops++;
      }
      if(tops>=1) break;
      else sw += 5;
  }
  
  while(se < 50)
  {
    int tops = 0;
    for(int i = x; i < x + se; i++)
      for(int j = y; j < y + se; j++)
      {
        if(treeTopMap(i,j)) tops++;
      }
      if(tops>=1) break;
      else se += 5;
  }
  
  radius = nw;
  if(ne > radius) radius = ne;
  if(sw > radius) radius = sw;
  if(se > radius) radius = se;
  
  return radius;
}

