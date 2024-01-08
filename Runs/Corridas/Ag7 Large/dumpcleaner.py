#!/usr/bin/env python

from pylab import *


infile = open('dumpAg7prueba.lammpstrj', 'r')
key = 'ITEM: TIMESTEP'
interval = 4
loop = interval
p = 0
dumpsI = 0
dumpsF = 0
#leer cantidad de atomos

for j, linea in enumerate(infile):
  if j == 3:
    a = linea.split()
    atoms=a[0] 
    break
infile.close()

k=(int(atoms)+9)

# copiar

fd = open('dumpfiltrado.dat', 'w')
with open('dumpAg7prueba.lammpstrj', 'r') as fp:
    for i, line in enumerate(fp):
      if key in line:
          loop += 1
          dumpsI += 1
      if loop == interval + 1:
          p += 1
          fd.write(line)
          if p == k:
             loop = 0
             p = 0
             dumpsF += 1
        
print('Cantidad inicial de dumps: ', dumpsI)  
print('Cantidad final de dumps: ', dumpsF)

fd.close()
