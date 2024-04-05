import argparse
import yaml
import h5py
import matplotlib.pyplot as plt
import sys
sys.path.append('src/..')
from src.process_data import *
from src.cut import *
from src.transmission import *
parser = argparse.ArgumentParser()
#parser.add_argument("input", type=str, help="intput file(.hdf5)")
parser.add_argument("config",type=str, help="config file of input file")
parser.add_argument("tag",type=str,help="tag of input files")
parser.add_argument("conditions_in", type=str, help="conditions of input file")
parser.add_argument("conditions_out", type=str, help="conditions of input file")
parser.add_argument("detector", type=str,choices=['PTBC','PKUP','FIMG'], help="detector")
#parser.add_argument("cut",type=str, help="cut of energy and amplitude ")
args = parser.parse_args()
with open(args.config,'r') as cfg:
    config=yaml.safe_load(cfg)
          
#with open(args.cut,'r') as cuts:
#    cut=yaml.safe_load(cuts)
##########    


input_In  = 'temp_data/' + config[args.tag][args.conditions_in]['data'] + '_' + config[args.tag][args.conditions_in]['target'] + '_'+ config[args.tag][args.conditions_in]['filter']+'_' + args.detector+'.h5'
input_Out = 'temp_data/' + config[args.tag][args.conditions_out]['data'] +'_' + config[args.tag][args.conditions_out]['target']+'_' + config[args.tag][args.conditions_out]['filter'] + '_' + args.detector+'.h5'

tof_In,en_In,norm_In = get_cut(input_In, args.detector)
tof_Out,en_Out,norm_Out = get_cut(input_Out, args.detector)
#In = h5py.File(input_in, "r")
#Out = h5py.File(input_out, "r")
#amp_In = In[args.detector]['amp'][:]
#tof_In=In[args.detector]['tof'][:]
#en_In = In[args.detector]['energy'][:]
#norm_In = In[args.detector]['norm'][0]
#amp_Out = Out[args.detector]['amp'][:]
#en_Out = Out[args.detector]['energy'][:]
#tof_Out=Out[args.detector]['tof'][:]
#norm_Out = Out[args.detector]['norm'][0]

#if args.cut:
norm = norm_Out/norm_In
#num_bins_tof, bin_edge_tof, num_bins_en, bin_edge_en = bin_edge(args.detector)

#bins_tof=100 
#tof_In_select,en_In_select   = data_cut(tof_In,amp_In,args.detector)
#tof_Out_select,en_Out_select = data_cut(tof_Out,amp_Out,args.detector)
#print(len(tof_In))
#print(len(en_In_select))
#en_In_select = en_In
#en_Out_select = en_Out
#tof_In_select = tof_In
#tof_Out_select = tof_Out
#if args.cut:
logbins = np.logspace(-1,9,300)
hist_in_en,bins_in_en,_ = plt.hist(en_In,bins= logbins)
#print(bin_edge_en)
#plt.savefig('temp_data/Test.png',dpi=600)
#hist_in_tof,bins_in_tof,_ =  plt.hist(tof_In,bins=bin_edge_tof)
hist_in_en[ hist_in_en== 0] = 0.001

hist_out_en,bins_out_en,_ = plt.hist(en_Out,bins= logbins)
#hist_out_en[ hist_out_en== 0] = 0.001
#hist_out_tof,bins_out_tof,_ =  plt.hist(tof_Out,bins= bin_edge_tof)


tr,tr_error=transmission(hist_in_en,hist_out_en,norm)
en_bin = (bins_in_en[1:] + bins_in_en[:-1]) / 2
#print(en_bin)
plt.clf()




#MC and endf data
f = open("temp_data/Ar.txt")
energy = []
xsec = []
for line in f:
    energy.append(float(line[3:14])*1e6) # in eV
    xsec.append(float(line[16:27]))
    #xsec.append(float(line[20:27]))
energy = np.array(energy)
xsec = np.array(xsec)
f.close()
ar_bottle_pressure = 197.385 * 1e5 # in Pa (SI unit)
ar_bottle_temp = 293.0 # in Kelvin
n_density_Ar = 11 *(ar_bottle_pressure / (8.31446261815324 * ar_bottle_temp * 1e6)) * 6.02214076e23 * 1e-24
ts = XsecToTs(xsec, n_density_Ar)

en_min= 1e3
en_max = 1e6 #eV
en_Ar= []
tr_Ar=[]
en_out=[]
for i in range(100000):
    en = np.random.uniform(en_min,en_max)
    ts_Ar = np.interp(en, energy, ts)
    en_out.append(en)
    tr_s = np.random.rand()*1
    if ts_Ar > tr_s:
        en_Ar.append(en)
        tr_Ar.append(tr_s)
logbins_MC = np.logspace(0,6,200)
hist_in_en_MC,bins_in_en_MC,_ = plt.hist(en_Ar,bins=logbins_MC)
hist_out_en_MC,bins_out_en_MC,_ = plt.hist(en_out,bins=logbins_MC)        

tr_MC,tr_error_MC = transmission(hist_in_en_MC,hist_out_en_MC,1)
en_bin_MC = (bins_in_en_MC[1:] + bins_in_en_MC[:-1]) / 2
plt.clf()
plt.figure(figsize=(20,8))
plt.errorbar(en_bin_MC,tr_MC,tr_error_MC,fmt ='o',label= 'MC')


plt.plot(energy,ts,label = 'ENDF')


#plt.hist2d(en_bin,tr, bin_edge_en)

plt.errorbar(en_bin,tr,tr_error,fmt ='o',label= 'PTBC')
plt.xlabel('En')
plt.xscale("log")
plt.xlim(1e3,1e6)
plt.legend(loc='lower left')
#plt.grid()
plt.savefig('temp_data/Transmission_'+args.conditions_in + '_'+args.detector + '.png',dpi=600)
plt.clf()

#xsec,xsec_error = cross_section(tr,config[args.tag][args.conditions_in]['num_density'])
#plt.errorbar(en_bin,xsec,xsec_error,fmt ='o',ecolor='r',ms=0.5,elinewidth=1.5)
#plt.xlabel('En')
#plt.xscale("log")
#plt.savefig('temp_data/CrossSection.png',dpi=600)
#plt.clf()
