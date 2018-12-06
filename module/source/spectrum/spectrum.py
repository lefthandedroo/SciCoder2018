from .errors import SDSSFileNotSpecifiedException
from astropy.io import fits
from .convolution.convolution import Convolution


class Spectrum(object):

    def __init__(self, file):
        if file is None:
            raise SDSSFileNotSpecifiedException("A spectrum file must "
                                                "be specified to create a spectrum.")
        self.data = fits.open(file)
        self.hdu_list = None
        self._ra = None
        self._dec = None
        self._flux = None
        self._wavelength = None

    @property
    def hdu_list(self):
        """ Returns the HDU list of this file. """
        if self._hdu_list is None:
            self._hdu_list = self.data
        return self._hdu_list

    @property
    def ra(self):
        """ Returns the RA of this spectrum in degrees. """
        if self._ra is None:
            self._ra = self.data[0].header["PLUG_RA"]
        return self._ra

    @property
    def dec(self):
        """ Returns the DEC of this spectrum in degrees. """
        if self._dec is None:
            self._dec = self.data[0].header["PLUG_DEC"]
        return self._dec

    @property
    def wavelength(self):
        """Wavelength binning, linear bins."""
        if getattr(self, '_wavelength', None) is None:
            self._wavelength = 10 ** self.data[1].data['loglam']
        return self._wavelength

    @property
    def flux(self):
        if getattr(self, '_flux', None) is None:
            self._flux = self.data[1].data['flux']
        return self._flux

    def plot(self, name_figure):
        """ Creates a plot of the spectrum """
        import matplotlib.pyplot as plt
        # Bunch of things so the plot looks nice. Nothing to do here.

        plt.rcParams['axes.linewidth'] = 1.5
        font = {'family': 'serif', 'size': 15}
        scatter_kwargs = {"zorder": 100}
        error_kwargs = {"lw": .5, "zorder": 0}
        plt.rc('font', **font)
        fig, axes = plt.subplots(1, figsize=(8, 7))
        plt.rcParams['xtick.major.size'] = 8
        plt.rcParams['xtick.major.width'] = 1.8
        plt.rcParams['xtick.minor.size'] = 5
        plt.rcParams['xtick.minor.width'] = 1.3
        plt.rcParams['ytick.major.size'] = 8
        plt.rcParams['ytick.major.width'] = 1.8
        plt.rcParams['ytick.minor.size'] = 7
        plt.rcParams['ytick.minor.width'] = 1.8
        plt.rcParams['pdf.fonttype'] = 42
        plt.rcParams['ps.fonttype'] = 42
        plt.rcParams["legend.fancybox"] = True

        #################

        # Plotting Spectrum
        plt.clf()
        plt.plot(self.wavelength, self.flux, color = 'b', lw = 2)
        plt.xlabel(r'Wavelength $(\AA)$')
        plt.ylabel(r'Flux (Some units)')
        plt.xlim([min(self.wavelength) - 1, max(self.wavelength) + 1])
        plt.ylim([min(self.flux) - 0.1 * (min(self.flux)), max(self.flux) - 0.1 * (max(self.flux))])
        plt.savefig(name_figure + '.png', dpi=200)

    def color(self, filter_name1, filter_name2):
        ### Compute color from the spectrum
        mag_object1 = Convolution(self.wavelength, self.flux, filter_name1)
        mag_object2 = Convolution(self.wavelength, self.flux, filter_name2)

        return mag_object1.magnitude - mag_object2.magnitude
