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


## CHANGE TO YOUR OWN FILEPATH
#filepath = '/Users/mckemmishgroup/Anna/SciCoder/SciCoder-2018-Sydney/Data Files/spectra/'

parser = argparse.ArgumentParser(description="Plot spectra of given file",
                                 usage="multi_skymap.py --filepath /Users/mckemmishgroup/Anna/SciCoder/SciCoder-2018-Sydney/Data\ Files/spectra/")

parser.add_argument("-f", "--filepath", help="path to directory with multiple .fits files")

args = parser.parse_args()

if args.filepath is None:
    args.filepath = input("Please specify path to multiple .fits files? ")

files = glob.glob(args.filepath+'*.fits', recursive=True)

skymap = plt.figure(figsize=(12,6))
ax = skymap.add_subplot(111, projection="mollweide")
    
for file in files: 
    
    s = Spectrum(file)

    sc = ax.scatter(coord.Angle(s.ra*u.degree).wrap_at(180*u.degree).radian, coord.Angle(s.dec*u.degree).radian, 
    				marker="*", s=200, c=s.color('g', 'r'), cmap=plt.get_cmap("rainbow"), vmin=0, vmax=1)
    
plt.colorbar(sc, fraction=0.025, pad=0.04)
plt.title("Title", fontsize=16, y=1.05)
caption = r'Caption'
skymap.text(.49,.05,caption, fontsize=8, horizontalalignment='center')
ax.grid(True)
ax.set_axisbelow(True)

skymap.savefig("skymap_all.pdf")
