# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as signal
from pytc2.sistemas_lineales import bodePlot, pzmap, GroupDelay, analyze_sys

print("hola")
alfa_max = 0.4
alfa_min = 48
wp = 1
ws = 3


ee =  round((10**(alfa_max/10)-1), 3)
e = ee**0.5
print(ee)
print(e)

n = 1
for n in range(1, 10, 1):
    cheby = 10*np.log10(1+ee*(np.cosh(n*np.arccosh(3))**2))
    butter = 10*np.log10(1+ee*(ws**(2*n)))
    print("order is: ", n, "alpha para butter: ", butter, "alpha para cheby: ", cheby)
    
z, p, k = signal.cheb1ap(5, e)
print(p)
print(z)
print(k)