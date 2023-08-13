# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as signal
from pytc2.sistemas_lineales import bodePlot, pzmap, GroupDelay, analyze_sys, tf2sos_analog, pretty_print_SOS
from pytc2.general import Chebyshev_polynomials
from pytc2.sistemas_lineales import TransferFunction as tf

f_1 = 1600e3
f_2 = 2500e3
b_hz = f_2 - f_1
fofo = f_1*f_2
fo = np.sqrt(fofo)
alpha_max = 3
alpha_min = 20
gain = 10
fs1 = 1250e3
fs2 = 3200e3

b_normalizado = b_hz /fo
omega_1 = f_1/fo
omega_2 = f_2/fo
omega_stop_1 = fs1/fo
omega_stop_2 = fs2/fo


if omega_1*omega_2 == 1:
    print("se cumple con w1*w2 ==1")
else :
    print("no se cumple")
   
#tal vez siva para el butter del lp.
for order in range(1,6):
    juan = 10*np.log10(1+((13/6)**(2*order)))
    print(order, juan)
    
#adoptamos orden 3
plt.close('all')

z, p, k =signal.buttap(3)
num_lp, den_lp = signal.zpk2tf(z, p, k)
num_bp, den_bp = signal.lp2bp(num_lp, den_lp, bw = b_normalizado)
sos_bp = tf2sos_analog(num_bp, den_bp)
pretty_print_SOS(sos_bp, mode = 'omegayq')
##analyze_sys(signal.TransferFunction(num_bp, den_bp))



f_o = 50
b = 10
w_o = 2*np.pi*f_o
q = f_o/10

num_notch = [1, 0, (w_o**2)]
den_notch = [1, (w_o/q), (w_o**2)]
tf(num_notch, den_notch)
analyze_sys(tf(num_notch, den_notch))