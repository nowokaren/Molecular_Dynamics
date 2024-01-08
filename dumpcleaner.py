#!/usr/bin/env python

from pylab import *


infile = open('log.lammps', 'r')
inicio = 'Step'
fin = 'Loop'
labels = []
count = 0
loop = 0

for linea in infile:
   if inicio in linea:
     words = linea.split()
     labels = words
     loop +=1
     linea1 = count
     print(linea1)
   if fin in linea:
     linea2 = count
     print(linea2)
   count +=1
infile.close()

fd = open('corrida.dat', 'w')
with open('log.lammps', 'r') as fp:
    for i, line in enumerate(fp):
        if (i > linea1) & (i < linea2) :
           fd.write(line)
fp.close()
fd.close()
