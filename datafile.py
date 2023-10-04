import numpy as np
import uproot
from matplotlib import pyplot as plt
import matplotlib as mpl
import h5py
import argparse


from src.process_data import process_data

parser = argparse.ArgumentParser()
parser.add_argument("runnumber_in_base", type=int,help="base of run number of neutron in ")
parser.add_argument("runnumber_in_top", type=int,help="top of run number of neutron in ")
parser.add_argument("runnumber_out_base", type=int,help="base of run number of neutron out ")
parser.add_argument("runnumber_out_top", type=int,help="base of run number of neutron out ")

parser.add_argument("detector", type=str, help="detector")
parser.add_argument("output_in", type=str, help="output file of neutron in")
parser.add_argument("output_out", type=str, help="output file of neutron out")


args = parser.parse_args()
#print(args.runnumber_out_top)

process_data([i for i in range(args.runnumber_in_base, args.runnumber_in_top)], args.detector, args.output_in)

process_data([i for i in range(args.runnumber_out_base, args.runnumber_out_top)], args.detector, args.output_out)