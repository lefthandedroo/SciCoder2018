import matplotlib.pyplot as plt
import astropy.units as u
import astropy.coordinates as coord
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

skymap = plt.figure(figsize=(12,6))
ax = skymap.add_subplot(111, projection="mollweide")
sc = ax.scatter(coord.Angle(s.ra*u.degree).wrap_at(180*u.degree).radian, coord.Angle(s.dec*u.degree).radian)
ax.grid(True)
skymap.savefig("skymap.pdf")