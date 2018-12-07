from .errors import SDSSFileNotSpecifiedException
from astropy.io import fits
from .convolution.convolution import Convolution


class Spectrum(object):

    def __init__(self, filepath=None):
        if filepath is None:
            raise SDSSFileNotSpecifiedException("A spectrum file must "
                                                "be specified to create a spectrum.")
        self.filepath    = filepath
        self._ra         = None
        self._dec        = None
        self._flux       = None
        self._wavelength = None
        self._error      = None
        self._id         = None
        self._objecttype = None

    @property
    def hdu_list(self):
        """ Returns the HDU list of this file. """
        return self.data

    @property
    def id(self):
        if getattr(self,'_id',None) is None:
            # ivar = inverse variance of flux
            with fits.open(self.filepath) as hdu_list:
                try:
                    self._id = str(hdu_list[2].data['BOSS_SPECOBJ_ID'][0])
                except KeyError:
                    print('You need to update the code to account for the modified keyword.')
        return self._id

    @property
    def objecttype(self):
        if getattr(self,'_objecttype',None) is None:
            # ivar = inverse variance of flux
            with fits.open(self.filepath) as hdu_list:
                try:
                    self._objecttype = hdu_list[2].data['OBJTYPE']
                except KeyError:
                    print('You need to update the code to account for the modified keyword.')
        return self._objecttype

    @property
    def ra(self):
        """ Returns the RA of this spectrum in degrees. """
        if self._ra is None:
            with fits.open(self.filepath) as hdu_list:
                try:
                    self._ra = hdu_list[0].header["PLUG_RA"]
                except KeyError:
                    print('You need to update the code to account for the modified keyword.')
        return self._ra

    @property
    def dec(self):
        """ Returns the DEC of this spectrum in degrees. """
        if self._dec is None:
            with fits.open(self.filepath) as hdu_list:
                try:
                    self._dec = hdu_list[0].header["PLUG_DEC"]
                except KeyError:
                    print('You need to update the code to account for the modified keyword.')
        return self._dec

    @property
    def wavelength(self):
        """Wavelength binning, linear bins."""
        if getattr(self, '_wavelength', None) is None:
            with fits.open(self.filepath) as hdu_list:
                try:
                    self._wavelength = 10**hdu_list[1].data['loglam']
                except KeyError:
                    print('You need to update the code to account for the modified keyword.')
        return self._wavelength

    @property
    def flux(self):
        if getattr(self, '_flux', None) is None:
            with fits.open(self.filepath) as hdu_list:
                try:
                    self._flux = hdu_list[1].data['flux']
                except KeyError:
                    print('You need to update the code to account for the modified keyword.')
        return self._flux
    @property
    def error(self):
        if getattr(self,'_error',None) is None:
            # ivar = inverse variance of flux
            with fits.open(self.filepath) as hdu_list:
                try:
                    self._error = 1./hdu_list[1].data['ivar']
                except KeyError:
                    print('You need to update the code to account for the modified keyword.')
        return self._error


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
        plt.plot(self.wavelength, self.flux, color = 'b', lw = 1.5)
        plt.plot(self.wavelength, self.error, color = 'r', lw = 1)
        plt.xlabel(r'Wavelength $(\AA)$')
        plt.ylabel(r'Flux (Some units)')
        plt.xlim([min(self.wavelength) - 1, max(self.wavelength) + 1])
        #plt.ylim([min(self.flux) - 0.1 * (min(self.flux)), max(self.flux) - 0.1 * (max(self.flux))])
        plt.savefig(name_figure + '.png', dpi=200)


    def color(self, filter_name1, filter_name2):
        ### Compute color from the spectrum
        mag_object1 = Convolution(self.wavelength, self.flux, filter_name1)
        mag_object2 = Convolution(self.wavelength, self.flux, filter_name2)

        return mag_object1.magnitude - mag_object2.magnitude

    def line_ew(self, name_line):
        ##### Retrieve the equivalent width of a given line

        with fits.open(self.filepath) as hdu_list:
            try:
                index = hdu_list[3].data['LINENAME'] == name_line
                line_value = hdu_list[3].data['LINEEW'][index]
            except ValueError:
                return "Value line wrong"

        return line_value
