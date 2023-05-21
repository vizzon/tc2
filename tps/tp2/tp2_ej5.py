# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as signal
from pytc2.sistemas_lineales import bodePlot, pzmap, GroupDelay, analyze_sys, tf2sos_analog
from pytc2.general import Chebyshev_polynomials
from pytc2.sistemas_lineales import TransferFunction as tf

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
    
z, p, k = signal.cheb1ap(5, alfa_max)

#print(p)
#print(z)
#print(k)
num, den = signal.zpk2tf(z, p, k)
print("numerador lp filter cheby \n",num)
print("denominador lp filter cheby\n", den)
den_hp = den[::-1]
num_hp = [num[0], 0, 0, 0, 0, 0]

print("numerador HP filter cheby \n",num_hp)
print("denominador HP filter cheby\n", den_hp)
roots_hp = np.roots(den_hp)
print("roots hp fileter: \n",roots_hp)

print("\n\n")
den_sos_1 = np.array([1, roots_hp[0]])
print(den_sos_1)
print("\n\n")

den_sos_2 = np.polymul(np.array([1, roots_hp[1]]), np.array([1, roots_hp[2]])).real
den_sos_2[1] = den_sos_2[1]*-1
print(den_sos_2)

l_1 = 1/den_sos_2[1]
c_1 = 1/(l_1*den_sos_2[2])

print("R: ", 1, "\nl_1: ", l_1, "\nc_1: ", c_1)

#analyze_sys(tf(num_hp, den_hp))















## tp2 ej3 
##poluy = Chebyshev_polynomials(5)
##print(poluy)
##cw = [16, 0, -20, 5, 0]
##robert = np.polymul(cw,cw) 
##robert = robert * ee
##robert[-1] = robert[-1] + 1
##print(robert)
##a = np.roots([1, 0, -640/256, 0, 560/256, 0, -200/256, 0, 25/256, 0, 1/(256*ee)])
##print(a)

