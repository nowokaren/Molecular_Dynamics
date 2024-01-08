import os
from pylab import *
import numpy as np

# Open the trajectory file for reading
infile = open('dumpAg0prueba.lammpstrj', 'r')
key = 'ITEM: TIMESTEP'
loop = 0
cont = 0
I = []  # List to store timesteps
g = 0
p = 0

# Read the number of atoms from the third line of the trajectory file
for j, linea in enumerate(infile):
    if j == 3:
        a = linea.split()
        atoms = a[0]
        break
infile.close()

k = (int(atoms) + 9)

# Copying trajectory files for each timestep
for t in range(1, 4):
    comp = str(t) + 'v' + str(t)
    os.mkdir(comp)
    
    # Open a new file for writing the modified trajectory
    fd = open(comp + '/dumpint.dat', 'w')
    
    # Find the length of each line in the trajectory file
    with open('dumpAg0prueba.lammpstrj', 'r') as fp:
        for i, line in enumerate(fp):
            if i == 10:
                k = len(line.split())
    
    # Copy data for the specific timestep to a new file
    with open('dumpAg0prueba.lammpstrj', 'r') as fp:
        for i, line in enumerate(fp):
            if key in line:
                loop += 1
            if loop == 1:
                atomos = cont
            L = line.split()
            if len(L) == k:
                if L[1] == str(t):
                    cont += 1
                    fd.write(line)
            else:
                fd.write(line)
    
    # Close the file after writing
    fd.close()
    
    # Open a new file for modifying atom count
    ff = open(comp + '/dump.dat', 'w')
    
    # Modify the atom count in the trajectory file
    with open(comp + '/dumpint.dat', 'r') as fl:
        for j, line in enumerate(fl):
            if str(atoms) in line:
                ff.write(str(atomos) + '\n')
            else:
                ff.write(line)
    
    # Initialize variables for timestep extraction
    g = 0
    p = 0
    
    # Extract timesteps from the modified trajectory
    with open(comp + '/dump.dat', 'r') as hh:
        for j, line in enumerate(hh):
            if key in line:
                g += 1
            if g == 1:
                p += 1
                if p == 2:
                    step = line.split()
                    I.append(step)
                    g = 0
                    p = 0
    
    # Extract information from the log file
    infile = open('log.lammps', 'r')
    inicio = 'Step'
    fin = 'Loop'
    labels = []
    count = 0
    loop = 0
    
    # Find the labels and line numbers in the log file
    for linea in infile:
        if inicio in linea:
            words = linea.split()
            labels = words
            loop += 1
            linea1 = count
        if fin in linea:
            linea2 = count
        count += 1
    infile.close()
    
    y = 0
    l = 0
    
    # Extract specific lines from the log file
    fd = open('loglog.dat', 'w')
    with open('log.lammps', 'r') as fp:
        for i, line in enumerate(fp):
            if 'Loop' in line:
                y = 0       
            if y == 1:
                fd.write(line)
            if 'Step' in line:
                y = 1
    
    # Close the file after writing
    fp.close()
    fd.close()
    
    # Initialize variables for temperature extraction
    s = [0]
    m = 0
    
    # Load data from the loglog file
    T = []
    z = np.loadtxt('loglog.dat')
    
    # Extract temperatures for each timestep
    with open('log.lammps', 'r') as log:
        for h, line in enumerate(log):
            if 'Step' in line:
                s = line.split()
    
    # Match timesteps and temperatures
    for i in range(len(z[:, 0])):
        if z[i, 0] == int(I[m][0]):
            m += 1
            T.append(z[i, s.index('Temp')])
    
    # Remove the temporary loglog file
    os.remove('loglog.dat')
    
    d = 0
    
    # Open and modify the trajectory file for each timestep
    with open(comp + '/dump.dat', 'r') as ff:
        for j, line in enumerate(ff):
            if key in line:
                new = open(comp + '/dump-' + str(T[d]) + '.dat', 'w')
                d += 1
            new.write(line)
    
    # Close the file after writing
    new.close()  
    ff.close()
    fl.close()
    
    # Remove temporary files
    os.remove(comp + '/dump.dat')
    fd.close()

# Close the final file after writing
fd.close()
