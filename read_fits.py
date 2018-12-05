#!/usr/bin/env python

from astropy.io import fits

path = "../../SciCoder/SciCoder-2018-Sydney/Data Files/spectra/"

filename = "spec-10000-57346-0002.fits"

with fits.open(path + filename) as hdu_list:

	hdu1 = hdu_list[0]
	print(f"This file has {len(hdu_list)} HDUS.")
	print(hdu_list.info())
	
	for key, value in hdu1.header.items():
		print("{0} = {1}".format(key, value))