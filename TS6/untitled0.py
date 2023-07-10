#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 11:19:20 2023

@author: vizzon
"""
import numpy as np
from IPython.display import display, Markdown
import matplotlib.pyplot as plt
from scipy import signal as signal
from pytc2.sistemas_lineales import bodePlot, pzmap, GroupDelay, analyze_sys, tf2sos_analog, pretty_print_SOS
## setear en True para ver logs de dev
dev = False
plt.close('all')
wo = 300*2*np.pi
wo_n = 1
Q = 1
a = 1/9
c = 1
ee = 10**(1/10)-1
e = np.sqrt(ee)
omega_butt = (e**(-1/3))
num_lp = np.array([0, 0, 0, 1])
den_lp = np.array([1, 2, 2, 1])
num_lp_2 = np.array([0,0,0, omega_butt**3])
den_lp_2 = np.array([1, 2*omega_butt, 2*(omega_butt**2), 1*(omega_butt**3)])
#analyze_sys([signal.TransferFunction(num_lp, den_lp), signal.TransferFunction(num_lp_2, den_lp_2)])
#analyze_sys(signal.TransferFunction(num_lp_2, den_lp_2))
r_1 = 1e3
c_1 = 5.96e-9
omega_o = 1/(r_1*c_1)
num_ap_1 = np.array([1, -omega_o])
den_ap_1 = np.array([1, omega_o])
#analyze_sys(signal.TransferFunction(num_ap_1, den_ap_1))
juan = 2*(omega_o/((omega_o**2)+(2*np.pi*9200)**2))
##num_hp = np.array([c, 0, a, 0])
##den_hp = np.array([1, 2, 2, 1])
##analyze_sys([signal.TransferFunction(num_hp, den_hp)])

# Notch
omega_notch = 2*np.pi*50
num_notch = np.array([1, 0, omega_notch**2])
den_notch = np.array([1, omega_notch/10, omega_notch**2])
#analyze_sys([signal.TransferFunction(num_notch, den_notch)])

# Notch LP
omega_notch_lp = 2*np.pi*280
num_notch_lp = np.array([0.031, 0, np.sqrt(2)*omega_notch_lp**2])
den_notch_lp = np.array([1, omega_notch_lp*np.sqrt(2), omega_notch_lp**2])
#analyze_sys([signal.TransferFunction(num_notch_lp, den_notch_lp)])

# OTA 
num_ota_hp = np.array([1, 0, 0])
den_ota_hp = np.array([1, 1, 1])
#analyze_sys([signal.TransferFunction(num_ota_hp, den_ota_hp)])
