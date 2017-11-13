# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 20:31:01 2017

@author: woony
"""

import pandas as pd
import numpy as np

#%%
class Project: #아직 다 안 짬
    def __init__(self):
        pass
    
    def payoff(self,S1,S2,K):
        if S1 > K:
            return S1-K
        else:
            return 0
    
    def cashornothing_callBC(self, S, K, sigma, r, tau, x, fg='u0',D0=0):
#        k1 = r / ((sigma**2)/2)
        k2 = (r-D0) / ((sigma**2)/2)
        payoff = self.payoff(S,K)
        if fg == 'g':
            return payoff/K * (np.exp( (k2-1)*x/2 + tau/4*(k2-1)**2 ))
        elif fg == 'f':
            return 0
        elif fg == 'u0':
            if x < 0:
                return 0
            elif x >= 0:
                return payoff/K * np.exp( (k2-1)*x/2 )
            else:
                return 'wrong value encountered'
        else:
            return 'wrong direction encountered'
    
    def EFDM(self, S, K, sigma, r, dx, dt, M, N):
        alpha = dt/(dx**2)
        
        Nplus = N
        Nminus = -N
        xrange = list(np.arange(Nminus,Nplus+1,1))
        taurange = list(np.arange(0,M+1,1))
        v_result = pd.DataFrame(index = xrange, columns = taurange)

        for m in taurange:
            v_result.ix[Nminus,m] = self.cashornothing_callBC(S, K, sigma, r, m*dt, Nminus*dx, 'f')
            v_result.ix[Nplus,m] = self.cashornothing_callBC(S, K, sigma, r, m*dt, Nplus*dx, 'g')
        
        for n in xrange:
            v_result.ix[n,0] = self.cashornothing_callBC(S, K, sigma, r, 0, n*dx, 'u0')

        for m in taurange:
            for n in xrange:
                print(n) #아직 다 안 짬

        return v_result
    
pj = Project()

#%%