import numpy as np


def transmission(target_in, target_in_error, target_out, target_out_error):
    transmission = target_in / target_out
    error_transmission = np.sqrt((target_in_error / target_out) **
                                 2 + (target_in * target_out_error / target_out ** 2) ** 2)
    return transmission, error_transmission
