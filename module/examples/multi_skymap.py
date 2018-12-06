#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 15:25:19 2018

@author: mckemmishgroup
"""

import matplotlib.pyplot as plt
import astropy.units as u
import astropy.coordinates as coord
import argparse
import glob

from spectrum import Spectrum

parser = argparse.ArgumentParser(description="Plot a skymap of given file",
										usage="multi_skymap.py --file directory")

parser.add_argument("-f", "--filepath", help="the data file to be read")

args = parser.parse_args()

# filepath = '/Users/Shannon/Desktop/SciCoder/SciCoder-2018-Sydney/Data Files/spectra/'

files = glob.glob(filepath+'*.fits', recursive=True)

skymap = plt.figure(figsize=(12,6))
ax = skymap.add_subplot(111, projection="mollweide")
    
for file in files: 
    
    s = Spectrum(file)

    sc = ax.scatter(coord.Angle(s.ra*u.degree).wrap_at(180*u.degree).radian, coord.Angle(s.dec*u.degree).radian, 
    				marker="*", s=200, c=s.color('g', 'r'), cmap=plt.get_cmap("rainbow"), vmin=0, vmax=1)
    
plt.colorbar(sc, fraction=0.025, pad=0.04)
plt.title("Title", fontsize=16, y=1.05)
txt = r'Caption'
skymap.text(.49,.05,txt, fontsize=8, horizontalalignment='center')
ax.grid(True)
ax.set_axisbelow(True)

skymap.savefig("skymap_all.pdf")
