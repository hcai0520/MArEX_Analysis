import numpy as np
import uproot
from matplotlib import pyplot as plt
import matplotlib as mpl
import h5py
import argparse

from src.graph import graph
from src.transmission import transmission

from src.process_data import process_data

parser = argparse.ArgumentParser()
parser.add_argument("output_in", type=str, help="output file of neutron in")
parser.add_argument("output_out", type=str, help="output file of neutron out")

args = parser.parse_args()

BiIn = h5py.File(args.output_in, "r")
BiOut = h5py.File(args.output_out, "r")

amp_BiIn = BiIn['amp'][:]
en_BiIn = BiIn['energy'][:]
norm_BiIn = BiIn['norm'][0]
amp_BiOut = BiOut['amp'][:]
en_BiOut = BiOut['energy'][:]
norm_BiOut = BiOut['norm'][0]

en_BiIn_select = en_BiIn[(en_BiIn > 600) & (en_BiIn < 1000) & (amp_BiIn > 4000)]
en_BiOut_select = en_BiOut[(en_BiOut > 600) & (en_BiOut < 1000) & (amp_BiOut > 4000)]

hist_BiIn, bins_BiIn, _, _ = graph(en_BiIn_select, 100)
plt.savefig('plot/en_BiIn.png')

hist_BiOut, bins_BiOut, _, _ = graph(en_BiOut_select, 100)

plt.savefig('plot/en_BiOut.png')

tr, tr_error = transmission(hist_BiIn, np.sqrt(hist_BiIn), hist_BiOut, np.sqrt(hist_BiOut))

bins = (bins_BiIn[1:] + bins_BiIn[:-1]) / 2

plt.figure(figsize=(10,10))
plt.errorbar(bins, tr, yerr=tr_error)

plt.savefig('plot/transmission')