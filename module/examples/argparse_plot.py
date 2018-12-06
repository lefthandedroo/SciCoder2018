import argparse

from spectrum.spectrum import Spectrum

parser = argparse.ArgumentParser(description="Plot spectra of given file",
										usage="spectrum.py --filepath datafile.fits")

parser.add_argument("-f", "--filepath", help="the data file to be read")

args = parser.parse_args()

s = Spectrum(args.filepath)
s.plot("Name")

print(s.color('g', 'r'))
