
import numpy as np
import uproot
import h5py
#import pandas as pd 


def TOFToEnergy(tof, x, m, c):
    return m * (1 / np.sqrt(1 - x * x / c / c / tof / tof) - 1) 
def EnergyToTOF(energy, x, m,c):
    return x /c/np.sqrt(1-(m*m/(energy + m)/(energy + m )))
def XsecToTs(xsec, num_density):
    ts = np.exp(- num_density * xsec)
    return ts
def get_data(file, detector):
    data = file[detector + ';1']
    tflash = data['tflash'].array(library="np")
    tof = data['tof'].array(library="np")
    detn = data['detn'].array(library="np")
    BN = data['BunchNumber'].array(library="np")
    PI = data['PulseIntensity'].array(library="np")

    amp = data['amp'].array(library="np")
    area = data['area'].array(library="np")
    time = data['time'].array(library = "np")
    #norm = PI[0]
    #for i in range(1, len(PI)):
    #    if BN[i] != BN[i - 1]:
    #        norm += PI[i]
    return tflash, tof, detn, amp, BN,PI,area,time


def compress(run_number):
    run_number= str(run_number)
    f = h5py.File('/home/hongc/NXSection/MArEX_Analysis/data/h5'+run_number+'.h5','w')
    file= uproot.open("/Volumes/HC/data/run" + run_number + ".root")
    key=file.keys()
    if "PTBC;1" in key:
        h5_PTBC=f.create_group('PTBC')
        tflash_PTBC, tof_PTBC, detn_PTBC, amp_PTBC, BN_PTBC, PI_PTBC,area_PTBC,time_PTBC = get_data(file, 'PTBC')
        h5_PTBC.create_dataset('tflash',data=tflash_PTBC)
        h5_PTBC.create_dataset('tof',data=tof_PTBC)
        h5_PTBC.create_dataset('detn',data=detn_PTBC)
        h5_PTBC.create_dataset('amp',data=amp_PTBC)
        h5_PTBC.create_dataset('BunchNumber',data=BN_PTBC)
        h5_PTBC.create_dataset('PulseIntensity',data=PI_PTBC)
        h5_PTBC.create_dataset('area',data=area_PTBC)
        h5_PTBC.create_dataset('time',data=time_PTBC)

        #print(tof_PTBC) 
    if "FIMG;1" in key:
        h5_FIMG=f.create_group('FIMG')
        tflash_FIMG, tof_FIMG, detn_FIMG, amp_FIMG, BN_FIMG, PI_FIMG,area_FIMG,time_FIMG = get_data(file, 'FIMG')
        h5_FIMG.create_dataset('tflash',data=tflash_FIMG)
        h5_FIMG.create_dataset('tof',data=tof_FIMG)
        h5_FIMG.create_dataset('detn',data=detn_FIMG)
        h5_FIMG.create_dataset('amp',data=amp_FIMG)
        h5_FIMG.create_dataset('BunchNumber',data=BN_FIMG)
        h5_FIMG.create_dataset('PulseIntensity',data=PI_FIMG)
        h5_FIMG.create_dataset('area',data=area_FIMG)
        h5_FIMG.create_dataset('time',data=time_FIMG)

    if "PKUP;1" in key:
        h5_PKUP=f.create_group('PKUP')
        data = file[ "PKUP;1"]
        tflash_PKUP= data['tflash'].array(library='np')
        BN_PKUP = data['BunchNumber'].array(library = 'np')
        h5_PKUP.create_dataset('tflash',data=tflash_PKUP)
        h5_PKUP.create_dataset('BunchNumber',data= BN_PKUP)

    f.close()


def read_h5(file,detector):
    tof=file[detector]['tof'][:]
    tflash=file[detector]['tflash'][:]
    amp = file[detector]['amp'][:]
    detn = file[detector]['detn'][:]
    BN = file[detector]['BunchNumber'][:]
    PI = file[detector]['PulseIntensity'][:]
    time = file[detector]['time'][:]
    tflash_PKUP = file['PKUP']['tflash'][:]
    BN_PKUP = file['PKUP']['BunchNumber'][:]
    BN_tpkup_map = dict(zip(BN_PKUP,tflash_PKUP))
    norm = PI[0]
    for i in range(1, len(PI)):
        if BN[i] != BN[i - 1]:
            norm += PI[i]
    return tof ,tflash, amp, detn,norm,BN_tpkup_map,BN,PI,time 

def process_data(run_numbers, detector, output):
    tflash = np.array([])
    tof = np.array([])
    detn = np.array([])
    amp = np.array([])
    BN = np.array([])
    PI = np.array([])
    time = np.array([])
    BN_tPKUP_map={}
    norm = 0
    L = 182.24
    if detector == 'PTBC':
        L == 182.65 - 0.41 # in m 182.24
    if detector == 'FIMG':
        L == 183.5 - 0.41  # in m   
    for i in run_numbers:

        f_i = h5py.File('data/'+str(i)+'.h5','r')
        try:
            tof_i, tflash_i, amp_i, detn_i,norm_i,BN_tPKUP_map_i,BN_i ,PI_i,time_i= read_h5(f_i, detector)
        except:
            print( 'h5' + str(i)+'.h5 do not have data of ' + detector +'.')
            continue
        #print(tof_i)
        tflash = np.append(tflash, tflash_i)
        tof = np.append(tof, tof_i)
        amp = np.append(amp, amp_i)
        detn = np.append(detn,detn_i)
        BN = np.append(BN,BN_i)
        PI = np.append(PI, PI_i)
        time = np.append(time, time_i)
        BN_tPKUP_map.update(BN_tPKUP_map_i) 
        norm += norm_i
    real_tof=np.zeros(len(tof))
    for i in range(len(real_tof)):    
        real_tof[i] = tof[i] - BN_tPKUP_map[BN[i]] + 660 + (L * 1e9/ 299792458) # in ns 
    
    #en = TOFToEnergy(real_tof / 1e9, L, 939.56542, 299792458)*1e6 # in eV
    f = h5py.File('temp_data/'+detector+'_'+output+'.h5', "w")
    data=f.create_group(detector)
    #data.create_dataset("energy", data=en)
    data.create_dataset("amp", data=amp)
    data.create_dataset("detn",data=detn)
    data.create_dataset("PI",data = PI)
    data.create_dataset("time",data = time)
    data.create_dataset('tof',data=real_tof)
    data.create_dataset("norm", data=[norm])
    f.close()
###########################
def FindDecadePower(e):
    decadePower=0
    value = e
    if e == 1:
        return decadePower
    if e > 1 :
        while value > 1:
            value /=10
            decadePower +=1
    if e < 1:
        while value < 1:
            value *= 10
            decadePower -=1        
    return decadePower

def bin_edge(detector):
    bins_per_decade = 1000.0
    num_decades_tof = 5.0
    num_bins_tof = bins_per_decade * num_decades_tof
    bin_edge_tof = []
    step = 1.0/bins_per_decade  
    for i in range(int(num_bins_tof +1)):
    #    base = 10
        exponent = (step * i) + 3
        bin_edge_tof.append(pow(10,exponent))

    #########################################    
    if detector == 'PTBC':
        L = 182.65 - 0.41 # in m
    if detector == 'FIMG':
        L = 183.5 - 0.41  # in m   
    tof_min = 1e3 # in ns
    tof_max = 1e8  # in ns 
    en_min = TOFToEnergy(tof_max/1e9, L, 939.56542*1e6 , 299792458) # in eV
    en_max = TOFToEnergy(tof_min/1e9, L, 939.56542*1e6  , 299792458)
    
    power_min = FindDecadePower(en_min)
    power_max = FindDecadePower(en_max)
    
    num_decades_en = power_max - power_min
    num_bins_en = num_decades_en * bins_per_decade
    bin_edge_en=[] 
    for i in range(int(num_bins_en +1)):
    #    base = 10
        exponent = (step * i) + power_min
        bin_edge_en.append(pow(10,exponent))
    print(power_max)
    print(power_min)    
    return num_bins_tof, bin_edge_tof, num_bins_en, bin_edge_en    
#_,bin_edge_tof,_,bin_edge_en=bin_edge('PTBC')
#print(bin_edge_en)
 
def read_endf(file):
    f=open(file)
#    print('Read ' +  file + '.')
    energy = []
    xsec = []

    for line in f:
        energy.append(float(line[3:14])*1e6) # in eV
    #xsec.append(float(line[16:27]))
        xsec.append(float(line[20:27]))
   
    energy = np.array(energy)

    xsec = np.array(xsec)
    return energy, xsec 