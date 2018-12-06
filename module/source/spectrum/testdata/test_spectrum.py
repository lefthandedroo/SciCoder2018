#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 09:04:20 2018

@author: mckemmishgroup
"""
from ..spectrum import Spectrum
import numpy as np

test_spectrum_data = 'spec-4055-55359-0001.fits'

def test_data_size():
    '''Test that the size of the file is what we expect'''
    s = Spectrum(test_spectrum_data)
    assert len(s.hud_list) == 4, "Wrong number of headers"
    
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
    assert s.flux >= 0, "Negative flux detected"