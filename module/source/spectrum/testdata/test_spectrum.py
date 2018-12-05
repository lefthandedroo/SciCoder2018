#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 09:04:20 2018

@author: mckemmishgroup
"""
from ..spectrum import Spectrum

test_spectrum_data = 'spec-4055-55359-0001.fits'

def test_data_size():
    s = Spectrum(test_spectrum_data)
    assert len() > 0, "nothing read from file"