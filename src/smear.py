import numpy as np
import sys
sys.path.append('src/..')
from src.process_data import *

def gaus(x,mu,sig):
    #return (1/np.sqrt(2* np.pi * sig**2))*np.exp(-((x -mu) ** 2)/2/sig**2)
    return np.exp(-((x - mu) ** 2) / 2 / sig ** 2) / np.sqrt(2 * np.pi * sig ** 2)

def smear_single(energy, xsec, mean_dL,sig_dL,en,L):
    tot = 0
    norm = 0
    #if detector == 'PTBC':
    tof = EnergyToTOF(en,L,939.56542*1e6,299792458)# en in eV ;tof in s 
    #if detector == 'FIMG':
    #    tof = EnergyToTOF(en,183.09,939.56542*1e6,299792458)# en in eV ;tof in s 

    energy_mean = TOFToEnergy(tof, L + mean_dL, 939.56542*1e6,299792458)
    energy_low = TOFToEnergy(tof, L + mean_dL - sig_dL, 939.56542*1e6,299792458)
    energy_high = TOFToEnergy(tof, L + mean_dL + sig_dL, 939.56542*1e6,299792458)
    diff = (energy_high - energy_low)/100
    cur = energy_low + diff/2
    for i in range(100):
        tot += np.interp(cur,energy,xsec)* gaus(cur, energy_mean, (energy_high - energy_low)/2)
        norm += gaus(cur, energy_mean, (energy_high - energy_low)/2) 
        cur += diff
    return tot/norm      

# in barn

def smear(energy, xsec, mean_dL,sig_dL, en_low,en_high, num, L):
    ret_energy = np.array([])
    ret_xsec = np.array([])
    diff = (en_high - en_low) / num
    cur = en_low
    for i in range(num):
        ret_xsec = np.append(ret_xsec, smear_single(energy, xsec, mean_dL, sig_dL, cur, L))
        ret_energy = np.append(ret_energy, cur)
        cur += diff
    return ret_energy, ret_xsec
