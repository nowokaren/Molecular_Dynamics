# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 14:06:40 2020

@author: karen
"""

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib import colors, ticker, cm
import os
arch=os.listdir()
arch.pop(len(arch)-1)
razon=[]
temp=[]
t=300
loop=0
gr=[]
for dump in arch:

    z=np.loadtxt(dump)
    r=z[:,0]
    g=z[:,1]
    Gr=z[:,2]
    temp.append(t)
    t += 500
    gr.append(g)
    
    j=0
    k=0
    gmax=max(g)
    while g[k] != gmax:
        k += 1    
    gmin=min(g[k:len(g)])
    while g[j] != gmin:
        j += 1
    razon.append(gmax/gmin)
        
    plt.figure('Radial distribution function')
    plt.xlabel('r')
    plt.ylabel('g(r)')
    plt.plot(r[k],g[k], 'bo')
    plt.plot(r[j],g[j], 'bo')
    plt.plot(r,g)
    
    plt.figure('Integral of radial distribution function')
    plt.xlabel('r')
    plt.ylabel('Integral of g(r)')   
    plt.plot(r,Gr)
    
    loop +=1
    
plt.figure('gmax/gmin')
plt.ylabel('gmax/gmin')
plt.xlabel('Temperatura [K]')
plt.plot(temp[::-1], razon, 'o')
#print('gr', gr)

plt.figure('Cooling Rate')
plt.title('Distribución radial')
plt.xlabel('r')
plt.ylabel('Temperatura [K]')
R, T = np.meshgrid(r, temp)
contourf(R, T, gr)


#R = np.arange(0, 1.1, 0.25)
##T = np.arange(300, 1700, 700)
#R, T = np.meshgrid(r, temp)
#print(np.shape(R), np.shape(T), len(gr))
#print(R, T)
#ax0.contourf(R, T, gr, rstride=1, cstride=1, cmap='hot')

#contourf(R, T, gr)