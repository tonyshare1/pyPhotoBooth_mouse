# -*- coding: utf-8 -*-
import pygame, pyImgShow, glob, random
from pygame.locals import *
from pyImgShow import *
from picamCountDown import *


def randomImgShow(path, img_ext, bg_color, screen_info,	DISPLAYSURF):

   if path[len(path)-1] != '/':
      path = "".join( (path,"/") )
   print path
   search_path = "".join( (path, "*.", img_ext) )
   print search_path
	
   file_list = glob.glob(search_path)
   print(file_list)
   print( len(file_list))

   if len(file_list) > 0:

      #use one of them as Title Page
      img_idx = random.randrange(0, len(file_list))
      print img_idx

      Img_w_bgcolor(file_list[img_idx], bg_color, screen_info, DISPLAYSURF)

def randomImgShow_withMask(path, img_ext, mask, screen_info,	DISPLAYSURF):

   if path[len(path)-1] != '/':
      path = "".join( (path,"/") )
   print path
   search_path = "".join( (path, "*.", img_ext) )
   print search_path
	
   file_list = glob.glob(search_path)
   print(file_list)
   print( len(file_list))

   if len(file_list) > 0:

      #use one of them as Title Page
      img_idx = random.randrange(0, len(file_list))
      print img_idx

      Img_w_bgimg(mask, file_list[img_idx], screen_info, DISPLAYSURF)


if 0:
   pygame.init()
   screen_info = pygame.display.Info()
   DISPLAYSURF = pygame.display.set_mode( (screen_info.current_w,
                         screen_info.current_h),
                        FULLSCREEN)
   BLACK=(0,0,0)

   randomImgShow("title/", "jpg", BLACK, screen_info,	DISPLAYSURF)

   randomImgShow_withMask("title/","jpg", "Mask/se31.png", screen_info,	DISPLAYSURF)
   pygame.time.wait(2000)

    
