import numpy as np
from matplotlib import pyplot as plt


def graph(data, n_bins, min_bin=1e-6):
    data = data[data > 0]
    hist, bins, _ = plt.hist(data, bins=n_bins)
    if bins[0] > min_bin:
        min_bin = bins[0]
    logbins = np.logspace(np.log10(min_bin), np.log10(bins[-1]), len(bins))
    # plt.figure(figsize=(8,8))
    hist2, bins2, _ = plt.hist(data, bins=logbins)
    # plt.xscale('log')
    return hist, bins, hist2, bins2
