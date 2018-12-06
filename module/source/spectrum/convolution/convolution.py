import os, glob, sys, warnings, array, re, math, time, copy
import numpy               as np
import matplotlib.pyplot   as plt
from   astropy.io          import fits
from   astropy.io          import ascii
from   scipy.interpolate   import interp2d, interp1d

class Convolution(object):

    def __init__(self, wave, flux, filter_name):
        self.wave = wave
        self.flux = flux
        self.filter_file = 'filters/' + self.filter_name + '_SDSS.res'

    def read_filter(self, file):
        data     = ascii.read(file)
        wavefilt = data['col1']
        fluxfilt = data['col2']
        fluxfilt = fluxfilt / np.amax(fluxfilt)
        return wavefilt, fluxfilt

    def load_zerofile(self):
        file         = 'alpha_lyr_stis_005.ascii'
        data         = ascii.read(file, comment='\s*#')
        npt          = len(data['col1'])
        zerosed      = np.recarray((npt,), dtype=[('wave', float),('flux', float)])
        zerosed.wave = data['col1']

        # Normalizing the SED@ 5556.0\AA
        zp5556       = 3.44E-9 #erg cm^-2 s^-1 A^-1, Hayes 1985
        zerosed.flux = 1.0/np.power(zerosed.wave, 2)
        return zerosed

    @property
    def magnitude(self):
        ''' Some constants to define'''
        cvel      = 2.99792458e18 # Speed of light in Angstron/sec
        dl        = 1E-5          # 10 pc in Mpc, z=0; for absolute magnitudes
        cfact     = 5.0 * np.log10(1.7684E8 * dl) # from lum[erg/s/A] to flux [erg/s/A/cm2]
        zerosed   = self.load_zerofile()
        interp_zp = interp1d(zerosed.wave, zerosed.flux)

        #Read the filter response

        wavefilt, fluxfilt = self.read_filter(self.filter_file)
        wave_eff           = np.sqrt(np.trapz(fluxfilt, x = wavefilt)/np.trapz(fluxfilt/np.power(wavefilt, 2), x = wavefilt))

        # Finding the wavelength limits of the filters

        good = (wavefilt > 0.0)
        wlow = np.amin(wavefilt[good])
        whi  = np.amax(wavefilt[good])

        # Selecting the relevant pixels in the input spectrum
        w        = (self.wavemod >= wlow) & (self.wavemod <= whi)
        tmp_wave = self.wavemod[w]
        tmp_flux = self.fluxmod[w]
        if np.amin(self.wavemod) > wlow or np.amax(self.wavemod) < whi:
           continue

        # Interpolate the filter response to data wavelength

        interp   = interp1d(wavefilt[good], fluxfilt[good])
        response = interp(tmp_wave)

        # Calculating the magnitude in the desired system

        vega   = interp_zp(tmp_wave)
        f      = np.trapz(tmp_flux * response, x = tmp_wave)/np.trapz(response, x = tmp_wave)
        vega_f = np.trapz(vega     * response, x = tmp_wave)
        mag    = -2.5 * np.log10(f/vega_f)
        fmag   = mag + cfact
        fmag   = fmag + 2.5*np.log10(cvel)-48.6 # oke & gunn 83

        return fmag
