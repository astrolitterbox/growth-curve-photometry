# -*- coding: utf-8 -*-
import pyfits
import csv


#import numpy as np
imgFile = pyfits.open('tsField-005115-2-40-0103.fit')
img = imgFile[1].data
head = imgFile[1].header
print head
print img.field(27)

exit()
with open('tsField.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(img)
    #writer.writerows(head)