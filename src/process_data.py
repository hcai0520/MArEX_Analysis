import numpy as np
import uproot
import h5py

def energy(tof, x, m, c):
    return m * (1 / np.sqrt(1 - x * x / c / c / tof / tof) - 1)

def get_data(run_number, detector):
    run_number = str(run_number)
    data = uproot.open("data/run" + run_number + ".root")[detector + ";1"]
    tflash = data['tflash'].array(library="np")
    tof = data['tof'].array(library="np")
    detn = data['detn'].array(library="np")
    BN = data['BunchNumber'].array(library="np")
    PI = data['PulseIntensity'].array(library="np")
    amp = data['amp'].array(library="np")
    norm = PI[0]
    for i in range(1, len(PI)):
        if BN[i] != BN[i - 1]:
            norm += PI[i]
    return tflash, tof, amp, norm

def process_data(run_numbers, detector, output):
    tflash = np.array([])
    tof = np.array([])
    amp = np.array([])
    norm = 0
    L = 184.5
    if detector == "C6D6":
        L += 6.89
    for i in run_numbers:
        tflash_i, tof_i, amp_i, norm_i = get_data(i, detector)
        tflash = np.append(tflash, tflash_i)
        tof = np.append(tof, tof_i)
        amp = np.append(amp, amp_i)
        norm += norm_i
    real_tof = tof - tflash + L / 299792458 * 1e9
    en = energy(real_tof, L, 939.56542, 299792458)
    f = h5py.File(output, "w")
    f.create_dataset("energy", data=en)
    f.create_dataset("amp", data=amp)
    f.create_dataset("norm", data=[norm])
    f.close
