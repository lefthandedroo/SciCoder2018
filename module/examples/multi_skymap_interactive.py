#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 15:25:19 2018

@author: mckemmishgroup
"""
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.coordinates as coord
from astropy.io import ascii

data = ascii.read("values.txt")
ra = coord.Angle(data['ra']*u.degree).wrap_at(180*u.degree).radian
dec = coord.Angle(data['dec']*u.degree).radian
c = data['colour']
NaNs = np.isnan(c)
c[NaNs] = 0

file = data['file']

cmap = plt.get_cmap("rainbow")
norm=plt.Normalize(1,4)

skymap = plt.figure(figsize=(12,6))
ax = skymap.add_subplot(111, projection="mollweide")
sc = ax.scatter(ra, dec, marker="*", s=200, c=c, cmap=cmap, vmin=0, vmax=1)
plt.colorbar(sc, fraction=0.025, pad=0.04)
plt.title("Title", fontsize=16, y=1.05)
txt = r'Caption'
skymap.text(.49,.05,txt, fontsize=8, horizontalalignment='center')
ax.grid(True)
ax.set_axisbelow(True)

annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
					bbox=dict(boxstyle="round", fc="w"), arrowprops = dict(arrowstyle="->"))
annot.set_visible(False)

def update_annot(ind):
	pos = sc.get_offsets()[ind["ind"][0]]
	annot.xy = pos
	text = "{}".format("\n".join([file[n] for n in ind["ind"]]))
	annot.set_text(text)
	annot.get_bbox_patch().set_facecolor(cmap(c[ind["ind"][0]]))
	annot.get_bbox_patch().set_alpha(1.0)

def hover(event):
	vis = annot.get_visible()
	if event.inaxes == ax:
		cont, ind = sc.contains(event)
		if cont:
			update_annot(ind)
			annot.set_visible(True)
			skymap.canvas.draw_idle()
		else:
			if vis:
				annot.set_visible(False)
				skymap.canvas.draw_idle()

skymap.canvas.mpl_connect("motion_notify_event", hover)

plt.show()