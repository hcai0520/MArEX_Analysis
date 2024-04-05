import numpy as np
import sys
sys.path.append('src/..')
from src.process_data import *
from src.transmission import *
# n_Bi_1cm = (1.0 /*cm*/) * (9.78 /*g/cm3*/) * (6.02214076e23 /*atoms/mole*/) * (1e-24 /*cm2/barn*/) / (208.9804 /*g/mole*/);

   
def chi_sq(L,t,xsec,energy,x_tof,tr,tr_err,number_density, thickness):       
    num_density = number_density *t/thickness
    ts = XsecToTs(xsec, num_density)[::-1]
    tof = EnergyToTOF(energy/1e6, L , 939.56542, 299792458)*1e9 # in ns
    tof = tof[::-1] 
#    en = TOFToEnergy(tof, L, 939.56542, 299792458)*1e6 
    y_ts = np.interp(x_tof, tof, ts)
    return  np.sum(((y_ts - tr) / tr_err) ** 2)