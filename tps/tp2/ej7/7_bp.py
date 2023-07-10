# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as signal
from pytc2.sistemas_lineales import bodePlot, pzmap, GroupDelay, analyze_sys, tf2sos_analog, pretty_print_SOS
## setear en True para ver logs de dev
dev = False
plt.close('all')
print("hola")
alfa_max = 3
alfa_min = 20
wp = 1
Q = 1 /(1.25-0.8)
ws_1 = Q*(1.6**2 -1)/1.6

ee = (10**(alfa_max/10)-1)
e = np.sqrt(ee)
print(ee)
print(e)

n = 1
for n in range(1, 10, 1):
    marta = 10*np.log10(1+ee*(np.cosh(n*np.arccosh(ws_1))**2))
    carlos = 10*np.log10(1+ee*(ws_1**(2*n)))
    print("cheby is: ", marta, "order is: ", n, "maxima planicidad: ", carlos)
    
num_lp_fos = np.array([0, 1])
den_lp_fos = np.array([1, 1])

num_fos_bp_1 = np.array([0, 1/Q, 0])
den_fos_bp_1 = np.array([1, 1/Q, 1])
#analyze_sys(signal.TransferFunction(num_fos_bp_1, den_fos_bp_1), sys_name="Primer Etapa")
#so far so good.


num_bp_complete = np.array([0, 0,    1/Q**2,   0,   0])
den_bp_complete = np.array([1, 1/Q, (2+1/Q**2), 1/Q, 1])
sos_2  = tf2sos_analog(num_bp_complete, den_bp_complete)
#analyze_sys(signal.TransferFunction(num_bp_complete, den_bp_complete), sys_name="Segunda y tercera Etapa")
sos_1 = tf2sos_analog(num_fos_bp_1, den_fos_bp_1)
sos = np.vstack((sos_1, sos_2))
analyze_sys(sos)
roots = np.roots(den_bp_complete)

z, p, k = signal.buttap(3)
num_complete_lp, den_complete_lp = signal.zpk2tf(z, p, k)
num, den  = signal.lp2bp(num_complete_lp, den_complete_lp, bw=(1/Q))
roots_by_buttapp = np.roots(den)
juan = tf2sos_analog(num, den)
#analyze_sys(signal.TransferFunction(num, den), sys_name="Etapas concatenadas")
#num, den =  signal.lp2hp(num_complete_lp, den_complete_lp)
#juan = tf2sos_analog(num, den)
