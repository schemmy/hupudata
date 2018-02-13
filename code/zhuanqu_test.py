from os import listdir
from os.path import isfile, join
import pandas as pd


path = '../data/nba/'
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]



for file in onlyfiles:
	fn = path + file

	o = pd.read_csv(fn, sep=',',
					names=['poster', 'ids', 'name', 'url'])

	print (file, len(o), len(set(o['name'])))