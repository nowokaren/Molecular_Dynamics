import math
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib import colors, ticker, cm
import os

def RdF():
    # Function to calculate and analyze Radial Distribution Function (RDF)

    # Initialization of variables
    Razon = []  # List to store the ratio of gmax to gmin
    loop = 0
    gr = []  # Matrix to store RDF for each run
    coord = []  # List to store the coordination number
    temp = open('../temps', 'r')
    T = np.loadtxt(temp)
    tt = []  # List to store temperatures
    i = 0
    b = 0
    B0 = 0.9
    R0 = 0.2
    G0 = 0.9
    TT = 0.5
    R = R0
    G = G0
    B = B0

    # Extracting temperature data
    name = os.getcwd()
    name = name.split('\\')
    name = name[len(name) - 2] + ' ' + name[len(name) - 1]

    # Creating directory for plots
    os.mkdir('../Gráficos ' + name)

    # Reading log file to get information about atoms
    with open('../log.lammps', 'r') as log:
        for h, line in enumerate(log):
            if b == 1:
                s = line.split()
                break
            if 'reading' in line:
                b += 1
    atoms = int(s[0])

    # Reading volume data
    volumen = open('../volume', 'r')
    V = np.loadtxt(volumen)

    # Plotting RDF for each dump file
    for dump in arch:
        z = np.loadtxt(dump)
        r = z[:, 0]
        g = z[:, 1]

        gr.append(g)  # Matrix for each run

        # Plotting RDF for individual runs
        plt.figure('Radial distribution function' + name)
        plt.xlabel('r')
        plt.ylabel('g(r)')
        plt.plot(r, g, color=(R, G, B, TT))
        plt.savefig('../Gráficos ' + name + '/Radial distribution ' + name)

        if arch.index(dump) == len(arch) - 1:
            plt.clf()

        # Plotting RDF for a combined run
        plt.figure('Radial distribution function' + e)
        plt.xlabel('r')
        plt.ylabel('g(r)')
        plt.plot(r, g, color=(R, G, B, TT))
        plt.savefig('../Gráficos ' + e + '/Radial distribution ' + e)

        # Finding temperature from the dump file name
        t = (dump.split()[0][2] + dump.split()[0][3] + dump.split()[0][4] + dump.split()[0][5])
        i = 0
        while abs(T[i] - int(t)) > 1:
            i += 1
        tt.append(T[i])
        loop += 1

        # Calculating RDF integral: 4*pi*g(r)*r^2*dr
        a = name[len(name) - 1].split('v')[0]
        porc = int(name.split()[1])
        if a == '3':
            num = int(atoms * porc / 100)
        elif a == 'All':
            num = atoms
        else:
            num = int(atoms * (100 - porc) / 200)
        suma = 0
        Gr = [0]
        vol = V[tt.index(T[i])]
        imax = g.argmax()
        imin = imax + g[imax:].argmin()
        for i in range(0, len(r) - 1):
            suma += 4 * math.pi * (r[i] * r[i]) * ((r[i + 1]) - (r[i])) * g[i]
            Gr.append(suma * (num / vol))
        Razon.append(g[imax] / g[imin])

        # Plotting RDF integral
        plt.figure('Integral of radial distribution function' + e)
        plt.title('Integral of radial distribution function')
        plt.xlabel('r')
        plt.ylabel('Integral of g(r)')
        plt.plot(r, Gr, color=(R, G, B, TT))
        plt.savefig('../Gráficos ' + e + '/Integral of radial distribution function ' + e)

        plt.figure('Integral of radial distribution function' + name)
        plt.title('Integral of radial distribution function')
        plt.xlabel('r')
        plt.ylabel('Integral of g(r)')
        plt.plot(r, Gr, color=(R, G, B, TT))
        plt.savefig('../Gráficos ' + name + '/Integral of radial distribution function ' + name)

        if arch.index(dump) == len(arch) - 1:
            plt.clf()

        coord.append(Gr[imin - 1])

        # Adjusting color for the next run
        B += ((0.9 - B0) / len(arch))
        R += ((0.5 - R0) / len(arch))
        G += ((0.2 - G0) / len(arch))

        if arch.index(dump) == len(arch) - 1:
            plt.clf()

    # Plotting gmax/gmin ratio over temperature
    plt.figure('gmax/gmin ' + e)
    plt.ylabel('gmax/gmin')
    plt.title('Degree of amorphicity')
    plt.xlabel('Temperature [K]')
    plt.plot(tt, Razon, 'o')
    plt.savefig('../Gráficos ' + e + '/Degree of amorphicity R ' + e)

    plt.figure('gmax/gmin ' + name)
    plt.ylabel('gmax/gmin')
    plt.title('Degree of amorphicity')
    plt.xlabel('Temperature [K]')
    plt.plot(tt, Razon, 'o')
    plt.savefig('../Gráficos ' + name + '/Degree of amorphicity ' + name)
    plt.clf()

    # Plotting Cooling Rate
    plt.figure('Cooling Rate ' + e)
    plt.title('Radial distribution')
    plt.xlabel('r')
    plt.ylabel('Temperature [K]')
    R, T = np.meshgrid(r, tt)
    plt.contourf(R, T, gr)
    plt.savefig('../Gráficos ' + e + '/Run ' + e)

    plt.figure('Cooling Rate ' + name)
    plt.title('Radial distribution')
    plt.xlabel('r')
    plt.ylabel('Temperature [K]')
    R, T = np.meshgrid(r, tt)
    plt.contourf(R, T, gr)
    plt.savefig('../Gráficos ' + name + '/Run ' + name)
    plt.clf()

    # Displaying coordination number over temperature
    plt.figure('Coordination Number ' + e)
    plt.title('Coord
    # Displaying coordination number over temperature
    plt.figure('Coordination Number ' + e)
    plt.title('Coordination Number')
    plt.xlabel('Temperature [K]')
    plt.ylabel('Integral of g(r)')
    plt.plot(tt, coord, 'o')
    plt.savefig('../Gráficos ' + e + '/Coordination Number ' + e)

    plt.figure('Coordination Number ' + name)
    plt.title('Coordination Number')
    plt.xlabel('Temperature [K]')
    plt.ylabel('Coordination Number')
    plt.plot(tt, coord, 'o')
    plt.savefig('../Gráficos ' + name + '/Coordination Number ' + name)
    plt.clf()

# Calling the function
RdF()

