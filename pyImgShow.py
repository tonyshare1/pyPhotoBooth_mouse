import pygame, time
from pygame.locals import *

#==Start of Img_fill===
#==fill_type =0: fill image with original w/h ratio with-in screen
#==fill_type =1: fill image with original w/h ratio, and let one of the w/h fit screen's w/h
#==fill_type =3: fill image directly to screen's w/h without maintaining its w/h ratio
def Img_fillin( img_file, screen_info, DISPLAYSURF, fill_type):
   img = pygame.image.load(img_file)
   img_rect = img.get_rect()

   img_w = img_rect[2]
   img_h = img_rect[3]
   img_ratio = img_rect[2]/float(img_rect[3])
   
   screen_w = screen_info.current_w
   screen_h = screen_info.current_h
   screen_ratio = screen_info.current_w/float(screen_info.current_h)

   if fill_type > 2:
      fill_type = 2 	#error handling
   if fill_type == 0:
      if img_ratio > screen_ratio:
         #img_w has to fit to scree_w
         scale_fact = screen_w/float(img_w)
         scale_h = int(round(img_h * scale_fact))
         #print(scale_h)
         img_scale = pygame.transform.scale(img, (screen_w,scale_h))
         DISPLAYSURF.blit( img_scale, (0, int(round((screen_h-scale_h)/2.0))) )
      else:
         #img_h has to fit to scree_h
         scale_fact = screen_h/float(img_h)
         scale_w = int(round(img_w * scale_fact))
         #print(scale_w)
         img_scale = pygame.transform.scale(img, (scale_w, screen_h))
         DISPLAYSURF.blit( img_scale, ( int(round((screen_w-scale_w)/2.0)), 0) )
         
   elif fill_type == 1:
      if img_ratio > screen_ratio:
         #img_h has to fit to scree_h
         scale_fact = screen_h/float(img_h)
         scale_w = int(round(img_w * scale_fact))
         #print(scale_w)
         img_scale = pygame.transform.scale(img, (scale_w,screen_h))
         DISPLAYSURF.blit( img_scale, ( int(round((screen_w-scale_w)/2.0)), 0) )

      else:
         #img_w has to fit to scree_w
         scale_fact = screen_w/float(img_w)
         scale_h = int(round(img_h * scale_fact))
         #print(scale_h)
         img_scale = pygame.transform.scale(img, (screen_w, scale_h))
         DISPLAYSURF.blit( img_scale, (0, int(round((screen_h-scale_h)/2.0))) )
         
   elif fill_type == 2:
      img_scale = pygame.transform.scale(img, (screen_w,screen_h))
      DISPLAYSURF.blit( img_scale, ( 0, 0) )
#==End of Img_fill===


#==Start of Img_w_bgcolor===
def Img_w_bgcolor( img_file, bg_color , screen_info, DISPLAYSURF):

   #==Fill Background Color
   DISPLAYSURF.fill(bg_color)

   #==Fill Foreground Image
   Img_fillin( img_file, screen_info, DISPLAYSURF, 0)

   #==Update Screen
   pygame.display.update()

#==Start of Img_w_bgcolor===

#==Start of Img_w_bgimg===
def Img_w_bgimg( img_file, bg_img , screen_info, DISPLAYSURF):

   #==Fill Background Color
   Img_fillin( bg_img, screen_info, DISPLAYSURF, 0)

   #==Fill Foreground Image
   Img_fillin( img_file, screen_info, DISPLAYSURF, 0)

   #==Update Screen
   pygame.display.update()

#==Start of Img_w_bgcolor===




def null_func():
   if len(countdown_list[i]) < 2:
      varfontObj= pygame.font.Font('freesansbold.ttf', int(screen_info.current_w / 2 ))
   else:
      varfontObj= pygame.font.Font('freesansbold.ttf', int(screen_info.current_w/ (len(countdown_list[i]))))

   textSurfaceObj = varfontObj.render(countdown_list[i], True, RED)
   textRectObj = textSurfaceObj.get_rect()
   textRectObj.center = ( screen_info.current_w/2, screen_info.current_h/2)

   #textSurfaceObj = varfontObj.render(countdown_list[i], True, RED)
   DISPLAYSURF.blit(textSurfaceObj, textRectObj)
   pygame.display.update()
   pygame.time.wait(1000)
   print(i)
   print( countdown_list[i])


##=======test code starts here============
if 0:
   pygame.init()
   screen_info = pygame.display.Info()
   DISPLAYSURF = pygame.display.set_mode( (screen_info.current_w,
                                        screen_info.current_h),
                                       FULLSCREEN)
   BLACK=(0,0,0)
   Img_w_bgcolor("test.jpg", BLACK, screen_info, DISPLAYSURF)
   pygame.time.wait(1000)

   Img_w_bgimg("test.jpg", "test2.jpg", screen_info, DISPLAYSURF)
   pygame.time.wait(1000)

   Img_w_bgimg("test2.jpg", "test.jpg" , screen_info, DISPLAYSURF)
   pygame.time.wait(1000)
