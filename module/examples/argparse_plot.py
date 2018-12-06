import argparse

from spectrum import Spectrum

parser = argparse.ArgumentParser(description="Plot spectra of given file",
										usage="spectrum.py --filepath datafile.fits")

parser.add_argument("-f", "--filepath", help="the data file to be read")

args = parser.parse_args()

s = Spectrum(args.filepath)
s.plot("Name")

print("Colour is: " + str(s.color('g', 'r')))
print("Declination is: " + str(s.dec))
print("Right Ascension is: " + str(s.ra))
print("Length (wavelength) is: " + str(len(s.wavelength)))
print("Length (flux) is: " + str(len(s.flux)))