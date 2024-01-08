import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
import scipy
import os

def filtro(x, y, t):
    # Function to apply a moving average filter to data.
    # Parameters:
    # x: x-axis data
    # y: y-axis data
    # t: number of points for the moving average

    a = 0
    g = []
    o = 0
    # Applying the moving average to the y-axis data
    while o < len(y) - t * 2:
        for e in range(1, t + 1):
            a += y[e + o]
            o += 1
        g.append(a / t)
        a = 0
    
    a = 0
    gg = []
    o = 0
    # Applying the moving average to the x-axis data
    while o < len(x) - t * 2:
        for e in range(1, t + 1):
            a += x[e + o]
            o += 1
        gg.append(a / t)
        a = 0
    
    return gg, g

# Opening and reading the log file
infile = open('log.lammps', 'r')
inicio = 'Step'
fin = 'Loop'
labels = []
count = 0
loop = 0
name = os.getcwd()
name = name.split('\\')
os.mkdir('Gráficos Energía')

fd = open('datos_log.dat', 'w')
 
# Extracting relevant information from the log file
for linea in infile:
    if inicio in linea:
        labels = linea.split()
        loop += 1
        linea1 = count
    if fin in linea:
        linea2 = count
        if loop == 1:
            with open('log.lammps', 'r') as fp:
                for i, line in enumerate(fp):
                    if (i >= linea1) & (i < linea2):
                        fd.write(line)
        elif loop > 1:
            with open('log.lammps', 'r') as fp:
                for j, line in enumerate(fp):
                    if (j > linea1) & (j < linea2):
                        fd.write(line) 
    count += 1

infile.close()
fp.close()
fd.close()

# Loading data from the log file
data = np.loadtxt('datos_log.dat', skiprows=2)

# Extracting relevant columns from the data
step = data[:, labels.index('Step')]
temp = data[:, labels.index('Temp')]
Epot = data[:, labels.index('PotEng')] / 1000

# Plotting temperature ramp
plt.figure('Rampa de temperatura')
plt.title('Rampa de temperatura') 
plt.plot(step, temp, 'r')
plt.xlabel('Step')
plt.ylabel('Temperatura [K]')
plt.savefig('Gráficos Energía/Rampa de temperatura (' + name[len(name)-1] + ')')

# Plotting potential energy
plt.figure('Energía potencial')
plt.title('Energía potencial [keV]')
plt.plot(step, Epot)
plt.xlabel('Step')
plt.ylabel('Energía potencial [keV]')
plt.savefig('Gráficos Energía/Energía potencial (' + name[len(name)-1] + ')')

# Initializing variables for further analysis
m = 0
Tmin = 0
j = 0
Tmax = 0

# Finding temperature ranges for further analysis
while abs(Tmin - 400) >= 0.1:
    m += 1
    Tmin = temp[m]
   
while abs(Tmax - 1000) >= 0.1:    
    j += 1
    Tmax = temp[j]
    
x = temp[j:m]
y = Epot[j:m]
t = 10

# Applying the moving average filter to the temperature and potential energy data
[X, Y] = filtro(x, y, t)

# Plotting the phase diagram
plt.figure('Diagrama de fase')
plt.title('Diagrama de fase')
plt.plot(temp, Epot, 'g-')
plt.plot(x, y, 'r-')
plt.plot(X, Y, 'b-')
plt.xlabel('Temperatura [K]')
plt.ylabel('Energía potencial [keV]')

plt.figure('Diagrama de fase 2')
plt.title('Diagrama de fase')
plt.plot(X, Y, 'r-')
plt.xlabel('Temperatura [K]')
plt.ylabel('Energía potencial [keV]')

# ------------ SIN FILTRO --------------

# x,y = sin filtro

# plt.figure('Diagrama de fase 3')
# plt.title('Diagrama de fase')
# plt.plot(x,y)

# plt.xlabel('Temperatura [K]')
# plt.ylabel('Energía potencial [keV]')
# coef1=np.polyfit(x[0:int(len(x)/2)], y[0:int(len(x)/2)] ,1)
# polinomio1=np.poly1d(coef1)
# yfit1=polinomio1(x)
# plt.plot(x, yfit1)

# coef2=np.polyfit(x[int(len(x)/2)+1:len(x)], y[int(len(x)/2)+1:len(x)],1)
# polinomio2=np.poly1d(coef2)
# yfit2=polinomio2(x)
# plt.plot(x, yfit2)

# Tg=(coef2[1]-coef1[1])/(coef1[0]-coef2[0])
# print(Tg, 'sin filtro')

# ---------------------------------------

# coef1=np.polyfit(X[0:int(len(X)/2)], Y[0:int(len(X)/2)] ,1)
# polinomio1=np.poly1d(coef1)
# Yfit1=polinomio1(X)


# coef2=np.polyfit(X[int(len(X)/2)+1:len(X)], Y[int(len(X)/2)+1:len(X)],1)
# polinomio2=np.poly1d(coef2)
# Yfit2=polinomio2(X)


# Tg=(coef2[1]-coef1[1])/(coef1[0]-coef2[0])
# k=0
# To=Tg+10
# while To-Tg > 0 :
#      k += 1
#      To=X[k]
# s1=(X[k]+X[k-1])/2
# s2=(Y[k]+Y[k-1])/2

# plt.plot(X, Yfit1)
# plt.plot(X, Yfit2)
# plt.text(800,-153,'Tg= '+str("%.2f" % Tg),fontsize=12)
# plt.plot(s1, s2, 'mo')
# plt.savefig('Gráficos Energía/Diagrama de Fase ('+name[len(name)-1]+')')




# L=Tg+2
# l=Tg-2
# m=0
# Xg=0
# while abs(Xg-L) >= 1 :
#     m += 1
#     Xg=X[m]
# xg=0
# k=0
# while abs(xg-l) >= 1 :
#     k += 1
#     xg=X[k]
# p=2
# d=0
# while abs(coef1[0]-coef2[0])>0.001:
#     if abs(Yfit1[m]-Y[m])<abs(Yfit2[k]-Y[k]):
#         p+=2
#     else: p-=2
#     d=int(len(X)/2)+p
#     coef1=np.polyfit(X[0:d], Y[0:d] ,1)
#     polinomio1=np.poly1d(coef1)
#     Yfit1=polinomio1(X)
#     plt.plot(X, Yfit1)
    
#     coef2=np.polyfit(X[len(X)-d:len(X)], Y[len(X)-d:len(X)],1)
#     polinomio2=np.poly1d(coef2)
#     Yfit2=polinomio2(X)
#     plt.plot(X, Yfit2)
    
# Tg=(coef2[1]-coef1[1])/(coef1[0]-coef2[0])

# # k=9000
# # To=0
# # while abs(To-Tg) >= 0.05 :
# #     k += 1
# #     To=temp[k]
# # print(Epot[k])
# # print(temp[k])
# # print(k)
# # print(Tg)
# # plt.plot(temp[k],Epot[k], 'go')


# # plt.axes([.235, .55, .3, .3])

# # plt.plot(temp[17400:17900], Epot[17400:17900], 'r-')

# # coef1=np.polyfit(temp[14000:14589], Epot[14000:14589],1)
# # polinomio1=np.poly1d(coef1)
# # EpotFIT=polinomio1(temp)
# # plt.plot(temp[17400:17900], EpotFIT[17400:17900])

# # coef2=np.polyfit(temp[18621:21003], Epot[18621:21003],1)
# # polinomio2=np.poly1d(coef2)
# # EpotFIT=polinomio2(temp)
# # plt.plot(temp[17400:17900], EpotFIT[17400:17900])
# # plt.plot(temp[k],Epot[k], 'go')


# #Promedio de pendientes

# pasos=10   # cantidad de divisiones del intervalo
# espacios=[]

  
# for p in range(0,pasos):
#  plt.figure(p)
#  coef1=np.polyfit(temp[j-2000:j+p*esp], Epot[j-2000:j+p*esp],1)   #
#  polinomio1=np.poly1d(coef1)
#  EpotFIT=polinomio1(temp)
#  plt.plot(temp, EpotFIT)
#  coef2=np.polyfit(temp[m-p*esp:END], Epot[m-p*esp:END],1)
#  polinomio2=np.poly1d(coef2)
#  EpotFIT=polinomio2(temp)
#  plt.plot(temp, EpotFIT)
#  plt.plot(temp[j-2000:j+p*esp], Epot[j-2000:j+p*esp], '^')
#  plt.plot(temp[m-p*esp:END], Epot[m-p*esp:END], '^')
 
#  Tg=(coef2[1]-coef1[1])/(coef1[0]-coef2[0])
#  Tgs.append(Tg)
#  espacios.append(p)
#  k=9000
#  To=0
#  while abs(To-Tg) >= 0.3 :
#      k += 1
#      To=temp[k]
#  plt.plot(temp[k],Epot[k], 'bo')
#  plt.plot(temp, Epot, 'r-')
# print('Tgs= ', Tgs)

# plt.figure('Tgs')
# plt.plot(espacios, Tgs, '*-')
