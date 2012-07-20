# -*- coding: utf-8 -*-
from Tkinter import *
import math
import numpy as np 
import Image, ImageTk
import pyfits
import db
import master 
import img_scale
 
def convert(data):
     tempDATA = []
     for i in data:
         tempDATA.append([float(j) for j in i])
     return np.asarray(tempDATA)
     
def draw_point(color, x, y):
    r,g,b = color
    pic.put("#%02x%02x%02x" % (r,g,b),(x,y))
    return 
# Midpoint circle drawing algorithm
def mid(xc,yc,r,color):
        x=0
        y=r
        p=1-r
        while(x<y):
                if(p<0):
                        x=x+1
                        p=p+2*x+1
                else:
                        x=x+1
                        y=y-1
                        p=p+2*(x-y)+1
                draw_point(color,xc+x,yc+y)
                draw_point(color,xc-x,yc+y)
                draw_point(color,xc+x,yc-y)
                draw_point(color,xc-x,yc-y)
                draw_point(color,xc+y,yc+x)
                draw_point(color,xc-y,yc+x)
                draw_point(color,xc+y,yc-x)
                draw_point(color,xc-y,yc-x) 
 
# We are using bresenham's algorithm
def draw_line(x0, y0, x1, y1, color):
    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    if y0 < y1:
        ystep = 1
    else:
        ystep = -1
 
    deltax = x1 - x0
    deltay = abs(y1 - y0)
    error = -deltax / 2
    y = y0
    for x in range(x0, x1 + 1):
        if steep:
            draw_point(color, y, x)
        else:
            draw_point(color, x, y )
 
        error = error + deltay
        if error > 0:
            y = y + ystep
            error = error - deltax

def drawOuterLimit(circleLength, xcenter, ycenter, length):

	
	angle_step = 360/circleLength
	for i in range(0, circleLength):
	    theta = angle_step * i
	    xstart = int(margin * math.cos(theta)) + xcenter
	    ystart = int(margin * math.sin(theta)) + ycenter
	    xend = int(length * math.cos(theta)) + xcenter
	    yend = int(length * math.sin(theta)) + ycenter
	    draw_line(xstart, ystart, xend, yend, color=(0,0,0))
	#drawOuterLimit(angle_step, xcenter, ycenter, length)


def main(inputImage):
  #inputFileName = '../data/filled/fpC-004152-r6-0064.fits'


  #inputFile = pyfits.open(inputFileName)
  #inputImage = inputFile[0].data

  
  listFile = '../data/SDSS_photo_match.csv'
  fitsDir = '../data/SDSS/'
  dataDir = '../data'
  
  print inputImage.shape
  #center = master.Astrometry.getPixelCoords(listFile, 0, dataDir)
  #print 'aaaaa', center

  #img=Image.fromarray(inputImage)
  #print img.shape, 'img'
  #imgTk=ImageTk.PhotoImage(img)
  #l.configure(image=imgTk)
  #l.bind('<Motion>', callback)
  

  #rgbArray = np.empty((height, width), dtype='object')
  #print rgbArray.shape
  #for i in range(0, height):
  #	for j in range(0, width):
		  #print  '#%02x%02x%02x' % (inputImage[i, j], inputImage[i, j], inputImage[i, j])
		  #rgbArray[i, j] = '#%02x%02x%02x' % (inputImage[i, j], inputImage[i, j], inputImage[i, j])
		  
		  
		  
 
      
      
		  
  center = db.dbUtils.getFromDB('ra, dec', 'mothersample', 'mothersample', ' where califa_id = 1')[0]		
  print center
  cutout = inputImage #get_cutout(center, inputImage, 700)
  print cutout.shape, 'cutoutshape'

  
  root = Tk()
  def callback():
      exit()

  b = Button(root, text="Exit?", command=callback)
  b.pack()


  print np.max(cutout), 'max', np.mean(cutout), 'mean', np.min(cutout), 'min'	
  
  #inputImage = 255*(np.log(inputImage)/np.log(np.max(inputImage)))
  #cutout = cutout - 85
  #cutout = 255*(cutout/np.max(cutout))
  #cutout = cutout-np.min(cutout)
  #cutout = 255*(cutout)/(np.max(cutout))
  cutout = 255 * img_scale.log(cutout-85)
  height=cutout.shape[0]
  width=cutout.shape[1]
  print np.max(cutout), 'max', np.mean(cutout), 'mean', np.min(cutout), 'min'
  
  
  img = PhotoImage(height=height, width=width)
  for i in range(0, height):
	  for j in range(0, width):		
		  
	      #if(cutout[i, j] > 14):
	    img.put('#%02x%02x%02x' % (cutout[i, j], cutout[i, j], cutout[i, j]), (j, i))
		 # print cutout[i, j], i, j
  #		img.put('#%02x%02x%02x' % (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256)), (j, i))
  #	horizontal_line = "{" + " ".join(rgbArray[i]) + "}"
  #	img.put(horizontal_line, (i, 0))
		  #print '#%02x%02x%02x' % (inputImage[i, j], inputImage[i, j], inputImage[i, j])	
	  print i,'-th column drawn'
  print "jau"
  h = Scrollbar(root, orient=HORIZONTAL)
  v = Scrollbar(root, orient=VERTICAL)
  canvas = Canvas(root, height=height, width=width, bg='#000000')#, yscrollcommand=v.set, xscrollcommand=h.set, scrollregion=(0, 0, width-300, height-900))
  canvas.pack()

  '''
  h['command'] = canvas.xview
  v['command'] = canvas.yview

  #canvas.grid(row=0, column=0)

  h.grid(row=0, column=1, sticky=NS)
  v.grid(row=1, column=0, sticky=EW)
  '''
  canvas.create_image(0, 0, image = img, anchor=NW)
  #root.grid_columnconfigure(0, weight=1)
  #root.grid_rowconfigure(0, weight=1)
  #lb = Label(root,image=img)
  #lb.pack()
  
  root.mainloop()


	    
''' 	 
	for i in range(0,margin):
	    mid(xcenter, ycenter,i,(0,0,0))
	 
	for i in range(line_length,line_length+4):
	    mid(xcenter, ycenter,i,(0,0,0))

 # Initializing Tkinter window
root = Tk()
CANVAS_SIZE = 600
pic = PhotoImage(width=CANVAS_SIZE,height=CANVAS_SIZE)
lb = Label(root,image=pic)
lb.pack()
 
margin = CANVAS_SIZE / 40
xcenter = int(CANVAS_SIZE / 2)
ycenter = int(CANVAS_SIZE / 2)
line_length = ((CANVAS_SIZE / 12) - margin)

currentPixels = np.array((100, 1))
n_lines = len(currentPixels)
angle_step = (2 * math.pi) / n_lines



 
 
'''
if __name__ == "__main__":
  main(inputImage)