import numpy as np

def xsec(transmission, transmission_error, target_mass, target_density, target_thickness):
    return -target_mass / target_density / target_thickness * np.log(transmission), target_mass * transmission_error / target_density / target_thickness / target_thickness