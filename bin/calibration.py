import numpy as np
import argparse
import yaml
import pandas as pd
import matplotlib.pyplot as plt
from iminuit import Minuit
import sys
sys.path.append('src/..')
from src.process_data import *
from src.transmission import *
from src.smear import *
from src.chi_sq import *
parser = argparse.ArgumentParser()

parser.add_argument("config",type=str, help="configuration of input file")
parser.add_argument("tag",type=str,help="tag of input files")
parser.add_argument("conditions_in", type=str, help="conditions of input file")
parser.add_argument("conditions_out", type=str, help="conditions of input file")

parser.add_argument("detector", type=str,choices=['PTBC','PKUP','FIMG'], help="detector")
parser.add_argument("initial_L",type = float, help= "Initial guess of length (m)")
parser.add_argument("initial_t",type = float, help = "Initial guess of target thickness (cm)")
args = parser.parse_args()
with open(args.config,'r') as cfg:
    config=yaml.safe_load(cfg)
f=config[args.tag][args.conditions_in]['endf']

energy,xsec = read_endf(f)




infile= 'temp_data/' + config[args.tag][args.conditions_in]['target'] + '_'+config[args.tag][args.conditions_in]['filter']+'_'+args.detector +'.xlsx'
outfile= 'temp_data/' + config[args.tag][args.conditions_out]['target'] + '_'+config[args.tag][args.conditions_out]['filter']+'_'+args.detector +'.xlsx'

Input= pd.read_excel(infile)
tof_in =np.array( Input['tof'])
tof_in = tof_in[::-1]
norm_in = Input['norm'][0]
Output = pd.read_excel(outfile)
tof_out = np.array(Output['tof'])
tof_out = tof_out[::-1]
norm_out = Output['norm'][0]
Norm =norm_out/norm_in
en_low = float(config[args.tag][args.conditions_in]['en_low']) # eV
en_high = float(config[args.tag][args.conditions_in]['en_high'])

number_density = float(config[args.tag][args.conditions_in]['num_density'])

thickness = float(config[args.tag][args.conditions_in]['thickness'])

def get_tr(L):    
    tof_high = EnergyToTOF(en_low/1e6,L,939.56542, 299792458)*1e9 #ns
    tof_low = EnergyToTOF(en_high/1e6,L,939.56542, 299792458)*1e9
    tof_in_select = tof_in[(tof_in > tof_low) & (tof_in < tof_high)]
    tof_out_select = tof_out[(tof_out > tof_low) & (tof_out < tof_high)]
    hist_tof_in,bins_tof_in,_ = plt.hist(tof_in_select,bins=50)
    hist_tof_out,bins_tof_out,_ = plt.hist(tof_out_select,bins=50)
    x_tof = (bins_tof_in[1:]+bins_tof_in[:-1])/2
    hist_tof_in[hist_tof_in==0] = 0.001
    tr,tr_err = transmission(hist_tof_in,hist_tof_out,Norm)

    return x_tof, tr,tr_err

def f_minuit(L,t):
    x_tof, tr, tr_err = get_tr(L)
    energy_smear, xsec_smear = smear(energy,xsec,29/100,37/100,en_low,en_high,100,L)
    chi_square = chi_sq(L,t,xsec_smear,energy_smear,x_tof,tr,tr_err,number_density,thickness)
    return chi_square 

L_initial = args.initial_L
t_initial = args.initial_t   

m= Minuit(f_minuit,L_initial,t_initial)

print(m.migrad())