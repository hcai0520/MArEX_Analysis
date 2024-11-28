#from src.process_data import *
import h5py
import uproot
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
    f = h5py.File(run_number+'.h5','w')
    file= uproot.open("/Volumes/HC/data/run" + run_number + ".root")
#    file= uproot.open("run" + run_number + ".root")

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

import yaml
filename= '../config/conditions.yml'
with open(filename) as f:
    config= yaml.safe_load(f)
c=config

for i in c['empty']['runlist']:
    compress(i)  
    print(str(i) + '.h5 created.') 
    if i == c['empty']['runlist'][-1]:
        print ('work done !!!')