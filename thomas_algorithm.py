#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 16:18:59 2017

@author: park-wanbae
"""
import numpy as np
import copy
    
def tridiagonalSolver(a_, d_):
    #Deep copy
    a = copy.deepcopy(a_)
    d = copy.deepcopy(d_)
    
    #Tridiagonal Solver: Ax = d
    if len(a) != len(d):    
        raise IndexError("Dimension of A and d should be equal")
    
    for i in range(len(a) - 1):
        d[i+1] += (-a[i+1][i] / a[i][i]) * d[i]
        a[i+1] += (-a[i+1][i] / a[i][i]) * a[i]
        
    x = np.zeros(len(d))
    x[-1] = d[-1] / a[-1][-1]
    for i in range(len(a) - 2, -1, -1):
        x[i] = (d[i] - a[i][i+1] * x[i+1]) / a[i][i]
    
    return x

if __name__ == "__main__":
    a1 = np.array([[1.0, 1.0, 0.0, 0.0],
                   [2.0, 1.0, 3.0, 0.0],
                   [0.0, 1.0, 2.0, 1.0],
                   [0.0, 0.0, 1.0, 1.0]])
    d1 = np.array([3.0, 13, 12, 7])
    
    #Diagonal term과 양 옆의 term 차이가 크지 않은 경우
    a2 = np.array([[1.0000001, 1.0, 0.0 ,0.0],
                  [2.0000001, 2.0, 2.0000001, 0.0],
                  [0.0, 3.0000001, 3.0, 3.0000001],
                  [0.0, 0.0, 1.0000001, 1.0]])
    d2 = np.array([7.0000003, 26.000001, 48.000001, 52.0000006])
    
    x1 = tridiagonalSolver(a1, d1)
    print('-'*70)
    print("Solution of equation #1")
    print("x:", x1)
    y1 = np.dot(a1, x1)
    print("Ax:", y1)
    print('-'*70)
    
    # Not ideal solution
    print("Solution of equation #2")
    x2 = tridiagonalSolver(a2, d2)
    print("x:", x2)
    
    y2 = np.dot(a2, x2)
    print("Ax:", y2)
    print('-'*70)
    
