import matplotlib.pyplot as plt
import h5py
import argparse
import numpy as np
import sys
import prettytable as pt
import yaml
sys.path.append('src/..')
#sys.path.append('config/')
#from src.graph import graph
#from src.transmission import transmission

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="intput file(.hdf5)")
parser.add_argument("config",type=str, help="configuration of input file")
#parser.add_argument("--tag",type=str,help="tag of input files")
parser.add_argument("--cut",type=str, help="cut of energy and amplitude ")
#parser.add_argument("output_out", type=str, help="output file (.hdf5) of target out")
parser.add_argument("--screen_dump",action="store_true",help="print the data of input file")
parser.add_argument("--compare",type=str,help="another input files for cpmarison")
parser.add_argument("-cc","--config_compare",type=str, help="configuration of file of comparison")
parser.add_argument("-tc","--tag_compare",type=str,help="tag of input files")
# add tag
# add plot.txt


parser.add_argument("--max",type=int,help="the number of printed data")

args = parser.parse_args()
with open(args.config,'r') as cfg:
    config=yaml.safe_load(cfg)
if args.compare:     
    with open(args.config_compare,'r') as cfg_c:
        config_c=yaml.safe_load(cfg_c)     
with open(args.cut,'r') as cuts:
    cut=yaml.safe_load(cuts)


Infile = h5py.File(args.input, "r")
tof_In=Infile['tof'][:]
amp_In = Infile['amp'][:]
en_In = Infile['energy'][:]
norm_In = Infile['norm'][0]

if args.compare:
    Comparefile = h5py.File(args.compare, "r")
    tof_Compare=Comparefile['tof'][:]
    amp_Compare = Comparefile['amp'][:]
    en_Compare = Comparefile['energy'][:]
    norm_Compare = Comparefile['norm'][0]


if args.screen_dump:
    tb_config=pt.PrettyTable()
    tb_config.title = str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] )
    tb_config.field_names=['data','filter','target','norm']
    tb_config.add_row([config['setup_info']['data'], config['setup_info']['filter'], config['setup_info']['target'],norm_In])  
    tb_in = pt.PrettyTable()
    #tb_in.title = 
    tb_in.field_names = [ "Index","Amplitude", "ToF", "Energy"]
    if args.max:
        if args.max <= len(Infile['tof']):
            for i in range(args.max):
                tb_in.add_row([i,amp_In[i], tof_In[i], en_In[i]])                
        else:
            print("Index is out of range")
               
    else:
        for i in range(len(tof_In)): 
            tb_in.add_row([i,amp_In[i], tof_In[i], en_In[i]])
    if args.compare:        
        tb_compare_config=pt.PrettyTable()
        tb_compare_config.title = str(config_c['setup_info']['data']) + str(config_c['setup_info']['filter']) + '_' + str(config_c['setup_info']['thickness'])+'mm_'+ str(config_c['setup_info']['target'] )

        tb_compare_config.field_names=['data','filter','target','norm']
        tb_compare_config.add_row([config_c['setup_info']['data'], config_c['setup_info']['filter'], config_c['setup_info']['target'],norm_Compare]) 
        tb_compare = pt.PrettyTable()
        tb_compare.field_names = [ "Index","Amplitude", "ToF", "Energy"]
        if args.max:
            if args.max <= len(Comparefile['tof']):
                for i in range(args.max):
                    tb_compare.add_row([i,amp_Compare[i], tof_Compare[i], en_Compare[i]])                
            else:
                print("Index is out of range")
               
        else:
            for i in range(len(tof_Compare)): 
                tb_in.add_row([i,amp_Compare[i], tof_Compare[i], en_Compare[i]])
    #("Input file data")          
    print(tb_config)
    print(tb_in)
    if args.compare:
    #    print("Comparison file data")
        print(tb_compare_config)
        print(tb_compare)
    
if args.cut:
    en_In_select = en_In[(en_In > cut['roi_cut']['e_min']) & (en_In < cut['roi_cut']['e_max']) & (amp_In > cut['alpha_cut']['amp'])]
    tof_In_select = tof_In[(en_In > cut['roi_cut']['e_min']) & (en_In < cut['roi_cut']['e_max']) & (amp_In > cut['alpha_cut']['amp'])]

bins_en=100
bins_tof=100

if args.compare:
    if args.cut:
        en_Compare_select = en_Compare[(en_Compare > cut['roi_cut']['e_min']) & (en_Compare < cut['roi_cut']['e_max']) & (amp_Compare > cut['alpha_cut']['amp'])]
        tof_Compare_select = tof_Compare[(en_Compare > cut['roi_cut']['e_min']) & (en_Compare < cut['roi_cut']['e_max']) & (amp_Compare > cut['alpha_cut']['amp'])]
        hist_in,bins_in,_=plt.hist(en_In_select,bins_en,alpha = 0.5,color='green',label='En_' + str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] ))
        plt.clf()   
        x_en = (bins_in[1:] + bins_in[:-1]) / 2
        error_in = np.sqrt(hist_in)
        plt.errorbar(x_en,hist_in,error_in,fmt ='o',ecolor='r',ms=2.5,elinewidth=1.5,label="En_"+str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] ))
        hist_compare,bins_compare,_=plt.hist(en_Compare_select,bins_en,alpha = 0.5,color='yellow',label='En_'+str(config_c['setup_info']['data']) + str(config_c['setup_info']['filter']) + '_' + str(config_c['setup_info']['thickness'])+'mm_'+ str(config_c['setup_info']['target'] )) 
        
    else:    
        hist_in,bins_in,_ = plt.hist(en_In,bins_en,alpha = 0.5,color='green',label='En_in')
        plt.clf()
        x_en = (bins_in[1:] + bins_in[:-1]) / 2
        error_in = np.sqrt(hist_in)
        plt.errorbar(x_en,hist_in,error_in,fmt ='o',ecolor='r',ms=2.5,elinewidth=1.5,label="En_"+str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] ))
        hist_compare,bins_compare,_ = plt.hist(en_Compare,bins_en,alpha = 0.5,color='yellow',label='En_')+str(config_c['setup_info']['data']) + str(config_c['setup_info']['filter']) + '_' + str(config_c['setup_info']['thickness'])+'mm_'+ str(config_c['setup_info']['target'] )
        
    np.savetxt('En_'+str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] )+'.txt',np.array(hist_in))
    np.savetxt('En_'+str(config_c['setup_info']['data']) + str(config_c['setup_info']['filter']) + '_' + str(config_c['setup_info']['thickness'])+'mm_'+ str(config_c['setup_info']['target'] )+'.txt',np.array(hist_compare))
    plt.legend(loc='upper right')
    plt.xlabel('En')
    plt.ylabel('N')
    plt.savefig('./NvsEn',dpi=600)
    plt.clf()
    if args.cut:
        hist_in_tof,bins_in_tof,_ = plt.hist(tof_In_select,bins_tof,alpha = 0.5,color='red',label='tof_in')
        plt.clf()
        x_tof = (bins_in_tof[1:] + bins_in_tof[:-1]) / 2
        error_in_tof = np.sqrt(hist_in_tof)
        plt.errorbar(x_tof,hist_in_tof,error_in_tof,fmt ='o',ecolor='r',ms=2.5,elinewidth=1.5,label='tof'+str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] ))
        hist_compare_tof,bins_compare_tof,_ =plt.hist(tof_Compare_select,bins_tof,alpha = 0.5,color='blue',label='tof_'+str(config_c['setup_info']['data']) + str(config_c['setup_info']['filter']) + '_' + str(config_c['setup_info']['thickness'])+'mm_'+ str(config_c['setup_info']['target'] ))
        
    else:
        hist_in_tof,bins_in_tof,_  = plt.hist(tof_In,bins_tof,alpha = 0.5,color='red',label='tof_in')
        plt.clf()
        x_tof = (bins_in_tof[1:] + bins_in_tof[:-1]) / 2
        error_in_tof = np.sqrt(hist_in_tof)
        plt.errorbar(x_tof,hist_in_tof,error_in_tof,fmt ='o',ecolor='r',ms=2.5,elinewidth=1.5,label='tof_'+str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] ))
        hist_compare_tof,bins_compare_tof,_ = plt.hist(tof_Compare,bins_tof,alpha = 0.5,color='blue',label='tof_'+str(config_c['setup_info']['data']) + str(config_c['setup_info']['filter']) + '_' + str(config_c['setup_info']['thickness'])+'mm_'+ str(config_c['setup_info']['target'] ))  
    
    np.savetxt('TOF_'+str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] )+'.txt',np.array(hist_in_tof))
    np.savetxt('TOF_'+str(config_c['setup_info']['data']) + str(config_c['setup_info']['filter']) + '_' + str(config_c['setup_info']['thickness'])+'mm_'+ str(config_c['setup_info']['target'] )+'.txt',np.array(hist_compare_tof))

    plt.legend(loc='upper right')
    plt.xlabel('tof')
    plt.ylabel('N')
    plt.savefig('./Nvstof',dpi=600)
    plt.clf()
else:
    if args.cut:
        hist_in,bins_in,_ = plt.hist(en_In_select,bins_en)
    else:
        hist_in,bins_in,_ = plt.hist(en_In,bins_en)
    
    np.savetxt('En_'+str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] )+'.txt',np.array(hist_in))
    plt.title('En_'+str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] ))
    #plt.legend(loc='upper right')
    plt.xlabel('En')
    plt.ylabel('N')
    plt.savefig('./NvsEn',dpi=600)
    plt.clf()
    if args.cut:
        hist_in_tof,bins_in_tof,_ =  plt.hist(tof_In_select,bins_tof)
    else:
        hist_in_tof,bins_in_tof,_ = plt.hist(tof_In,bins_tof)    
    np.savetxt('TOF_'+str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] )+'.txt',np.array(hist_in_tof))
    plt.title('TOF_'+str(config['setup_info']['data']) + str(config['setup_info']['filter']) + '_' + str(config['setup_info']['thickness'])+'mm_'+ str(config['setup_info']['target'] ))
    plt.xlabel('tof')
    plt.ylabel('N')
    plt.savefig('./Nvstof',dpi=600)
    plt.clf()
    

