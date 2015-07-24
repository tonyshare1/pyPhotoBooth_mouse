import subprocess, shlex
from time import sleep

class PngOverlay(object):
   def __init__(self, png_path, layer=4):
      self.png_path = png_path
      self.overlay_process = None
      self.layer = layer

   def show(self):
      self.__killProcess()

      args = shlex.split("./pngview -b 0 -l " + str(self.layer) + " " + self.png_path)
      self.overlay_process = subprocess.Popen(args)

   def hide(self):
      self.__killProcess()

   def setImage(self, png_path):
      self.png_path = png_path
    
      if self.__isShowing():
         self.show()

   def __killProcess(self):
      if self.__isShowing():
         self.overlay_process.terminate()
         self.overlay_process.wait()

   def __isShowing(self):
      return self.overlay_process is not None
   
