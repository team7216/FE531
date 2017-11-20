# -*- coding: utf-8 -*-
###############################################################################
# KAIST 금융수치해석 팀 프로젝트
# 팀원 : 김용덕, 김정운, 박완배                                        
# Title : Class Package for 박씨와 두 김씨네 팀
###############################################################################

import pandas as pd
import numpy as np

#%%
class Parameters:
    '''
    parameters 추정을 위한 함수를 모아 놓은 클래스
    '''
    def __init__(self):
        pass

    def vol_interpolate(self, voldata, minN, maxN, ds, dt):
        '''
        voldata: 블룸버그에서 손크롤링한 엑셀 파일
        minN: 가격 변화의 미니멈
        maxN: 가격 변화의 맥시멈
        ds: 가격 변화의 간격
        dt: 시간 변화의 간격. 시간의 첫 시작점과 끝나는 지점은 투자설명서에 있는 날짜로 함수 안에 basedate과 matdate이라고 집어넣어둠
        
        결과는 2d, 넘파이 어레이로 나옴, 컬럼이 가격, 인덱스가 시간
        '''
        voldata['date'] = np.array(voldata['date'],dtype = 'datetime64')
        voldata = voldata.set_index('date')
        
        xp = list(voldata.columns.values*100)
        ds_list = list(np.linspace(minN, maxN, ds))
        
        desired = np.array([[np.nan]*(ds)]*(dt))
        v_desired = ds_list
        v_mid = np.array([[np.nan]*(ds)]*(len(voldata)))
        basedate = np.datetime64('2017-11-24')
        matdate = np.datetime64('2020-11-23')
        dt_list = list(np.linspace(0, (np.datetime64(matdate,'D') - np.datetime64(basedate,'D')).astype(int) , dt))
        datesto_int_list = []
        
        for d in voldata.index:
            datesto_int_list.append((np.datetime64(d,'D') - np.datetime64(basedate,'D')).astype(int))
        
        for i in range(0,len(voldata)):
            fp = list(voldata.iloc[i].values)
            v_mid[i] = np.interp(v_desired, xp, fp)
        
        xp = datesto_int_list
        for i in range(0,len(v_mid.T)):
            fp = list(v_mid[:,i])
            desired[:,i] = np.interp(dt_list, xp, fp)
        
        return desired

    def BM_process(self):
        pass


#%%
class OSM_Pricing:
    '''
    Operating Splitting Method를 사용하기 위한 함수를 모아 놓은 클래스
    '''
    def __init__(self):
        pass
    
    def initial_mesh(self, minvalue, maxvalue, num, coupon, barrier):      
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
    
    def u_mesh(self):
        pass
    

#%%
class ADI_Pricing:
    '''
    ADI를 사용하기 위한 함수를 모아 놓은 클래스
    '''
    def __init__(self):
        pass

    def initial_mesh(minvalue, maxvalue, num, coupon, barrier):
        pass

    def u_mesh(self):
        pass


#%% 
class Analyzer:
    '''
    계산된 ELS price를 분석해보는데 필요한 함수들을 모아 놓은 클래스
    '''
    def __init__(self):
        pass
    
    def graphing_3D(self):
        pass
