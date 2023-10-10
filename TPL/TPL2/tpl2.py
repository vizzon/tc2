#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 20:47:48 2023

@author: 
"""
# Inicialización e importación de módulos

# Módulos para Jupyter
import warnings
warnings.filterwarnings('ignore')

# Módulos importantantes
import scipy.signal as sig
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.io as sio
from pytc2.sistemas_lineales import plot_plantilla

# de sucios nomas, cerramos todos los plots que puedan haber abiertos
plt.close('all')

############################## Nyquist
fs = 40000 # Hz
nyq_frec = fs / 2

############################## Plantilla
# filter design
ripple = 0.5 # dB
gpass= 0.5
atenuacion = 40 # dB
ws1 = 2000 #Hz
wp1 = 4000 #Hz
wp2 = 6000 #Hz
ws2 = 8000 #Hz

############################################### FILTRO IIR ##############################

############################### Diseño del filtro sos
H_z = sig.iirdesign(wp=[wp1,wp2], ws=[ws1,ws2], gpass=gpass,
                           gstop=atenuacion, analog=False, ftype='butter', output='sos', fs=fs)

############################### Diseño del filtro ba
numZ, denZ = sig.iirdesign(wp=[wp1,wp2], ws=[ws1,ws2], gpass=gpass,
                           gstop=atenuacion, analog=False, ftype='butter', output='ba', fs=fs)

print(len(numZ))

############################## Respuesta para sos
wrad, hh = sig.sosfreqz(H_z, worN=1000)
ww = wrad / np.pi
############################## Respuesta para ba
wrad2, hh2 = sig.freqz(numZ, denZ, worN=1000)
ww2 = wrad2 / np.pi

############################# Visualizacion
#Grafico de modulo
#plt.figure(1)
#plt.plot(ww,20*np.log10(np.abs(hh)))
#plt.plot(ww2,20*np.log10(np.abs(hh2)))
#plt.title('IIR filter')
#plt.xlabel('Frecuencia')
#plt.ylabel('Modulo [dB]')
#plt.grid(which='both',axis='both')

#Gráfico de fase 
#plt.figure(2)
#plt.plot(ww,20*np.log10(np.angle(hh)))
#plt.plot(ww2,20*np.log10(np.angle(hh2)))
#plt.title('IIR filter')
#plt.xlabel('Frecuencia')
#plt.ylabel('Fase')
#plt.grid(which='both',axis='both')

#Para calcular la respuesta al impulso:
    #A) Antitransformada Z da el impulso (buscando equivalencias, tabla etc.)
    #B) Teniendo la respuesta al impulso en modulo y fase (numericamente) se puede realizar
    #   la transformada de Fourier discreta.

####################################### FILTRO B ##############################
# Elimina banda por el metodo de los minimos cuadrados.
#Usar cualquiera de las siguientes o el de ventana (suboptimo)
alpha_min=20
alpha_max=1
numtaps =  51
frecs = [0, 2000, 4000, 6000, 8000, nyq_frec]
gains = [-alpha_max, -alpha_max, -alpha_min, -alpha_min, -alpha_max, -alpha_max]
gains = 10**(np.array(gains)/20)

coef = sig.firls(numtaps, frecs, gains, fs = fs)

wz, hz = sig.freqz(coef, 1.0)

fig, axes = plt.subplots(2, 1, figsize = (15, 15))
axes[0].set_title('Modulo')
axes[0].plot(wz*fs/(2*np.pi), 20*np.log10(hz))
axes[0].plot(frecs, 20*np.log10(gains), 'rx', label='plantilla')
axes[0].grid()




############################ FILTRO A #########################################
lp_taps = 51
lp_frecs = [0, 1000, 2000, nyq_frec]
lp_gains_db = [-1, -20]
lp_gains_db_2 = [-1, -1, -20, -20]
lp_gains_vs = 10**(np.array(lp_gains_db)/20) 
lp_coef = sig.remez(lp_taps, lp_frecs, lp_gains_vs, fs = fs)

wz_lp, hz_lp = sig.freqz(lp_coef, 1.0)

fig_fir, axes_fir = plt.subplots(2, 1, figsize = (15, 15))
axes_fir[0].set_title('Modulo')
axes_fir[0].plot(wz_lp*fs/(2*np.pi), 20*np.log10(hz_lp))
axes_fir[0].plot(lp_frecs, lp_gains_db_2, 'rx', label='plantilla')
axes_fir[0].grid()


###################################### FILTRO C  ##############################
frecs_c = [0, 1000, 6000, nyq_frec]
gains_c = [-1, -1, -20, -np.inf]
numZ, denZ = sig.iirdesign(
    wp=1000, 
    ws=6000, 
    gpass=1,
    gstop=20, 
    analog=False, 
    ftype='butter', 
    output='ba', 
    fs=fs
    )

wz_lp_2, hz_lp_2 = sig.freqz(numZ, denZ)
fig_c, axes_c = plt.subplots(2, 1, figsize = (15, 15))
axes_c[0].set_title('Modulo')
axes_c[0].plot(wz_lp_2*fs/(2*np.pi), 20*np.log10(hz_lp_2))
axes_c[0].plot(frecs_c, gains_c, 'rx', label='plantilla')
axes_c[0].grid()



############# cosas que medimos
freqs_base_line = np.array([500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000])
times_base_line = np.array([1.76e-3, 770e-6, 260e-6, 96e-6, 260e-6, 152e-6, 88e-6, 40e-6, 6e-6, -28e-6, -48e-6, -18e-6])
vi_base_line = np.array([3.08, 3.08, 3.08, 3, 3, 2.92, 2.88, 2.8, 2.76, 2.68, 2.68, 2.6,  2.6])
vo_base_line = np.array([3, 3, 2.76, 2.48, 2.20, 1.92, 1.68, 1.52, 1.32, 1.16, 1.04, 0.92, 0.84])

freqs_filter_a = np.array([500, 1000, 1500, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000])
vi_filter_a = np.array(   [3.08, 3.08, 3.08, 3,    3,     2.92,  2.88, 2.8,  2.76,  2.68,  2.68, 2.6])
vo_filter_a = np.array(   [2.76, 2.68, 1.96, 0.92, 0.216, 0.216, 0.2,  0.16, 0.184, 0.12,  0.15, 0.088])
times_filter_a = np.array([300e-6, 260e-6, 300e-6, 290e-6, 290e-6, 40e-6, 90e-6, 120e-6, 0, -36e-6, 60e-6, -20e-6])
#phase = np.array([180, 141.12, 139.104, 136.224, 136.08, 133.2, 226, 218.88, 180, 180])

################# filtro b, stop band
freqs_filter_b = np.array([500,    1000,   2000,   2500,   3000,   3500,   4000,   5000,   6000,   6500,  7000, 7500,   8000, 10000])
vi_filter_b = np.array(   [3.08,   3.08,   3.04,   3,      3,      2.96,   3,      2.92,   2.88,   2.8,    2.8,  2.8,   2.62,  2.64])
vo_filter_b = np.array(   [2.68,   2.64,    2.48,   2.24,   1.76,   1.08,   0.6,    0.24,   0.24,   0.22,  0.22, 0.3,   0.5,   0.9 ])
times_filter_a = np.array([280e-6, 300e-6, 290e-6, 100e-6, -40e-3, -10e-6, -44e-6, 108e-6, 120e-6, 132e-6, 4e-6, 16e-6, 32e-6, 80e-6])



################# filtro c, low pas iir
freqs_filter_c = np.array([500,    1000,   2000,   4000,  6000,   10000])
vi_filter_c = np.array(   [3.08,   3.08,   3.04,   2.96,  2.84,   2.64])
vo_filter_c = np.array(   [2.68,   2.64,   2.40,   0.52,  0.184,  0.848])
times_filter_c = np.array([300e-6, 320e-6, 290e-6, 40e-6, 120e-6, 80e-6])

amp_base_line = 20*np.log10(vo_base_line/vi_base_line)
amp_filter_a = 20*np.log10(vo_filter_a/vi_filter_a)
amp_filter_b = 20*np.log10(vo_filter_b/vi_filter_b)
amp_filter_c = 20*np.log10(vo_filter_c/vi_filter_c)




#ret = -np.diff(phase)/np.diff(f)
#ret = np.insert(ret, 0,0,axis = 0)

fig_4, axes_base_line = plt.subplots(2, 1, figsize = (30, 30))
axes_base_line[0].set_title('Modulo')
axes_base_line[0].plot(freqs_base_line, amp_base_line, label='Transferencia en vacio')
axes_base_line[0].plot(freqs_filter_a, amp_filter_a, label='Transferencia Filtro A')
axes_base_line[0].plot(freqs_filter_b, amp_filter_b, label='Transferencia Filtro B')
axes_base_line[0].plot(freqs_filter_c, amp_filter_c, label='Transferencia Filtro C')

axes_base_line[0].grid()

