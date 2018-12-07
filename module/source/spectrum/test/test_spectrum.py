#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 09:04:20 2018

@author: mckemmishgroup
"""
from spectrum import Spectrum
import numpy as np
#import argparse

#parser = argparse.ArgumentParser(description="Test a given .FITS file",
#										usage="test_spectrum.py --filepath datafile.fits")
#
#parser.add_argument("-f", "--filepath", help="the data file to be tested")
#
#args = parser.parse_args()
#
#test_spectrum_data = filepath

test_spectrum_data = 'spec-4055-55359-0001.fits'

def test_data_size():
    '''Test that the size of the file is what we expect'''
    s = Spectrum(test_spectrum_data)
    assert len(s.hdu_list) == 4, "Wrong number of headers"
    
def test_ra():
    ''' Test that we can read the right ra'''
    s = Spectrum(test_spectrum_data)
    np.testing.assert_approx_equal(s.ra, 237.74594)
    
def test_dec():
    '''Test that we can read the right dec'''
    s = Spectrum(test_spectrum_data)
    np.testing.assert_approx_equal(s.dec, 1.4850507)
    
def test_wavelength():
    '''Test wavelength is nonzero'''
    s = Spectrum(test_spectrum_data)
    assert len(s.wavelength > 0), "Wavelength empty"
    
def test_flux_presence():
    '''Test if flux has values'''
    s = Spectrum(test_spectrum_data)
    assert len(s.flux > 0), "No flux detected"
    
def test_flux_sign():
    ''' Checking for -ve flux'''
    s = Spectrum(test_spectrum_data)
    s_array = np.array(s.flux)
    assert np.all(s_array) >= 0, "Negative flux detected"
    
def test_color():
    '''Check if color returns'''
    s = Spectrum(test_spectrum_data)
    color = s.color('g', 'r')
    np.testing.assert_approx_equal(color, 0.4571685891215722) 
