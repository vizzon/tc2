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

print("hola")
alfa_max = 1
alfa_min = 54
wp = 1
ws = 3.75


ee = (10**(alfa_max/10)-1)
e = np.sqrt(ee)
print(ee)
print(e)

n = 1
for n in range(1, 10, 1):
    marta = 10*np.log10(1+ee*(np.cosh(n*np.arccosh(3.75))**2))
    carlos = 10*np.log10(1+ee*(ws**(2*n)))
    print("cheby is: ", marta, "order is: ", n, "maxima planicidad: ", carlos)
    
den_mod = np.array([1, 0, 2, 0, 5/4, 0, 1/4, 0, (1+(1/ee))/64])
roots = np.roots(den_mod)
den_1 = np.polymul(np.array([1, roots[2]]), [1, roots[3]])
den_2 = np.polymul(np.array([1, roots[6]]), [1, roots[7]])

num_sos_1 = [0, 0, np.sqrt(1/(8*e))]
den_sos_1 = np.abs(den_1)
num_sos_2 = [0, 0, np.sqrt(1/(8*e))]
den_sos_2 = np.abs(den_2)

den_hp_sos_1 = np.array([1, den_sos_1[1]/den_sos_1[2], 1/den_sos_1[2]])
num_hp_sos_1 = np.array([1/den_sos_1[2], 0, 0])    
#analyze_sys([signal.TransferFunction(num_hp_sos_1, den_hp_sos_1)])

den_hp_sos_2 = np.array([1, den_sos_2[1]/den_sos_2[2], 1/den_sos_2[2]])
num_hp_sos_2 = np.array([1/den_sos_2[2], 0, 0])    
#analyze_sys([signal.TransferFunction(num_hp_sos_1, den_hp_sos_1)])


z, p, k = signal.cheb1ap(4, alfa_max)
num_complete_lp, den_complete_lp = signal.zpk2tf(z, p, k)
num, den =  signal.lp2hp(num_complete_lp, den_complete_lp)
juan = tf2sos_analog(num, den)
