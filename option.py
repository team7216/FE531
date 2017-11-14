#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 20:43:07 2017

@author: park-wanbae
"""
import datetime
import scipy.stats as sst
import numpy as np
from dateutil import relativedelta as rdt

class MarketVariable:
    def __init__(self, spot, r, q, sigma):
        self.spot = spot
        self.r = r
        self.q = q
        self.sigma = sigma

class PlainVanillaOption:
    def __init__(self, strike, maturity, optionType):
        self.strike = strike
        self.maturity = maturity
        self.t = (maturity - datetime.date.today()).days / 365.0
        if optionType.lower() == 'call':
            self.optionType = 1
        else:
            self.optionType = -1
    
    def setMarketVariable(self, mktVar):
        self.mktVar = mktVar
        
        #(tau, x) - space에서의 변수 결정
        self.k1 = mktVar.r / mktVar.sigma ** 2 * 2
        self.k2 = (mktVar.r - mktVar.q) / mktVar.sigma ** 2 * 2
        self.x = np.log(mktVar.spot / self.strike)
        self.tau = self.t * (mktVar.sigma ** 2) * 0.5

    def bsprice(self):
        d1 = (np.log(self.mktVar.spot / self.strike) + \
              (self.mktVar.r + 0.5 * self.mktVar.sigma ** 2) * self.t) / \
              (self.mktVar.sigma * np.sqrt(self.t))
        d2 = d1 - self.mktVar.sigma * np.sqrt(self.t)
        return self.optionType * (self.mktVar.spot * \
                                  np.exp(-self.mktVar.q * self.t) * \
                                  sst.norm.cdf(self.optionType * d1) - \
                                  self.strike * np.exp(-self.mktVar.r * self.t) * \
                                  sst.norm.cdf(self.optionType * d2))
    def payoff(self, spot):
        return np.where(self.optionType * (spot - self.strike) > 0,
                        self.optionType * (spot - self.strike), 0)
    
    def payoff_tr(self, x, tau):  #Transformed Payoff
        return np.exp(0.5 * (self.k2 - 1) * x + (0.25 * (self.k2 - 1) ** 2 + self.k1) * tau) * \
                        np.where(self.optionType * (np.exp(x) - 1) > 0,
                        self.optionType * (np.exp(x) - 1), 0)
    
    def efdmprice(self, m, n, dx):
        mesh = np.zeros([n, m])
        
        #x의 범위를 설정(x - a1*dx, ... , x , ... x + a2*dx)
        a1, a2 = np.floor((n - 1) / 2), np.ceil((n - 1) / 2)
        dx_range = np.concatenate([np.arange(-a1, 0, 1), np.arange(0, a2 + 1, 1)])
        x_range = dx_range * dx + self.x
        xmax = np.max(x_range)
        xmin = np.min(x_range)
        x_idx = np.where(x_range == self.x)[0][0]   # index of current underlying price
        spot_range = self.strike * np.exp(x_range)  # spot price range
        
        dt = self.tau / (m - 1)
        t_range = np.arange(0, self.tau + dt, dt)
        
        alpha = dt / (dx ** 2)
        
        #Alpha should not be larger than 0.5
        if (alpha > 0.5):
            raise(Warning)('alpha is larger than 0.5')
        
        #Boundary Setting
        mesh[:,0] = self.payoff_tr(x_range, 0)
        if self.optionType == 1:
            mesh[-1,1:] = np.exp(0.5 * (self.k2 + 1) * xmax + \
                                0.25 * (self.k2 + 1) ** 2 * t_range[1:])   
        else:
            mesh[0,1:] = np.exp(0.5 * (self.k2 - 1) * xmin + \
                                0.25 * (self.k2 - 1) ** 2 * t_range[1:])
        
        # Solve PDE by recursion
        for j in range(1, m):
            for i in range(1, n-1):
                mesh[i][j] = mesh[i][j-1] + alpha * (mesh[i+1][j-1] - 2*mesh[i][j-1] + mesh[i-1][j-1])
        
        #변환했던 변수를 다시 돌려놓음
        price = mesh[:,-1] * self.strike * np.exp(-0.5 * (self.k2 - 1) * x_range - \
                                (0.25 * (self.k2 - 1) ** 2 + self.k1) * self.tau)
        return spot_range, spot_range[x_idx], price, price[x_idx], alpha
        
        
        
if __name__ == '__main__':
    mktVar = MarketVariable(10, 0.05, 0, 0.2)
    put = PlainVanillaOption(10, datetime.date.today() + rdt.relativedelta(months = 6), 'put')
    put.setMarketVariable(mktVar)
    fdmprice = put.efdmprice(300, 400, 0.01)
    print('Spot: %.2f' %fdmprice[1])
    print('EFDM Price: %.4f' %fdmprice[3])
    print('Black-Scholes Price: %.4f' %put.bsprice())
    print('alpha: %.4f' %fdmprice[4])