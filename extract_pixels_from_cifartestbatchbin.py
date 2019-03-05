#######################################################################
#
# Reading cifar10_testbatch.bin and extracting the image_pixels in 
# sequential manner.
#
#######################################################################

#######################################################################
#
# Tqdm is required for displaying the progress bar. 
# Do pip install tqdm
#
#######################################################################

import os
import sys
import time
import argparse
import numpy as np
from tqdm import tqdm

TEST_SET_IMAGE_COUNT = 10000
TOOLBAR_WIDTH = 40

def extract_image_pixels(input_filename, output_filename):
  fptr_read = open(input_filename,"rb")
  fptr_write = open(output_filename,"w")
 
  h,w,c = 32,32,3

  ## Image is of the format <1 byte Label> <3072 byte Image Data>
  for i in tqdm(range(0,TEST_SET_IMAGE_COUNT)):
    label = fptr_read.read(1)
    img_data = fptr_read.read(3072)
    label=ord(label)

    # Save image data label to a file  
    fptr_write.write(str(label)+",")
    
    # Creating Image data
    ## In cifar_testbatch.bin, Image is in rrrrrrrgggggbbbbb format.

    image = np.zeros((h,w,c),dtype=np.uint8)
    counter = 0 

    # Convert RRRRRGGGBBB to RGBRGBRGB.. type image	
    for row in range(0,h):
        for col in range(0,w):
           image[row,col,0] = img_data[counter]
           image[row,col,1] = img_data[counter+1024]
           image[row,col,2] = img_data[counter+2048]
           counter = counter+1
 
    for row in range(0,h):
        for col in range(0,w):
            for ch in range(0,c):
                if row == h-1 and col == w-1 and ch == c-1:
                    fptr_write.write(str(image[row,col,ch]))
                else:
                    fptr_write.write(str(image[row,col,ch])+",")

  fptr_read.close()
  fptr_write.close()

if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument("--i",help="input cifar_testbatch.bin file")
   parser.add_argument("--o",help="output pixel file")	   
   args = parser.parse_args()
   #print args.accumulate(args.i)
   extract_image_pixels(args.i,args.o)



