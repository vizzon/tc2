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

wo = 300*2*np.pi
wo_n = 1
Q = 1/np.sqrt(2)
a = 1/3
c = 1
num_lp = np.array([a, 0, c])
den_lp = np.array([1, wo_n/Q, wo_n**2])
#analyze_sys(signal.TransferFunction(num_lp, den_lp))
num_hp = np.array([c, 0, a])
den_hp = np.array([1, wo_n/Q, wo_n**2])
#analyze_sys(signal.TransferFunction(num_hp, den_hp))

num_hp_2 = np.array([c, 0, a*(wo**2)])
den_hp_2 = np.array([1, wo/Q, wo**2])
analyze_sys(signal.TransferFunction(num_hp_2, den_hp_2))