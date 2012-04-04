# -*- coding: utf-8 -*-
import os
import csv
import string

def touch(fname, times = None):
	  os.utime(fname, times)


for i in range(0, 939):
  with open('../data/maskFilenames.csv', 'rb') as f:
    mycsv = csv.reader(f)
    mycsv = list(mycsv)
    fname = string.strip(mycsv[i][1])
    
    with file(fname, 'a'):
      try:
	f = open(fname)
	#touch(fname)
      except IOError as e:
	print 'File does not exist', fname     	
	
    print fname