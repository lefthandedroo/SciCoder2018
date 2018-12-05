
from astropy.io import fits


class Spectrum(object):

      def __init__(self, file):
          if filepath is None:
             raise SDSSFileNotSpecified("A spectrum file must "
                                        "be specified to create a spectrum.")
          self.data = fits.open(file)
          self._ra  = None
          self._dec = None
          self._flux = None
          self._wavelength = None

      @property
      def ra(self):
          ''' Returns the RA of this spectrum in degrees. '''
          if self._ra == None:
             self._ra = self.data[0].header["RA"]
          return self._ra

      @property
      def dec(self):
          ''' Returns the RA of this spectrum in degrees. '''
          if self._dec == None:
             self._dec = self.data[0].header["DEC"]
          return self._ra

      @property
      def wavelength(self):
          """Wavelength binning, linear bins."""
          if getattr(self,'_wavelength',None) is None:
              self._wavelength = 10**self.data[1].data['loglam']
          return self._wavelength

      @property
      def flux(self):
          if getattr(self,'_flux',None) is None:
              self._flux = self.data[1].data['flux']
          return self._flux
