# -*- coding: utf-8 -*-
import pygame, sys, picamera, time, pyImgShow, pySlideShow, random, py_imgproc_pil, img_post_upload, pyFrameSelect
import shutil
from pygame.locals import *
from pyImgShow import *
from picamCountDown import *
from pySlideShow import *
from py_imgproc_pil import *
from img_post_upload import *
from pyFrameSelect import *
from gen_preview_mask import *
import easygui

#define used constants
WHITE = (255,255,255)
RED = (200,24,24)
BLACK = (0,0,0)

GEN_MASK = 1 		#if all other parameters are fixed and ran once, this can be set to 0 (bypass image cropping procedure)
ENABLE_4IN1 = 0

#path define
picam_dir = "pict/"
output_dir = "result/"
print_output_dir = "print_result/"
inter_dir = "inter/"
welcome_page_dir = "title/"
preview_output_dir = "Preview_Mask/"
count_down_img_list = ("count_down_img/num3.png","count_down_img/num2.png","count_down_img/num1.png")
hint_mask = "count_down_img/Hint_Shoot.png"

#Printer Name
printer_name = "Canon_CP900_GUTEN"

#configure for Path Selection
bg_select_cur =0
bg_selection_n = 2

bg_selection_list = ["Mask/demo_frame1.png" ,"Mask/demo_frame2.png" ]

#set by Manual
overlay_size_list = [ (640,480), (866,626)]
overlay_shift_list = [(164,186) , (105,125)]



#pygame init, start main program.
pygame.init()
screen_info = pygame.display.Info()

picam_res_list =[]
vertical_res = 1200
cal_image_capture_size_norm_y(overlay_size_list, picam_res_list , vertical_res)

picam_res_list_full_screen = []
cal_preview_screen( picam_res_list,picam_res_list_full_screen,screen_info.current_w, screen_info.current_h)

#img_file_type = "png"
img_file_type = "jpg"		#use JPG as PiCam output file extension, shorter IO time

output_img_file_type = "png"

nshot_x_by_y = (2,2)

banner_text_size = 100
frame_select_method = 1 #0=fixed to 0, 1=manual selection, will enter pyFrameSelect, 2: random

#Selphy Printer Paper Tray/Ink Catridge Problem
paper_ink_notification = 0  #0= disable, 1=enable
paper_round = 18  	#1 paper tray can fill in 18 sheet
paper_val = 18
ink_round =2		#1 ink catridge can print up to 2 paper tray (36sheet)
ink_val = 2

#welcome page & result

#define COuntdown words show for each 1 shot
countdown_list=[]
processing_list=[]
combining_list=[]
# require to solve unicode utf-8 font, to display Chinese characters
countdown_list.append("3")
countdown_list.append("2")
countdown_list.append("1")
countdown_list.append("SMILE")
processing_list.append("PROCESSING")
combining_list.append("Combining")

#define n-shot header
nshot_list=[]
nshot_list.append("1st SHOT")
nshot_list.append("2nd SHOT")
nshot_list.append("3rd SHOT")
nshot_list.append("4th SHOT")

PRINT_SEL_PRINT = 0		#no movement
PRINT_SEL_RECAP = 1		#left click
PRINT_SEL_DISCARD = 2	#Right click

#Foreground update index limit (300 = 3sec)
fg_timer=0
FG_LIMIT=1200

#set percentage of Title image probablity
TITLE_PERCENT = 45


cups_queue_enable(printer_name)

#gpio module init
#gpio_input_init(button_L)
#gpio_input_init(button_R)

cups_service_restart()


DISPLAYSURF = pygame.display.set_mode((screen_info.current_w, 
				     screen_info.current_h),
				     FULLSCREEN)

SCREEN_POS_LowRight = [screen_info.current_w, screen_info.current_h]

pygame.mouse.set_visible(True)
pygame.mouse.set_pos(SCREEN_POS_LowRight)

DISPLAYSURF = pygame.display.set_mode((screen_info.current_w, 
 					     screen_info.current_h))

#show title page, while processing sub-image
randomImgShow(welcome_page_dir , "png", BLACK, screen_info,	DISPLAYSURF)

# Generate Mask Image
single_shot_mask_list = []
n_shot_mask_list = []
gen_preview_1shot( bg_selection_list, overlay_size_list, overlay_shift_list, preview_output_dir,picam_res_list_full_screen, single_shot_mask_list, GEN_MASK)
gen_preview_nshot( bg_selection_list, overlay_size_list, overlay_shift_list, preview_output_dir, nshot_x_by_y ,picam_res_list_full_screen, n_shot_mask_list, GEN_MASK)


DISPLAYSURF.fill(BLACK)
pygame.display.update()
pygame.time.wait(10)

if (paper_ink_notification):
   paper_input = easygui.enterbox(msg="Set Paper Number, New =18", title="Reload Paper Set", default ="18")
   if paper_input:
      paper_val= int(paper_input)
	
      if paper_val ==0:
         easygui.msgbox(msg="No Paper, No Printing", title="Reload Paper Set")
         quit()
   else:
      quit()
      pygame.quit()
      sys.quit()
	
   ink_input = easygui.enterbox(msg="Set Ink Number, New =2", title="Reload Ink Set", default ="2")
   if ink_input:
      ink_val= int(ink_input)
	
      if ink_val ==0:
         easygui.msgbox(msg="No Ink, No Printing", title="Reload Ink Set")
         quit()
   else:
      quit()
      pygame.quit()
      sys.quit()


#Start Photobooth Loop
while True:

   # Don't Update screen every time in While loop
   # Otehrwise, you will suffer program HANGED in full screen

   if fg_timer >= FG_LIMIT:
      #This sector is to Show Welcome image & random slideshow
      DISPLAYSURF = pygame.display.set_mode((screen_info.current_w, 
                                             screen_info.current_h), FULLSCREEN)

      pygame.mouse.set_visible(True)
      pygame.mouse.set_pos(SCREEN_POS_LowRight)

      if random.randrange(0,100) < TITLE_PERCENT:
         randomImgShow(welcome_page_dir , "png", BLACK,screen_info,	DISPLAYSURF)
      else:
         #randomImgShow(print_output_dir, output_img_file_type, BLACK, screen_info,	DISPLAYSURF)
         randomImgShow_withMask(print_output_dir, output_img_file_type, hint_mask, screen_info,	DISPLAYSURF)

      cups_queue_enable(printer_name)

      pygame.time.wait(20)
      fg_timer = 0

      if (paper_ink_notification):
         if paper_val == 0:
            ink_val = ink_val -1
            if ink_val ==0:
               #print Change Ink & Paper
               text_screencenter( "Refill INK & PAPER", WHITE, screen_info,	DISPLAYSURF)

               pygame.display.update()
               easygui.msgbox(msg="Refill Ink & Paper, and press OK", title="Reload Paper & Ink", ok_button='OK')
               #Reset Paper_val & Ink_val
               paper_val=paper_round
               ink_val=ink_round
            else:            
               #print Change Paper
               text_screencenter( "Refill PAPER", WHITE, screen_info,	DISPLAYSURF)
               pygame.display.update()
               easygui.msgbox(msg="Refill Paper, and press OK", title="Reload Paper", ok_button='OK')
               #Reset Paper_val & Ink_val
               paper_val=paper_round
            fg_timer = FG_LIMIT #this line is used to update screen immediately

   else:
      fg_timer +=1

   pygame.time.wait(5)

   for event in pygame.event.get(QUIT):
      print "QUIT"
      cups_service_restart()
      quit()
      pygame.quit()
      sys.quit()
   for event in pygame.event.get(pygame.KEYDOWN):
      print "KEY DOWN"
      if event.key == pygame.K_ESCAPE:
         cups_service_restart()
         quit()
         pygame.quit()
         sys.quit()

   for event in pygame.event.get():
#if you use only event in pygame.event.get(), there will contains multiple events
#if it contains more than 1 mouse button down, it will trigger multiple shots
#better way is to get one from event & clear the queue
#before exit the photo procedure, clear the queue again

      print event

      photoframe_select = bg_select_cur

      if frame_select_method ==0:   #0=fixed to 0
         photoframe_select = bg_select_cur
      if frame_select_method ==1:   #1=manual selection, will enter pyFrameSelect
         photoframe_select = bg_select_cur
      if frame_select_method ==2:   #2: random
         photoframe_select = random.randrange(0, bg_selection_n)

      if (event.type == pygame.MOUSEBUTTONDOWN):		
         pygame.event.clear()

         if event.button == 1: #LMB
            pygame.event.clear()
             
            print_choice = PRINT_SEL_RECAP #Re-take picure

            if frame_select_method ==1:   #1=manual selection, will enter pyFrameSelect
               photoframe_select = photoFrameSelection(bg_selection_list, bg_select_cur, bg_selection_n, screen_info, DISPLAYSURF, banner_text_size)

            while(print_choice== PRINT_SEL_RECAP):
               time_stamp = time.strftime("%Y%m%d%H%M%S")
               pict_path = "".join( (picam_dir, time_stamp) )
               #print(pict_path)

               picam_booth_1shot_overlay(pict_path, picam_res_list[photoframe_select], 
                                          WHITE, single_shot_mask_list[photoframe_select],
                                          count_down_img_list, WHITE,img_file_type,
                                          screen_info,	DISPLAYSURF)
               pict_file_name = "".join( (time_stamp,".",img_file_type) )	 #png or jpg
               pict_output_name = "".join( (time_stamp,".",output_img_file_type) )	 #png or jpg
			
               pict_result_path = "".join( (picam_dir, pict_file_name) )
               pict_output_path = "".join( (output_dir, pict_output_name) )
               print_output_path = "".join( (print_output_dir, pict_output_name) )
               #print(pict_output_path)
	
               #h-flip the image
               #inter_file_name = "".join( (time_stamp,".jpg") )
               #inter_result_path = "".join( (inter_dir, inter_file_name) )
               #print inter_result_path
               #img_h_flip(pict_path, pict_result_path)
	
               text_screencenter( processing_list[0], RED, screen_info,	DISPLAYSURF)
               pygame.display.update()
	
               mask_over_img(pict_result_path, overlay_size_list[photoframe_select], 
                              overlay_shift_list[photoframe_select], 0,
                              bg_selection_list[photoframe_select], pict_output_path)

               Img_w_bgcolor( pict_output_path, WHITE ,screen_info,	DISPLAYSURF)
               pygame.time.wait(2000)
               
               print_choice = photoPrintSelect(pict_output_path, screen_info, DISPLAYSURF)
               pygame.event.clear()

               if(print_choice == PRINT_SEL_PRINT):
                  cups_cli_print(printer_name, pict_output_path)
                  shutil.copy2( pict_output_path, print_output_path)
                  paper_val = paper_val -1   #paper count --
                  Img_w_bgcolor( pict_output_path, WHITE ,screen_info,	DISPLAYSURF)
                  pygame.time.wait(2000)
                  #set to print
               pygame.time.wait(500)
               print("Single shot done")


         if (event.button == 3)&(ENABLE_4IN1): #RMB
         #if 0:   #Disable 4 in 1
            pygame.event.clear()
            print_choice = PRINT_SEL_RECAP #Re-take picure
            bg_select_cur = 1
            
            if frame_select_method ==1:   #1=manual selection, will enter pyFrameSelect
               photoframe_select = photoFrameSelection(bg_selection_list, bg_select_cur, bg_selection_n, screen_info, DISPLAYSURF, banner_text_size)

            while(print_choice==PRINT_SEL_RECAP):
               time_stamp = time.strftime("%Y%m%d%H%M%S")
               pict_path = "".join( (picam_dir, time_stamp) )
               #print(pict_path)

               picam_booth_nshot_overlay(pict_path, picam_res_list[photoframe_select],
                                          WHITE, n_shot_mask_list[photoframe_select],
                                          count_down_img_list, WHITE,
                                          nshot_list, RED, WHITE,img_file_type,
                                          screen_info,	DISPLAYSURF)
                                          
               #start image processing & show
               multi_source_path=[]
               for i in range(0,4):
                  pict_file_name = "".join( (time_stamp,"_", str(i),".", img_file_type) )	 #png or jpg

                  pict_result_path = "".join( (picam_dir, pict_file_name) )
                  multi_source_path.append(pict_result_path)
                  #print multi_source_path
	
               text_screencenter( combining_list[0], RED, screen_info,	DISPLAYSURF)
               pygame.display.update()


               inter_file_name = "".join( (time_stamp,".", output_img_file_type) )
               inter_result_path = "".join( (inter_dir, inter_file_name) )
               #print inter_result_path
	
               text_screencenter( combining_list[0], RED, screen_info,	DISPLAYSURF)
               pygame.display.update()
	
               img_4to1(multi_source_path, inter_result_path)
               Img_w_bgcolor( inter_result_path, BLACK ,screen_info,	DISPLAYSURF)
               pygame.time.wait(1000)
	
               text_screencenter( processing_list[0], RED, screen_info,	DISPLAYSURF)
               pygame.display.update()
	
               pict_file_name = "".join( (time_stamp,".", output_img_file_type) )
               pict_output_path = "".join( (output_dir, pict_file_name) )
               print_output_path = "".join( (print_output_dir, pict_output_name) )
               #print(pict_output_path)
	
               mask_over_img(inter_result_path, overlay_size_list[photoframe_select], 
                              overlay_shift_list[photoframe_select], 0,
                              bg_selection_list[photoframe_select], pict_output_path)
	
               Img_w_bgcolor( pict_output_path, WHITE ,screen_info,	DISPLAYSURF)
               pygame.time.wait(2000)

               print_choice = photoPrintSelect(pict_output_path, screen_info, DISPLAYSURF)
               pygame.event.clear()

               if(print_choice == PRINT_SEL_PRINT ):
                  cups_cli_print(printer_name, pict_output_path)
                  shutil.copy2( pict_output_path, print_output_path)
                  paper_val = paper_val -1   #paper count --
                  Img_w_bgcolor( pict_output_path, WHITE ,screen_info,	DISPLAYSURF)
                  pygame.time.wait(2000)
                  #set to print
               pygame.time.wait(500)
               print("MULTI shot done")



      pygame.event.clear()  
      break


