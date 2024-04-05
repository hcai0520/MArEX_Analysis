import numpy as np
import sys
sys.path.append('src/..')
from src.process_data import *

def cut_line(x1,y1,x2,y2,x3):
    return ((y2-y1)*(x3-x1)/(x2 - x1)+ y1)
#cut_D1_FIMG: 10000, 2350; 100000, 500
#cut_D2_FIMG: 10000, 3000; 100000, 500
    
#cut_D1_PTBC: 700, 10000; 20000, 10000; 20000, 5000
#cut_D2_PTBC: 700, 8000; 20000, 8000; 20000, 5000
#cut_D3_PTBC: 700, 7000; 2000, 7000; 2000, 4500
#cut_D4_PTBC: 700, 10000; 2000, 10000; 2000, 5000
#cut_D5_PTBC: 700, 10000; 2000, 10000; 2000, 8000;20000, 8000;20000, 4500
#cut_D6_PTBC: 700, 9000; 2000, 9000; 2000, 6000;20000, 6000;20000, 4500
#cut_D7_PTBC: 700, 8000; 2000, 8000; 2000, 4000;20000, 4000;20000, 3500
def PTBC_cut(detn):
    if detn == 1:
        n=2
        t=[[0]*2 for _ in range(n)]
        a=[[0]*2 for _ in range(n)]
        t[0][0] = 700.0
        a[0][0] = 10000.0

        t[0][1] = 20000.0
        a[0][1] = 10000.0

        t[1][0] = 20000.0
        a[1][0] = 5000.0

        t[1][1] = 1e8
        a[1][1] = 5000.0
    if detn == 2:
        n=4
        t=[[0]*2 for _ in range(n)]
        a=[[0]*2 for _ in range(n)]
        t[0][0] = 800.0
        a[0][0] = 8000.0

        t[0][1] = 2600.0
        a[0][1] = 8000.0

 
        t[1][0] = 2600.0
        a[1][0] = 9500.0

        t[1][1] = 2800.0
        a[1][1] = 9500.0

    
        t[2][0] = 2800.0
        a[2][0] = 8000.0

        t[2][1] = 5000.0
        a[2][1] = 8000.0

    
        t[3][0] = 5000.0
        a[3][0] = 4000.0 

        t[3][1] = 1e8
        a[3][1] = 4000.0
    if detn == 3:
        n=2
        t=[[0]*2 for _ in range(n)]
        a=[[0]*2 for _ in range(n)]
        t[0][0] = 800.0
        a[0][0] = 5000.0

        t[0][1] = 3000.0
        a[0][1] = 5000.0

        t[1][0] = 3000.0
        a[1][0] = 3500.0

        t[1][1] = 1e8
        a[1][1] = 3500.0
    if detn == 4:
        n=2
        t=[[0]*2 for _ in range(n)]
        a=[[0]*2 for _ in range(n)]
        t[0][0] = 800.0
        a[0][0] = 6000.0

        t[0][1] = 2000.0
        a[0][1] = 6000.0

        t[1][0] = 2000.0
        a[1][0] = 3500.0

        t[1][1] = 1e8
        a[1][1] = 3500.0
    if detn ==5:
        n=2
        t=[[0]*2 for _ in range(n)]
        a=[[0]*2 for _ in range(n)]
        t[0][0] = 800.0
        a[0][0] = 7000.0

        t[0][1] = 7000.0
        a[0][1] = 7000.0

        t[1][0] = 7000.0
        a[1][0] = 3500.0

        t[1][1] = 1e8
        a[1][1] = 3500.0    

    
    if detn ==6:
        n=2
        t=[[0]*2 for _ in range(n)]
        a=[[0]*2 for _ in range(n)]
        t[0][0] = 800.0
        a[0][0] = 6000.0

        t[0][1] = 6000.0
        a[0][1] = 6000.0

        t[1][0] = 6000.0
        a[1][0] = 4000.0

        t[1][1] = 1e8
        a[1][1] = 4000.0

        
    if detn ==7:
        n=2
        t=[[0]*2 for _ in range(n)]
        a=[[0]*2 for _ in range(n)]
        t[0][0] = 800.0
        a[0][0] = 4000.0

        t[0][1] = 4000.0
        a[0][1] = 4000.0

        t[1][0] = 4000.0
        a[1][0] = 3000.0

        t[1][1] = 1e8
        a[1][1] = 3000.0

    return t,a,n
def para_cut():
    n=2
    t=[[0]*2 for _ in range(n)]
    a=[[0]*2 for _ in range(n)]
    t[0][0] = 800.0
    a[0][0] = 5000.0

    t[0][1] = 3000.0
    a[0][1] = 5000.0

    t[1][0] = 3000.0
    a[1][0] = 4000.0

    t[1][1] = 1e8
    a[1][1] = 4000.0
    return t,a,n 

def FIMG_cut(detn):
    if detn == 1 :
        n=5
        t=[[0]*2 for _ in range(n)]
        a=[[0]*2 for _ in range(n)]
        t[0][0] = 7e3
        a[0][0] = 4600.
        t[0][1] = 1e4
        a[0][1] = 3000.

        t[1][0] = 1e4
        a[1][0] = 3000.
        t[1][1] = 2e4
        a[1][1] = 1525.

        t[2][0] = 2e4
        a[2][0] = 1525.
        t[2][1] = 45090.
        a[2][1] = 1525.

        t[3][0] = 45090.
        a[3][0] = 1525.
        t[3][1] = 1e5
        a[3][1] = 500.

        t[4][0] = 1e5
        a[4][0] = 500.
        t[4][1] = 1e8
        a[4][1] = 500.
    if detn == 2 :
        n=5
        t=[[0]*2 for _ in range(n)]
        a=[[0]*2 for _ in range(n)]
        t[0][0] = 7e3
        a[0][0] = 4000.
        t[0][1] = 8e3
        a[0][1] = 3200.

        t[1][0] = 8e3
        a[1][0] = 3200.
        t[1][1] = 2e4
        a[1][1] = 2250.

        t[2][0] = 2e4
        a[2][0] = 2250.
        t[2][1] = 31800.
        a[2][1] = 2250.

        t[3][0] = 31800.
        a[3][0] = 2250.
        t[3][1] = 7e4
        a[3][1] = 500.

        t[4][0] = 7e4
        a[4][0] = 500.
        t[4][1] = 1e8
        a[4][1] = 500.
        
    return t, a ,n 

def data_cut(tof,amp,detector,detn,PI):
    tof_select= np.array([])
    en_select= np.array([])
    if detector == 'PTBC':
        L = 182.65 - 0.41 # in m
        amp_para = amp[PI <= 6e12]
        tof_para = tof[PI <= 6e12]
        tof_para_select = data_cut_para(tof_para,amp_para)
        for j in range(2,8):
            t,a,n = PTBC_cut(j)
            for i in range(n):
                tof_i = tof[ (tof > t[i][0]) & (tof < t[i][1]) & (amp > cut_line(t[i][0],a[i][0],t[i][1],a[i][1],tof))& (detn == j)&(PI > 6e12)]
                tof_select = np.append(tof_select, tof_i) # in ns
        tof_select = np.append(tof_select, tof_para_select)   
        en_select = TOFToEnergy(tof_select / 1e9, L, 939.56542, 299792458)*1e6 # in eV

    if detector == 'FIMG':
        L = 183.5 - 0.41  # in m
        for j in range(1,3):    
            t,a,n = FIMG_cut(j)
            for i in range(n):
                tof_i = tof[ (tof > t[i][0]) & (tof < t[i][1]) & (amp > cut_line(t[i][0],a[i][0],t[i][1],a[i][1],tof))& (detn == j)]
            #print(len(tof_i))
                tof_select = np.append(tof_select, tof_i) # in ns
           
        en_select = TOFToEnergy(tof_select / 1e9, L, 939.56542, 299792458)*1e6 # in eV   
       
    return tof_select, en_select
def data_cut_para(tof,amp):
    tof_select= np.array([])
    t,a,n = para_cut()
    for i in range(n):
        tof_i = tof[ (tof > t[i][0]) & (tof < t[i][1]) & (amp > cut_line(t[i][0],a[i][0],t[i][1],a[i][1],tof))]
        tof_select = np.append(tof_select, tof_i)
    return tof_select


def get_cut(input,detector):
    In = h5py.File(input, "r")

    amp = In[detector]['amp'][:]
    tof=In[detector]['tof'][:]
    #en_In = input_in[detector]['energy'][:]
    detn = In[detector]['detn'][:]
    PI = In[detector]['PI'][:]
    norm = In[detector]['norm'][0]
    #print('read ' + str(input))
   
    tof_In_select,en_In_select = data_cut(tof,amp,detector, detn,PI)
    
    return tof_In_select,en_In_select,norm
