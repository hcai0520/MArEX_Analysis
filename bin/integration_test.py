import uproot
import numpy as np
import argparse
import yaml
import matplotlib.pyplot as plt
import sys
sys.path.append('src/..')
from src.process_data import get_data
from src.process_data import energy



parser = argparse.ArgumentParser()
parser.add_argument("infile", type=argparse.FileType("r"), help="input file with list of run numbers")
parser.add_argument('set',type=str,help= 'experiment set up')
parser.add_argument("config",type=str, help="configuration of input file")
parser.add_argument("detector", type=str, help="detector")
parser.add_argument("--cut",type=str, help="cut of energy and amplitude ")
args = parser.parse_args()

tflash = np.array([])
tof = np.array([])
amp = np.array([])
norm = 0
L = 184.5
if args.detector == "C6D6":
    L += 6.89
#for i in args.config[args.set]['runlist']:
for i in args.infile:
    tflash_i, tof_i, amp_i, norm_i = get_data(i, args.detector)
    tflash = np.append(tflash, tflash_i)
    tof = np.append(tof, tof_i)
    amp = np.append(amp, amp_i)
    norm += norm_i
real_tof = tof - tflash + L / 299792458 * 1e9
en = energy(real_tof / 1e9, L, 939.56542, 299792458) * 1e6


with open(args.config,'r') as cfg:
    config=yaml.safe_load(cfg)

bins_en=100
bins_tof=100    

if args.cut:
    with open(args.cut,'r') as cuts:
        cut=yaml.safe_load(cuts)

    en_select = en[(en > cut['roi_cut']['e_min']) & (en < cut['roi_cut']['e_max']) & (amp > cut['alpha_cut']['amp'])]
    tof_select = real_tof[(en > cut['roi_cut']['e_min']) & (en < cut['roi_cut']['e_max']) & (amp > cut['alpha_cut']['amp'])]
    hist_en,bins_en,_=plt.hist(en_select,bins_en)
    hist_tof,bins_tof,_ = plt.hist(tof_select,bins_tof)
else:
    hist_en,bins_en,_=plt.hist(en,bins_en)
    hist_tof,bins_tof,_ = plt.hist(real_tof,bins_tof) 

    np.savetxt('TOF_'+str(config[args.set]['data']) +'_'+ str(config[args.set]['target']) + '_' + str(config[args.set]['filter'] )+'.txt',np.array(hist_tof))
    np.savetxt('En_'+str(config[args.set]['data']) +'_'+ str(config[args.set]['target']) + '_' + str(config[args.set]['filter'] )+'.txt',np.array(hist_en))

en_record= open('integration_record/En_'+str(config[args.set]['data']) +'_'+ str(config[args.set]['target']) + '_' + str(config[args.set]['filter'] )+'.txt')
tof_record=open('integration_record/TOF_'+str(config[args.set]['data']) +'_'+ str(config[args.set]['target']) + '_' + str(config[args.set]['filter'] )+'.txt')

line_en = en_record.readlines()
line_tof = tof_record.readlines()
match_en = True
match_tof = True
for i in range(len(line_en)):
    if int(float(line_en[i])) != hist_en[i]:
        match_en = False
        print(line_en[i])
        print( str(i) + 'th bin not match')
if match_en == True:
    print('energy data matched') 

for i in range(len(line_tof)):
    if int(float(line_tof[i])) != hist_tof[i]:
        match_tof = False
        print( str(i) + 'th bin not match')
if match_tof == True:
    print('tof data matched')