# -*- coding: utf-8 -*-
import pygame, sys, pyImgShow, picamCountDown, pySlideShow, random
from pygame.locals import *
from pyImgShow import *
from picamCountDown import *
from pySlideShow import *


#define used constants
WHITE = (255,255,255)
RED = (200,24,24)
BLACK = (0,0,0)

TOP_BANNER_TEXT =  "Wait 3 sec to Take Photo"
BUTTOM_BANNER_TEXT = "Left Click for Next"

#Foreground update index limit (300 = 3sec)
WAIT_STEP = 5
FG_LIMIT=10

STAGE_LIMIT = 5
STAGE_LIMIT_CNT = STAGE_LIMIT*1000/WAIT_STEP


def photoFrameSelection(bg_selection, bg_select_current,bg_select_num_max, screen_info, DISPLAYSURF, text_size):
   bg_select_prev = bg_select_current+1  #initial value must be different
   fg_timer=FG_LIMIT+1
   self_timer =0
   print bg_select_current

   screen_info = pygame.display.Info()
   DISPLAYSURF = pygame.display.set_mode( (screen_info.current_w,
                      screen_info.current_h),
                      FULLSCREEN)
   pygame.mouse.set_pos(	[screen_info.current_w, screen_info.current_h] )

   instruction_mask = PngOverlay("count_down_img/frame_select_text.png") 
   instruction_mask.show()

   while self_timer< STAGE_LIMIT_CNT:
      # Don't Update screen every time in While loop
      # Otehrwise, you will suffer program HANGED in full screen
      if bg_select_current >= bg_select_num_max:
         bg_select_current = 0
	
      if fg_timer >= FG_LIMIT:
         #Update Shown Frame if choice is changed
         if bg_select_prev != bg_select_current:
            Img_w_bgcolor( bg_selection[bg_select_current], WHITE ,screen_info,	DISPLAYSURF)
            pygame.display.update()
            pygame.time.wait(20)
            bg_select_prev = bg_select_current

         #Reset timer
         fg_timer = 0
      else:
         fg_timer +=1
	
      pygame.time.wait(WAIT_STEP)
	
      for event in pygame.event.get(QUIT):
         print "QUIT"
         instruction_mask.hide()
         quit()
         pygame.quit()
         sys.quit()
      for event in pygame.event.get(pygame.KEYDOWN):
         print "KEY DOWN"
         if event.key == pygame.K_ESCAPE:
            instruction_mask.hide()
            quit()
            pygame.quit()
            sys.quit()
	
      for event in pygame.event.get():
         #if you use only event in pygame.event.get(), there will contains multiple events
         #if it contains more than 1 mouse button down, it will trigger another shot after current shot is complete
         #better way is to get one from event & clear the queue
         #before exit the photo procedure, clear the queue again
         print event
         pygame.event.clear()  
         
         if (event.type == pygame.MOUSEBUTTONDOWN):
            pygame.event.clear()

            if event.button == 1: #LMB
               pygame.event.clear()
               bg_select_current = bg_select_current +1
               self_timer =0	#reset timer

            if event.button == 3: #RMB
               instruction_mask.hide()
               pygame.event.clear()
               return bg_select_current

         pygame.event.clear() 
 
      self_timer = self_timer+1  #timer ++

   instruction_mask.hide()
   return bg_select_current #if while loop expired, return current value



def photoPrintSelect(bg_selection, screen_info, DISPLAYSURF):
   fg_timer=FG_LIMIT+1
   self_timer =0
   print bg_selection
   print_choice = 0  # 0 as not selected(Print), 1 as Recapture, 2 as Discard all, and re-select Photo Frame

   screen_info = pygame.display.Info()
   DISPLAYSURF = pygame.display.set_mode( (screen_info.current_w,
                                          screen_info.current_h),
                                          FULLSCREEN)

   pygame.mouse.set_pos(	[screen_info.current_w, screen_info.current_h] )

   instruction_mask = PngOverlay("count_down_img/print_or_restart.png") 
   instruction_mask.show()

   #show Photo Result
   Img_w_bgcolor( bg_selection, WHITE ,screen_info,	DISPLAYSURF)
   pygame.display.update()
   pygame.time.wait(20)

   while (self_timer< STAGE_LIMIT_CNT)&(print_choice==0):
      pygame.time.wait(WAIT_STEP)
	
      for event in pygame.event.get(QUIT):
         print "QUIT"
         instruction_mask.hide()
         quit()
         pygame.quit()
         sys.quit()
      for event in pygame.event.get(pygame.KEYDOWN):
         print "KEY DOWN"
         if event.key == pygame.K_ESCAPE:
            instruction_mask.hide()
            quit()
            pygame.quit()
            sys.quit()

      for event in pygame.event.get():
         print event
         pygame.event.clear()  
         if (event.type == pygame.MOUSEBUTTONDOWN):
            pygame.event.clear()

            if event.button == 1: #LMB		#Left for Re-capture
               pygame.event.clear()
               print_choice = 1     #Print

            if event.button == 3: #RMB		#Right for Abort
               pygame.event.clear()
               print_choice = 2     #Re capture, don't reselect the frame

         pygame.event.clear() 
 
      self_timer = self_timer+1  #timer ++
      #print self_timer
      #print STAGE_LIMIT_CNT

   instruction_mask.hide()
   return print_choice #if while loop expired, return current value





if 0: #test function sector
   bg_select_cur =0

   bg_selection_n = 2
   bg_selection_list = ("Mask/1.png" , "Mask/2.png")

   banner_text_size = 100


   #pygame init, start main program.
   pygame.init()

   screen_info = pygame.display.Info()
   DISPLAYSURF = pygame.display.set_mode((screen_info.current_w, 
                    screen_info.current_h),
                    FULLSCREEN)

   pygame.mouse.set_visible(False)

   DISPLAYSURF.fill(BLACK)
   pygame.display.update()
   pygame.time.wait(10)

   #a = photoFrameSelection(bg_selection_list, bg_select_cur, bg_selection_n, screen_info, DISPLAYSURF, text_size)
   a = photoPrintSelect(bg_selection_list[1], screen_info, DISPLAYSURF)
   print a
