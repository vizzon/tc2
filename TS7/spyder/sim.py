#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 20:38:55 2021

@author: mariano

Matriz Admitancia Indefinida (MAI)
----------------------------------
Ejemplos de cálculo simbólico mediante MAI de una red T puenteada de R constante.

Referencias:
------------
Cap. 9. Avendaño L. Sistemas electrónicos Analógicos: Un enfoque matricial.
"""

import sympy as sp

from pytc2.cuadripolos import calc_MAI_impedance_ij, calc_MAI_vtransf_ij_mn, calc_MAI_ztransf_ij_mn
from pytc2.general import print_latex


# T puenteado cargado: red de R constante
# explicación:
'''    
+ Numeramos los polos de 0 a n=3

            |------Ya-------|
            |               |
    0-------+--G----2---G---3
                    |       |
                   Yb       G
                    |       |
    1---------------+--------
    
'''    

Ya, Yb, Yc = sp.symbols('Ya Yb Yc', complex=True)
G = sp.symbols('G', real=True, positive=True)

# Armo la MAI

#               Nodos: 0          1        2         3
Ymai = sp.Matrix([  
                    [  Ya,        -Ya,       0,      0],
                    [ -Ya,   Ya+Yb+Yc,     -Yb,    -Yc],
                    [   0,        -Yb,    G+Yb,     -G],
                    [   0,        -Yc,     -G,    G+Yc]
                 ])

con_detalles = False
#con_detalles = True

# Calculo la Z en el puerto de entrada a partir de la MAI
Zmai = calc_MAI_impedance_ij(Ymai, 0, 3, verbose=con_detalles)

# Aplico la condición de R constante
print('si consideramos:')
print('entonces')

print('Transferencia de tensión:')
Vmai = calc_MAI_vtransf_ij_mn(Ymai, 2, 3, 0, 3, verbose=con_detalles)
print(Vmai)
Vmai = sp.simplify(Vmai.subs(G, 1))
print(Vmai)
Vmai_Ya = sp.simplify(Vmai.subs(Ya, 1/Ya))
print(Vmai)
Vmai_Yb = sp.simplify(Vmai.subs(Ya, G**2/Yb))


#print('Transimpedancia:')
Zmai = calc_MAI_ztransf_ij_mn(Ymai, 0, 3, 0, 3, verbose=con_detalles)
Zmai = sp.simplify(Zmai.subs(G, 1))
Zmai_Ya = sp.simplify(Zmai.subs(Yb, G**2/Ya))
Zmai_Yb = sp.simplify(Zmai.subs(Ya, G**2/Yb))


