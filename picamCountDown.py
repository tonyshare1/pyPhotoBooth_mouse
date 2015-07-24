import pygame, sys, picamera, time, pyImgShow
from pygame.locals import *
from pyImgShow import *
from png_overlay import *

def text_screencenter( show_text, text_color,screen_info,	DISPLAYSURF):
   if len(show_text) < 2:
      varfontObj= pygame.font.Font('freesansbold.ttf', int(screen_info.current_w / 2 ))
   else:
      varfontObj= pygame.font.Font('freesansbold.ttf', int(screen_info.current_w/ (len(show_text))))

   textSurfaceObj = varfontObj.render(show_text, True, text_color)
   textRectObj = textSurfaceObj.get_rect()
   textRectObj.center = ( screen_info.current_w/2,
                          screen_info.current_h/2)
   DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def text_size_screencenter( show_text, text_color,screen_info,	DISPLAYSURF, font_size):
   varfontObj= pygame.font.Font('freesansbold.ttf', font_size)
   textSurfaceObj = varfontObj.render(show_text, True, text_color)
   textRectObj = textSurfaceObj.get_rect()
   textRectObj.center = ( screen_info.current_w/2,
                          screen_info.current_h/2)
   DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def text_size_screencenter_bottom( show_text, text_color,screen_info,	DISPLAYSURF, font_size):
   varfontObj= pygame.font.Font('freesansbold.ttf', font_size)
   textSurfaceObj = varfontObj.render(show_text, True, text_color)
   textRectObj = textSurfaceObj.get_rect()
   textRectObj.center = ( screen_info.current_w/2,
                          screen_info.current_h - textRectObj.height/2)
   DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def text_size_screencenter_top( show_text, text_color,screen_info,	DISPLAYSURF, font_size):
   varfontObj= pygame.font.Font('freesansbold.ttf', font_size)
   textSurfaceObj = varfontObj.render(show_text, True, text_color)
   textRectObj = textSurfaceObj.get_rect()
   textRectObj.center = ( screen_info.current_w/2,
                          0 + textRectObj.height/2)
   DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def picam_booth_1shot(file_name, resolution, transparency, capture_bgcolor,
			countdown_list, text_color, bg_color, img_file_type,
			screen_info,	DISPLAYSURF):
   screen_info = pygame.display.Info()
   DISPLAYSURF = pygame.display.set_mode( (screen_info.current_w,
                      screen_info.current_h),
                      FULLSCREEN)
   countdown_len = len(countdown_list)
   print(countdown_len)

   with picamera.PiCamera(sensor_mode=2) as camera:
      camera.resolution = resolution
      camera.hflip = True
      camera.vflip = False
      camera.brightness = 65
      camera.awb_mode = 'off'
      camera.awb_gains = (1.4, 1.8)
      camera.start_preview()
      camera.preview_alpha = transparency

      image_file = []
      image_file.append(file_name)
      image_file.append(".")
      image_file.append(img_file_type)
      image_file_name = ''.join(image_file)
      print(image_file_name)

      time.sleep(2)
      for i in xrange(0, countdown_len, +1):
         DISPLAYSURF.fill(bg_color)
         text_screencenter( countdown_list[i], text_color,screen_info,	DISPLAYSURF)
         pygame.display.update()
         pygame.time.wait(1000)

      DISPLAYSURF.fill(capture_bgcolor)
      pygame.display.update()
      camera.capture(image_file_name)

      Img_w_bgcolor( image_file_name, capture_bgcolor ,screen_info,	DISPLAYSURF)
      camera.stop_preview()
      pygame.time.wait(1000)


def picam_booth_1shot_overlay(file_name, resolution, capture_bgcolor,
                              mask_img, countdown_img_list, bg_color, img_file_type,
                              screen_info,	DISPLAYSURF):
   screen_info = pygame.display.Info()
   DISPLAYSURF = pygame.display.set_mode( (screen_info.current_w,
                      screen_info.current_h),
                      FULLSCREEN)
   countdown_len = len(countdown_img_list)
   print(countdown_len)

   with picamera.PiCamera(sensor_mode=2) as camera:
      camera.resolution = resolution
      camera.hflip = True
      camera.vflip = False
      camera.awb_mode = 'off'
      
      file = open("camara_param", "r")
      line = file.readline()
      file.close()
      params = line.split(" ")
      camera.brightness = int(params[2])
      camera.awb_gains = (float(params[0]), float(params[1]))

      camera.start_preview()

      image_file = []
      image_file.append(file_name)
      image_file.append(".")
      image_file.append(img_file_type)
      image_file_name = ''.join(image_file)
      print(image_file_name)
		
      time.sleep(2)
      preview_mask = PngOverlay(mask_img)   	#default =4, 1 layer higher than PiCamera Preview
      preview_mask.show()
      time.sleep(2)

      cd_num = PngOverlay(countdown_img_list[0], 5)	# layer 5, 1 layer higher than Preview mask
      time.sleep(1)
      for cd_img in countdown_img_list:
         DISPLAYSURF.fill(bg_color)
         cd_num.setImage(cd_img)
         cd_num.show()
         pygame.display.update()
         pygame.time.wait(1000)			

      cd_num.hide()
      camera.capture(image_file_name)

      preview_mask.hide()
      camera.stop_preview()

      Img_w_bgcolor( image_file_name, capture_bgcolor ,screen_info,	DISPLAYSURF)
      pygame.time.wait(500)


def picam_booth_nshot(file_name, resolution, transparency, capture_bgcolor,
                     countdown_list, text_color, bg_color,
                     nshot_list, nshot_txt_color, nshot_bg_color, img_file_type,
                     screen_info,	DISPLAYSURF):
   nshot_len = len(nshot_list)
   print("start nshot sub")
   for j in xrange(0, nshot_len, +1):
      DISPLAYSURF.fill(nshot_bg_color)
      text_screencenter( nshot_list[j], text_color,screen_info,	DISPLAYSURF)		
      pygame.display.update()
      pygame.time.wait(1000)
      nshot_filename = "".join((file_name,"_", str(j)))
      print(nshot_filename)
      picam_booth_1shot(nshot_filename, resolution, transparency, capture_bgcolor,
            countdown_list, text_color, bg_color,img_file_type,
            screen_info,	DISPLAYSURF)
   print("exit multi shot")

def picam_booth_nshot_overlay(file_name, resolution, capture_bgcolor,
                              mask_img_list, countdown_img_list, bg_color,
                              nshot_list, nshot_txt_color, nshot_bg_color,img_file_type,
                              screen_info,	DISPLAYSURF):

   nshot_len = len(nshot_list)
   print("start nshot sub")
   for j in xrange(0, nshot_len, +1):
      DISPLAYSURF.fill(nshot_bg_color)
      text_screencenter( nshot_list[j], nshot_txt_color,screen_info,	DISPLAYSURF)
      pygame.display.update()
      pygame.time.wait(1000)
      nshot_filename = "".join((file_name,"_", str(j)))
      print(nshot_filename)
      picam_booth_1shot_overlay(nshot_filename, resolution, capture_bgcolor,
                     mask_img_list[j], countdown_img_list, bg_color,img_file_type,
                     screen_info,	DISPLAYSURF)
   print("exit multi shot")




#Start Test Code
if 0:
   #Set Count-down Display String

   nshot_list=[]
   nshot_list.append("1st SHOT")
   nshot_list.append("2nd SHOT")
   nshot_list.append("3rd SHOT")
   nshot_list.append("4th SHOT")


   countdown_list=[]
   countdown_list.append("READY")
   countdown_list.append("3")
   countdown_list.append("2")
   countdown_list.append("1")
   countdown_list.append("SMILE")
   print countdown_list
   print countdown_list[1]

   WHITE = (255,255,255)
   RED = (200,24,24)
   BLACK = (0,0,0)
   img_file_type ="png"

   pygame.init()
   screen_info = pygame.display.Info()
   DISPLAYSURF = pygame.display.set_mode( (screen_info.current_w,
                  screen_info.current_h),
                  FULLSCREEN)

   count_down_img_list = ("count_down_img/num3.png","count_down_img/num2.png","count_down_img/num1.png")
   mask_list =("Mask/2_0_hor.png", "Mask/overlay.png", "Mask/overlay.png", "Mask/2_0_hor.png")
   picam_booth_1shot_overlay("test_pic",  (640,480), WHITE,
               "Mask/2_0_hor.png", count_down_img_list, BLACK,img_file_type,
               screen_info,	DISPLAYSURF)

   picam_booth_nshot_overlay("test4in1", (640,480), WHITE,
         mask_list, count_down_img_list, BLACK,
         nshot_list, RED, BLACK,img_file_type,
         screen_info,	DISPLAYSURF)

   exit()

   text_size_screencenter( "test for center", RED,screen_info,	DISPLAYSURF,150)
   pygame.display.update()
   pygame.time.wait(1000)

   text_size_screencenter( "Left Click for Next Frame", RED,screen_info,	DISPLAYSURF,150)
   pygame.display.update()
   pygame.time.wait(1000)
if 0:
   text_size_screencenter_bottom( "test for bottom", RED,screen_info,	DISPLAYSURF, 100)
   pygame.display.update()
   pygame.time.wait(1000)
   text_size_screencenter_top( "test for top", RED,screen_info,	DISPLAYSURF, 100)
   pygame.display.update()
   pygame.time.wait(1000)
if 0:
   picam_booth_1shot("Test_pic", (640,480), 220, WHITE,
            countdown_list, RED, BLACK,img_file_type,
            screen_info,	DISPLAYSURF)
   pygame.time.wait(1000)

   picam_booth_nshot("Test_pic", (640,480), 220, WHITE,
            countdown_list, RED, BLACK,
            nshot_list, RED, BLACK,img_file_type,
            screen_info,	DISPLAYSURF)
   pygame.time.wait(1000)
