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

print("File is: " + str(args.filepath))
print('-'*len(args.filepath) + '-'*9)
print("Colour is: " + str(s.color('g', 'r')))
print("Declination is: " + str(s.dec))
print("Right Ascension is: " + str(s.ra))
print("Length (wavelength) is: " + str(len(s.wavelength)))
print("Length (flux) is: " + str(len(s.flux)))
print("ID of object is: " + str(s.id))


##############################
# Skymap. Kind of useless in this file now that we've implemented it elsewhere.
##############################

'''skymap = plt.figure(figsize=(12,6))
ax = skymap.add_subplot(111, projection="mollweide")
sc = ax.scatter(coord.Angle(s.ra*u.degree).wrap_at(180*u.degree).radian, coord.Angle(s.dec*u.degree).radian, 
				marker="*", s=200, c=s.color('g', 'r'), cmap=plt.get_cmap("rainbow"), vmin=0, vmax=1)
plt.colorbar(sc, fraction=0.025, pad=0.04)
plt.title("Title", fontsize=16, y=1.05)
txt = r'Caption'
skymap.text(.49,.05,txt, fontsize=8, horizontalalignment='center')
ax.grid(True)
ax.set_axisbelow(True)
skymap.savefig("skymap.pdf")''''


