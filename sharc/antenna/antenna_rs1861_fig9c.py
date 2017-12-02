#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 14:09:08 2017

@author: carlosrodriguez
"""

from sharc.antenna.antenna import Antenna
from sharc.parameters.parameters_fss_ss import ParametersFssSs

import numpy as np

class AntennaRS1861FIG9c(Antenna):
    """
    Implements the EESS sensor antenna for 23.6-24 GHz for Sensor type F4
    """
    
    def __init__(self, param: ParametersFssSs):
        super().__init__()
        self.peak_gain = param.antenna_gain
        

        self.phi_1 = 10       
        self.phi_2 = 140
                
    def calculate_gain(self, *args, **kwargs) -> np.array:
        phi = np.absolute(kwargs["phi_vec"])
        
        gain = np.zeros(phi.shape)
        "Form parabolic equation according to figure 9c, a*attˆ2+b*att+angle = 0"
        a = 0.010521886
        b = 0.650252525
        
        "From line eq for second part of fig 9c att=m*angle+c"
        m = -0.25384615
        c = -30.4615385

        idx_0 = np.where((0 <= phi) & (phi < self.phi_1))[0]
        gain[idx_0] = self.peak_gain + ( - 1 * b + np.sqrt(np.power(b,2) - 4 * a * phi[idx_0]))/(2 * a)

        idx_1 = np.where((self.phi_1 <= phi) & (phi <= self.phi_2))[0]
        gain[idx_1] = self.peak_gain + m * phi[idx_1] + c
        
        idx_2 = np.where((self.phi_2 <= phi) & (phi < 180))[0]
        gain[idx_2] = self.peak_gain - 66
         
        return gain
        
        
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    phi = np.linspace(0.1, 179, num = 100000)
    
    # initialize antenna parameters
    param27 = ParametersFssSs()
    param27.antenna_pattern = "ITU-R RS.1861 Figure 9c"
    param27.frequency = 23800
    param27.antenna_gain = 50
    antenna27 = AntennaRS1861FIG9c(param27)

    gain27 = antenna27.calculate_gain(phi_vec=phi)
    

    fig = plt.figure(figsize=(8,7), facecolor='w', edgecolor='k')  # create a figure object
    
    plt.plot(phi, gain27 - param27.antenna_gain, "-b", label = "$f = 23.8$ $GHz$")

    plt.title("Envelope of ITU-R RS.1861 Figure 9c antenna radiation pattern")
    plt.xlabel("Off-axis angle $\phi$ [deg]")
    plt.ylabel("Gain relative to $G_m$ [dB]")
    plt.legend(loc="lower left")
    plt.xlim((phi[0], phi[-1]))
    plt.ylim((-80, 10))
    
    #ax = plt.gca()
    #ax.set_yticks([-30, -20, -10, 0])
    #ax.set_xticks(np.linspace(1, 9, 9).tolist() + np.linspace(10, 100, 10).tolist())

    plt.grid()
    plt.show()        