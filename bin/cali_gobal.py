from iminuit import Minuit
import matplotlib.pyplot as plt
import sys
sys.path.append('src/..')
from src.transmission import *
from src.cut import *
from src.smear import *
from src.chi_sq import *
import yaml
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("config",type=str, help="configuration of input file")
parser.add_argument("tag",type=str,help="tag of input files")
parser.add_argument('-t','--tar',type=str, nargs='+', help="list of input target for calibration")
parser.add_argument('-d','--det',type=str, nargs='+', help="list of target detector for calibration")
parser.add_argument('-p','--para', nargs='+', help="minimize parameter t,L (t1,t2,..,L1,L2,..)")

parser.add_argument('-g','--guess', nargs='+',help="list of initial guess of L,t (same order as input parameter)")
args = parser.parse_args()
with open(args.config,'r') as cfg:
    config=yaml.safe_load(cfg)


def get_empty(condition,detector):
    if condition == 'Argon_bottle_231017' or condition == 'Argon_bottle_231018' or condition == 'Argon_bottle_231019' or condition == 'Argon_bottle_231020' or condition == 'Argon_bottle_231021' or condition == 'Argon_bottle_231022' or condition == 'Argon_bottle_231023' :
        if detector == 'PTBC':
            empty = 'temp_data/data_air_bottle_empty_PTBC.h5'
            tof_empty, en_empty, norm_empty = get_cut(empty, detector)
        if detector == 'FIMG':
            empty = 'temp_data/data_air_bottle_empty_FIMG.h5'
            tof_empty, en_empty, norm_empty = get_cut(empty, detector)    
    else:
        if detector == 'PTBC':
            empty = 'temp_data/data_empty_empty_PTBC.h5'
            tof_empty, en_empty, norm_empty = get_cut(empty, detector)
        if detector == 'FIMG':
            empty = 'temp_data/data_empty_empty_FIMG.h5'
            tof_empty, en_empty, norm_empty = get_cut(empty, detector) 
        
    return tof_empty, en_empty, norm_empty



def get_tr(condition,tof,tof_empty ,L,Norm):
    en_low = float(config[args.tag][condition]['en_low'])
    en_high = float(config[args.tag][condition]['en_high']) 
    
    #tof ns en eV
    tof = tof[::-1]
    tof_empty = tof_empty[::-1]
    tof_high = EnergyToTOF(en_low/1e6,L,939.56542, 299792458)*1e9 #ns
    tof_low = EnergyToTOF(en_high/1e6,L,939.56542, 299792458)*1e9
    tof_select = tof[(tof > tof_low ) & (tof < tof_high) ]
    tof_empty_select = tof_empty[(tof_empty > tof_low) &(tof_empty < tof_high)]
    #logbins = np.logspace(3,5,50)
   # tof_select=tof_select[::-1]
   # tof_empty_select = tof_empty_select[::-1]

    hist_tof,bins_tof,_  = plt.hist(tof_select, bins=50)
    hist_empty_tof,bins_empty_tof,_  = plt.hist(tof_empty_select, bins=50)

    x_tof = (bins_tof[1:] + bins_tof[:-1])/2
    #Norm = norm_empty/norm
    hist_tof[hist_tof== 0] = 0.001

    tr,tr_err = transmission(hist_tof,hist_empty_tof,Norm)  
    return x_tof ,tr , tr_err
    #### get smear (endf) 
def get_smear(condition,L):
    en_low = float(config[args.tag][condition]['en_low'])
    en_high = float(config[args.tag][condition]['en_high'])
    f=config[args.tag][condition]['endf']
    energy, xsec = read_endf(f)
    energy_smear, xsec_smear = smear(energy, xsec, 29/100, 37/100,en_low, en_high, 100, L)
#    tof_smear = EnergyToTOF(energy_smear/1e6, L , 939.56542, 299792458) # in s 
    return xsec_smear, energy_smear
condition = []
detector = []
number_density =[]
thickness= []

tof=[]
tof_empty=[]
Norm=[]
#print(args.det)
for i in range(len(args.det)):
    detector.append(str(args.det[i]))
for i in range(len(args.tar)):
    condition.append(str(args.tar[i]))
    number_density.append( float(config[args.tag][condition[i]]['num_density']))
    thickness.append(config[args.tag][condition[i]]['thickness'])
    for j in range(len(detector)):
        input = 'temp_data/'+config[args.tag][condition[i]]['data'] + '_' + config[args.tag][condition[i]]['target'] + '_'+config[args.tag][condition[i]]['filter']+'_'+detector[j]+'.h5'
        tof_i,en,norm = get_cut(input, detector[j])
        tof_empty_i, en_empty, norm_empty = get_empty(condition[i],detector[j])
        tof.append(tof_i)
        tof_empty.append(tof_empty_i)
        Norm.append(norm_empty/norm)
n = len(detector) 
L_t = args.para
def f_minuit(L_t):
    chi_sq_tot=0
    for i in range(len(condition)):
        t = L_t[i]
        for j in range(len(detector)):
            L = L_t[len(condition) + j]
            x ,tr, tr_err  = get_tr(condition[i],tof[n*i+j],tof_empty[n*i+j],L,Norm[n*i+j])
            xsec_smear, energy_smear = get_smear(condition[i],L)
            chi_sq_i = chi_sq(182.24,t,xsec_smear,energy_smear,x,tr,tr_err,number_density[i], thickness[i])

#            xsec_smear.append(xsec_smear_i)
#            tof_smear.append(tof_smear_i)              
#            chi_sq_i = chi_sq(L,t,xsec_smear[n*i+j],tof_smear[n*i+j],x_en[n*i+j],tr[n*i+j],tr_err[n*i+j],number_density[i], thickness[i])
            chi_sq_tot = chi_sq_i + chi_sq_tot
    
    return chi_sq_tot
L_t_initial=[]
for i in range(len(args.guess)):
    L_t_initial.append(float(args.guess[i]))
L_t_initial = tuple(L_t_initial)
#print(L_t_initial)

m = Minuit(f_minuit,L_t_initial)
#m.fixed["L"] = True
print(m.migrad())