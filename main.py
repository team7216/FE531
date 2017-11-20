# -*- coding: utf-8 -*-
###############################################################################
# KAIST 금융수치해석 팀 프로젝트
# 팀원 : 김용덕, 김정운, 박완배                                        
# Title : Class Package for 박씨와 두 김씨네 팀
###############################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize']=(15,10)
import seaborn as sns
import time
import winsound
import ELS_Pricing_Pack
OSM = ELS_Pricing_Pack.OSM_Pricing()
Param = ELS_Pricing_Pack.Parameters()

#%%
minvalue = 0
maxvalue = 300
num = 400
coupon = np.array([0.025, 0.05, 0.075, 0.1, 0.125, 0.15])
barrier = 0.65

x = OSM.initial_mesh(minvalue, maxvalue, num, coupon, barrier)

#sns.heatmap(x)
#plt.xticks(rotation=90)
#plt.yticks(rotation=90)

#%%
dt = 300
HSCEI_voldata = pd.read_excel('loc_vol_HSCEI.xlsx')
HSCEI_loc_vol = Param.vol_interpolate(HSCEI_voldata, minvalue, maxvalue, num, 300)
EuroStoxx_voldata = pd.read_excel('loc_vol_EuroStoxx50.xlsx')
EuroStoxx_loc_vol = Param.vol_interpolate(EuroStoxx_voldata, minvalue, maxvalue, num, 300)
#아마 완배가 생각한 num과 제가 생각한 ds가 같은 거인 거 같아서 같은 값을 인풋으로 넣어줌

#sns.heatmap(HSCEI_loc_vol)
#sns.heatmap(EuroStoxx_loc_vol)