#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

import random

#f=open("ZrCuAg.in.dat","r")

'''
x = 0  #porcentaje atomos Ag
n_Ag = x * 320
n_Zr = int((100 - x)/2 * 320)
n_Cu = n_Zr 

'''
n_Ag = 2 * 320
n_Zr = 49 * 320
n_Cu = 49 * 320


a = zeros(32000, int)
for i in range(len(a)):
   a[i] = i + 10
shuffle(a)
f = open("ZrCuAg.init.dat","r")
o = open("salida","w")

ll = f.readlines()

for j in range(0,10):
    o.write(ll[j])



for j in  range(n_Zr):
    split = str.split(ll[a[j]])
    split[1] = "1"
    ll[a[j]] = split[0]+' '+split[1]+' '+split[2]+' '+split[3]+' '+split[4]

for j in  range(n_Zr, n_Zr+n_Cu):
    split = str.split(ll[a[j]])
    split[1] = "2"
    ll[a[j]] = split[0]+' '+split[1]+' '+split[2]+' '+split[3]+' '+split[4]

inicio = n_Zr
fin = n_Zr+n_Cu
for j in  range(inicio, fin):
    split = str.split(ll[a[j]])
    split[1] = "2"
    ll[a[j]] = split[0]+' '+split[1]+' '+split[2]+' '+split[3]+' '+split[4]

inicio = fin
fin = len(ll)-10
for j in  range(inicio, fin):
    split = str.split(ll[a[j]])
    split[1] = "3"
    ll[a[j]] = split[0]+' '+split[1]+' '+split[2]+' '+split[3]+' '+split[4]

for i in range(10, len(ll)):
    o.write(ll[i] + '\n')

f.close()
o.close()

cont_at = 0
cont_Zr = 0
cont_Cu = 0
cont_Ag = 0

for line in ll:
    split = str.split(line)
    if len(split) == 5:
       if split[1] == "1":
          cont_Zr += 1
       if split[1] == "2":
          cont_Cu += 1
       if split[1] == "3":
          cont_Ag += 1    
       cont_at += 1
print("*******************************************")
print("Numero de atomos:",  cont_at)
print(" ")
print("Elemento      Total         %")
print("   Zr        ",   cont_Zr, "      ", cont_Zr/320)
print("   Cu        ",   cont_Cu, "      ", cont_Cu/320)
print("   Ag         ",   cont_Ag, "      ", cont_Ag/320)
print("*******************************************")


#out.write(split[0]+' '+split[1]+' '+split[2]+' '+split[3]+' '+split[4]+' '+split[5]+' '+split[6]+'\n')

