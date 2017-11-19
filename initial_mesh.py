#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 21:04:00 2017

@author: park-wanbae
"""

import numpy as np

def initial_mesh(minvalue, maxvalue, num, coupon, barrier):
    
    '''
    tau = 0 시점의 mesh를 만들어주는 함수
    가로축: x축
    세로축: y축
    
    ===Input===
    minvalue: 표준화된 최소값
    maxvalue: 표준화된 최대값
    num: mesh를 쪼개는 개수
    coupon: 시간 순서대로 상환시 지급하는 쿠폰(ex: [0.025, 0.05, 0.075, 0.1, 0.125, 0.15])
    barrier: knock-in 배리어
    
    변수 coupon과 barrier는 class를 만들 때 멤버 변수화될 것임
    '''
    
    price_range = np.linspace(minvalue, maxvalue, num)
    x, y = np.meshgrid(price_range, price_range)    #(x와 y의 (num * num) matrix를 만듬)
    mesh = np.where(x > y, y, x)                    #x와 y중 mininum을 component로 갖는 행렬
    mesh = np.where(mesh > 100 * barrier, 100 * (1 + coupon[-1]), mesh)     #barrier보다 크면 쿠폰 지급, 아닌 경우 원금 손실
    
    return mesh

if __name__ == '__main__':
    minvalue = 0
    maxvalue = 300
    num = 400
    coupon = np.array([0.025, 0.05, 0.075, 0.1, 0.125, 0.15])
    barrier = 0.65
    
    x = initial_mesh(minvalue, maxvalue, num, coupon, barrier)