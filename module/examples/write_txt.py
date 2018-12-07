import glob

from spectrum import Spectrum

filepath = '/Users/Shannon/Desktop/SciCoder/SciCoder-2018-Sydney/Data Files/spectra/'

files = glob.glob(filepath+'*.fits', recursive=True)

new = 'ra dec colour file \n'

for file in files:

	s = Spectrum(file)
	new += f"{s.ra} {s.dec} {s.color('g', 'r')} {s.id} \n"

	with open('test_text.txt', 'w') as f:
		f.write('%s' % new) 