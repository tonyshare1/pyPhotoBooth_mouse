import picamera
from time import sleep

from Tkinter import *

camera = picamera.PiCamera()

camera.start_preview()

camera.awb_gains = (1.7, 2.1)
camera.resolution = (500, 1080)
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)

camera.awb_mode = 'off'

index = 0
MAX_INDEX = 3  #2
TEST_FILE = "test.jpg"


awb_r = 1.7
awb_b = 2.1
brightness = 50
awb_mode = 'off'

awb_mode_sel= 0
awb_mode_arr =('off', 'auto', 'sunlight', 'cloudy', 'shade', 'tungsten', 'fluorescent', 'incandescent','flash','horizon')
#total 10 AWB_MODE
AWB_MODE_NUM = 10

step = 0.1


def plus(s):
   global camera
   global awb_r
   global awb_b
   global index
   global brightness
   global awb_mode_sel
   global awb_mode
   if index is 0:
      awb_r += s
   elif index is 1:
      awb_b += s
   elif index is 2:
      brightness += int(10 * s)
   elif index is 3:
      awb_mode_sel += int( 1/step * s)		#1 increment
      if (awb_mode_sel<0):
         awb_mode_sel=0
      if (awb_mode_sel>=AWB_MODE_NUM):
         awb_mode_sel=AWB_MODE_NUM-1
      print awb_mode_arr[awb_mode_sel]
      awb_mode = awb_mode_arr[awb_mode_sel]
   updateCameraParams()

def updateCameraParams():
   global awb_r
   global awb_b
   global brightness
   global awb_mode
   print "setting awb_gain (" + str(awb_r) + ", " + str(awb_b) + ") brightness " + str(brightness) + " AWB Mode:"+awb_mode
   camera.awb_gains = (awb_r, awb_b)
   camera.brightness = brightness
   camera.awb_mode = awb_mode

def searchAWBmode( mode ):
   for idx in xrange(0,AWB_MODE_NUM):
      if mode == awb_mode_arr[idx]:
         return idx



def printCurrentControlParamName():
   global index
   if index is 0:
      print "tuning awb_r, current value is " + str(awb_r)
   elif index is 1:
      print "tuning awb_b, current value is " + str(awb_b)
   elif index is 2:
      print "tuning brightness, current value is " + str(brightness)
   elif index is 3:
      print "tuning AWB Mode, current value is " + str(awb_mode)
      
def index_prev():
   global index
   if index > 0:
      index = index - 1
   printCurrentControlParamName()

def index_next():
   global index
   if index < MAX_INDEX:
      index = index + 1
   printCurrentControlParamName()




class KeyDemo( Frame ):
   def __init__( self ):
      Frame.__init__( self )
      self.pack( expand = YES, fill = BOTH )
      self.master.title( "Pi Camera tuning" )
      self.master.geometry( "700x100" )

      self.message1 = StringVar()
      self.line1 = Label( self, textvariable = self.message1 )
      self.message1.set( "/ : previous parameter\n* : next parameter\n- : decrease value\n+ : increase value" )
      self.line1.pack()

      self.message2 = StringVar()
      self.line2 = Label( self, textvariable = self.message2 )
      self.message2.set( "" )
      self.line2.pack()

      self.master.bind( "<KeyPress>", self.keyPressed )

   def keyPressed( self, event ):
      global step
      if event.char is '/': # up
         index_prev()
      elif event.char is '*': # down
         index_next()
      elif event.char is '+': # add
         plus(step)
      elif event.char is '-': # minus
         plus(-step)
      elif event.char is '0': # minus
         camera.capture(TEST_FILE)
   
def main():
   global awb_r
   global awb_b
   global brightness
   global awb_mode_sel
   global awb_mode

   file = open("pygame_picam/camara_param", "r")
   line = file.readline()
   params = line.split(" ")
   awb_r = float(params[0])
   awb_b = float(params[1])
   brightness = int(params[2])
   awb_mode_sel = searchAWBmode( params[3] )
   awb_mode = params[3]

   print params
   updateCameraParams()
   KeyDemo().mainloop()
   file = open("camara_param", "w")
   file.write(str(awb_r) + " " + str(awb_b) + " " + str(brightness) +" "+awb_mode )
   file.close()
if __name__ == "__main__":
   main()

