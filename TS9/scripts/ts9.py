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
fs = 1000 # Hz
nyq_frec = fs / 2

############################## Plantilla
# filter design
ripple = 0.5 # dB
gpass= 0.5
atenuacion = 40 # dB
ws1 = 1.0 #Hz
wp1 = 5.0 #Hz
wp2 = 25.0 #Hz
ws2 = 30.0 #Hz

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

############################################### FILTRO FIR ##############################
#Usar cualquiera de las siguientes o el de ventana (suboptimo)
numtaps =  701
frecs = [0, ws1, wp1, wp2, ws2, nyq_frec]
gains = [-np.inf, -np.inf, ripple, ripple, -atenuacion, -np.inf]
gains = 10**(np.array(gains)/20)


coef = sig.firls(numtaps, frecs, gains, fs = fs)

wz, hz = sig.freqz(coef, 1.0)

fig, axes = plt.subplots(2, 1, figsize = (15, 15))
axes[0].set_title('Modulo')
axes[0].plot(wz*fs/(2*np.pi), 20*np.log10(hz))
axes[0].grid()
#sig.remez(numtaps, bands, desired)
#La respuesta al impulso son los propios coefcientes ya que denominador=1

#le duele mucho y la verdad no se acerca realemente a lo que quiero, vamos por 
# ventanas

# FIR re-design
cant_coef = 5001
gains = [0,0, 1, 1, 0, 0]
num_bh = sig.firwin2(cant_coef, frecs, gains , window='blackmanharris', antisymmetric=True, fs=fs)
num_hm = sig.firwin2(cant_coef, frecs, gains , window='hamming', antisymmetric=True, fs=fs )
num_ka = sig.firwin2(cant_coef, frecs, gains , window=('kaiser',14), antisymmetric=True, fs=fs)

wz_bh, hz_bh = sig.freqz(num_bh, 1.0)
wz_hm, hz_hm = sig.freqz(num_hm, 1.0)
wz_ka, hz_ka = sig.freqz(num_ka, 1.0)

fig_fir, axes_fir = plt.subplots(2, 1, figsize = (15, 15))
axes_fir[0].set_title('Modulo')
axes_fir[0].plot(wz_bh*fs/(2*np.pi), 20*np.log10(hz_bh))
axes_fir[0].plot(wz_hm*fs/(2*np.pi), 20*np.log10(hz_hm))
axes_fir[0].plot(wz_ka*fs/(2*np.pi), 20*np.log10(hz_ka))
axes_fir[0].grid()
#axes_fir[0].set_ylim([-40, 1])

############################################### PARTE 2 ##############################
# Se deben usar los coeficientes del SOS.


###  TPL



