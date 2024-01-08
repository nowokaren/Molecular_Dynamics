import math
import numpy as np
from matplotlib import pyplot as plt
import os

def RdF():
    # Function for Radial Distribution Function (RDF) analysis

    razon = []  # List to store gmax/gmin ratio
    loop = 0
    gr = []  # Matrix to store RDF for each run
    temp = open('../temps', 'r')
    T = np.loadtxt(temp)
    tt = []
    i = 0
    b = 0
    B0 = 0.9
    R0 = 0.2
    G0 = 0.9
    TT = 0.5
    R = R0
    G = G0
    B = B0

    # Save the run name
    name = os.getcwd()
    name = name.split('\\')
    name = name[len(name) - 2] + ' ' + name[len(name) - 1]

    # Create arch: list of gr files
    arch = os.listdir()
    arch.pop(len(arch) - 1)

    while b != len(arch):
        if arch[b].split('r')[0] != 'g':
            arch.pop(b)
        else:
            b += 1

    os.mkdir('../Gráficos ' + name)

    e = 'union'

    # Graphs
    for dump in arch:
        z = np.loadtxt(dump)
        r = z[:, 0]
        g = z[:, 1]

        gr.append(g)  # Matrix for each run

        # Calculate gmax/gmin
        j = 0
        k = 0
        gmax = max(g)
        while g[k] != gmax:
            k += 1
        gmin = min(g[k:len(g)])
        while g[j] != gmin:
            j += 1
        razon.append(gmax / gmin)

        # Plot RDF for individual runs
        plt.figure('Radial distribution function' + name)
        plt.xlabel('r')
        plt.ylabel('g(r)')
        plt.plot(r, g, color=(R, G, B, TT))
        plt.savefig('../Gráficos ' + name + '/Radial distribution ' + name)

        if arch.index(dump) == len(arch) - 1:
            plt.clf()

        # Plot RDF for a combined run
        plt.figure('Radial distribution function' + e)
        plt.xlabel('r')
        plt.ylabel('g(r)')
        plt.plot(r, g, color=(R, G, B, TT))
        plt.savefig('../Gráficos ' + e + '/Radial distribution ' + e)

        # Trapezoidal Rule Integration
        h = r[1] - r[0]
        suma = 0
        Gr = [0]
        for i in range(0, len(r) - 1):
            suma = (h * h + h * abs(g[i + 1] - g[i])) * 2 * math.pi * (((r[i + 1] - r[i]) / 2) ** 2) + suma
            Gr.append(suma)

        # Save the integral plot
        plt.figure('Integral of radial distribution function' + e)
        plt.title('')
        plt.xlabel('r')
        plt.ylabel('Integral of g(r)')
        plt.plot(r, Gr, color=(R, G, B, TT))
        plt.savefig('../Gráficos ' + e + '/Integral of radial distribution function ' + e)

        plt.figure('Integral of radial distribution function' + name)
        plt.title('')
        plt.xlabel('r')
        plt.ylabel('Integral of g(r)')
        plt.plot(r, Gr, color=(R, G, B, TT))
        plt.savefig('../Gráficos ' + name + '/Integral of radial distribution function ' + name)

        t = (dump.split()[0][2] + dump.split()[0][3] + dump.split()[0][4] + dump.split()[0][5])

        i = 0
        while abs(T[i] - int(t)) > 1:
            i += 1
        tt.append(T[i])
        loop += 1

        # Adjust color for the next run
        B += ((0.9 - B0) / len(arch))
        R += ((0.5 - R0) / len(arch))
        G += ((0.2 - G0) / len(arch))

        if arch.index(dump) == len(arch) - 1:
            plt.clf()

    # Plot gmax/gmin ratio over temperature
    plt.figure('gmax/gmin' + e)
    plt.ylabel('gmax/gmin')
    plt.xlabel('Temperature [K]')
    plt.plot(tt[::-1], razon, 'o')
    plt.savefig('../Gráficos ' + e + '/Degree of amorphicity ' + e)

    plt.figure('gmax/gmin' + name)
    plt.ylabel('gmax/gmin')
    plt.xlabel('Temperature [K]')
    plt.plot(tt[::-1], razon, 'o')
    plt.savefig('../Gráficos ' + name + '/Degree of amorphicity ' + name)
    plt.clf()

    # Plot Cooling Rate
    plt.figure('Cooling Rate' + e)
    plt.title('Radial distribution')
    plt.xlabel('r')
    plt.ylabel('Temperature [K]')
    R, T = np.meshgrid(r, tt)
    plt.contourf(R, T, gr)
    plt.savefig('../Gráficos ' + e + '/Run ' + e)

    plt.figure('Cooling Rate' + name)
    plt.title('Radial distribution')
    plt.xlabel('r')
    plt.ylabel('Temperature [K]')
    R, T = np.meshgrid(r, tt)
    plt.contourf(R, T, gr)
    plt.savefig('../Gráficos ' + name + '/Run ' + name)
    plt.clf()

# Calling the function
RdF()
