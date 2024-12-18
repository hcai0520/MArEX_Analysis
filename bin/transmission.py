import argparse
import yaml
import h5py
import matplotlib.pyplot as plt
import ROOT
import sys
sys.path.append('src/..')
from src.process_data import *
from src.cut import *
from src.transmission import *
parser = argparse.ArgumentParser()
#parser.add_argument("input", type=str, help="intput file(.hdf5)")
parser.add_argument("config",type=str, help="config file (yml files)")
#parser.add_argument("tag",type=str,help="tag of input files")
parser.add_argument("tag_in", type=str, help="conditions of input file (target and filter)")
parser.add_argument("tag_out", type=str, help="conditions of input file (target and filter)")
parser.add_argument("detector", type=str,choices=['PTBC','PKUP','FIMG'], help="detector")
#parser.add_argument("cut",type=str, help="cut of energy and amplitude ")
args = parser.parse_args()
with open(args.config,'r') as cfg:
    config=yaml.safe_load(cfg)
             
###############################
def TOFToEnergy(tof, x, m, c):
    return m * (1 / np.sqrt(1 - x * x / c / c / tof / tof) - 1) 

L = 182.24
if args.detector == 'PTBC':
    L == 182.65 - 0.41 # in m 182.24
if args.detector == 'FIMG':
    L == 183.5 - 0.41  # in m 
###############################


input_In  = 'temp_data/' +  args.detector + '_' + args.tag_in + '.h5'
input_Out = 'temp_data/' +  args.detector + '_' + args.tag_out + '.h5'


tof_In,norm_In = get_cut(input_In, args.detector)
tof_Out,norm_Out = get_cut(input_Out, args.detector)
en_In = TOFToEnergy(tof_In / 1e9, L, 939.56542, 299792458)*1e6 # in eV
en_Out = TOFToEnergy(tof_Out / 1e9, L, 939.56542, 299792458)*1e6 # in eV

norm = norm_Out/norm_In

logbins = np.logspace(-1,7,200)
Target_in = ROOT.TH1F(args.detector + '_' + args.tag_in,args.detector + '_' + args.tag_in,199,logbins)
Target_out = ROOT.TH1F(args.detector + '_' + args.tag_out,args.detector + '_' + args.tag_out,199,logbins)

c = ROOT.TCanvas('c','',200,10,1200,600)
c.SetGrid()

for en in en_In:
    Target_in.Fill(en)
for en in en_Out:
    Target_out. Fill(en)    


Target_in.Draw()
c.SetLogx()

c.SaveAs('temp_data/hist_' + args.detector  + '_' + args.tag_in + '.png')
Target_out.Draw()
c.SaveAs('temp_data/hist_' + args.detector  + '_' + args.tag_out +'.png')
c.Update()

en_tr = np.array([])
tr = np.array([])
tr_err = np.array([])

for en in range(199):
    if Target_out.GetBinContent(en+1) > 0 :
        tr_i = Target_in.GetBinContent(en+1)/Target_out.GetBinContent(en+1)
        tr_err_i = np.sqrt((np.sqrt(Target_in.GetBinContent(en+1)) / Target_out.GetBinContent(en+1))**2 + (Target_in.GetBinContent(en+1) * np.sqrt(Target_out.GetBinContent(en+1)) / Target_out.GetBinContent(en+1) ** 2) ** 2)
        en_tr = np.append(en_tr,logbins[en])
        tr = np.append(tr, tr_i)
        tr_err = np.append(tr_err, tr_err_i)
n = len(tr)
x= np.zeros(n)
gr = ROOT.TGraphErrors(n,en_tr,tr,x,tr_err)
gr.SetTitle('Transmission_' + args.detector  + '_'+ args.tag_in +'_'+ args.tag_out )
gr.SetLineColor(2)
gr.GetXaxis().SetTitle("Energy(eV)")
#gr.SetMarkerStyle( 21 )
gr.Draw('AP')
 

c.SetLogx()
c.Update()
c.SaveAs('temp_data/Transmission_' + args.detector  + '_'+ args.tag_in +'_'+ args.tag_out + '.png')

# tr,tr_error=transmission(hist_in_en,hist_out_en,norm)
# en_bin = (bins_in_en[1:] + bins_in_en[:-1]) / 2
# #print(en_bin)
# plt.clf()

data_file = open('temp_data/T_' + args.detector  + '_'+ args.tag_in +'_'+ args.tag_out+'.dat','w')
for i in range(n):
    data_file.write(str(format(en_tr[i],'.10f')).rjust(20)+str(format(tr[i],'.13f')).rjust(20)+str(format(tr_err[i],'.13f')).rjust(20))
    data_file.write("\n")
data_file.close()
print('Data is written into '+'T_' + args.detector  + '_'+ args.tag_in +'_'+ args.tag_out+'.dat')    



#MC and endf data
# f = open("temp_data/Ar.txt")
# energy = []
# xsec = []
# for line in f:
#     energy.append(float(line[3:14])*1e6) # in eV
#     xsec.append(float(line[16:27]))
#     #xsec.append(float(line[20:27]))
# energy = np.array(energy)
# xsec = np.array(xsec)
# f.close()
# ar_bottle_pressure = 197.385 * 1e5 # in Pa (SI unit)
# ar_bottle_temp = 293.0 # in Kelvin
# n_density_Ar = 11 *(ar_bottle_pressure / (8.31446261815324 * ar_bottle_temp * 1e6)) * 6.02214076e23 * 1e-24
# ts = XsecToTs(xsec, n_density_Ar)

# en_min= 1e3
# en_max = 1e6 #eV
# en_Ar= []
# tr_Ar=[]
# en_out=[]
# for i in range(100000):
#     en = np.random.uniform(en_min,en_max)
#     ts_Ar = np.interp(en, energy, ts)
#     en_out.append(en)
#     tr_s = np.random.rand()*1
#     if ts_Ar > tr_s:
#         en_Ar.append(en)
#         tr_Ar.append(tr_s)
# logbins_MC = np.logspace(0,6,200)
# hist_in_en_MC,bins_in_en_MC,_ = plt.hist(en_Ar,bins=logbins_MC)
# hist_out_en_MC,bins_out_en_MC,_ = plt.hist(en_out,bins=logbins_MC)        

# tr_MC,tr_error_MC = transmission(hist_in_en_MC,hist_out_en_MC,1)
# en_bin_MC = (bins_in_en_MC[1:] + bins_in_en_MC[:-1]) / 2
# plt.clf()
# plt.figure(figsize=(20,8))
# plt.errorbar(en_bin_MC,tr_MC,tr_error_MC,fmt ='o',label= 'MC')


# plt.plot(energy,ts,label = 'ENDF')


#plt.hist2d(en_bin,tr, bin_edge_en)

# plt.errorbar(en_bin,tr,tr_error,fmt ='o',label= 'PTBC')
# plt.xlabel('En')
# plt.xscale("log")
# plt.xlim(1e3,1e6)
# plt.legend(loc='lower left')
# #plt.grid()
# plt.savefig('temp_data/Transmission_'+args.conditions_in + '_'+args.detector + '.png',dpi=600)
# plt.clf()

#xsec,xsec_error = cross_section(tr,config[args.tag][args.conditions_in]['num_density'])
#plt.errorbar(en_bin,xsec,xsec_error,fmt ='o',ecolor='r',ms=0.5,elinewidth=1.5)
#plt.xlabel('En')
#plt.xscale("log")
#plt.savefig('temp_data/CrossSection.png',dpi=600)
#plt.clf()
