# pyPhotoBooth_mouse
Raspberry Pi Photo Booth: using python, Pillow, PiCamera, easyGui..etc


# Overview:
 This is a Raspberry Pi project to act as commercial photo booth.
Basic idea is to press-button and shoot. The remaining image processing
and printing are done by python codes automatically.
 

# HW Requirement
 Raspberry Pi 2 (Pi Model B/B+ are OK, but with slower sleep)
 PiCamera

# SW Requirement
 Pillow 
 	(http://pillow.readthedocs.org/)
 easy_gui 
	(used for Change Ink/Cartridge indication)
 mechanize 
	(used for POST submit if CUPS doesn’t support your Printer. 
	You’ll need another PC/NB can properly print and setup 
	Apache web server + PHP to receive file/save file/print.)

# Raspberry Pi Setup
 Memory Split for GPU
 GPU must have 256MB+ if you got a full HD screen.

#Behavior
 =>Might show on Youtube Tutorial?

#How-to-Run
 python pyPhotoBooth_mouse.py

 After title page or photo slide show started, you can press mouse
 1> Left click => Start 1 Photo Format
 2> Right Click=> Start 4in1 format (if ENABLE_4IN1=1)

 Then you enter the Frame-selection, the instruction should show
 “Left click for next frame, or wait 5 sec to proceed”

 Next stage will show the count down and take pictures. 4in1 format will do this 4 times.

 Image processing will be performed automatically.
 Once the result is shown on screen, the instructions will show
 “Wait 5 sec to print,
 Left Click to re-capture Photo, Right Click to Discard all selection”
 1> Do nothing=> Print directly, and return to slide show mode
 2> Left Click=> Restart the count down and photo taking
 3> Right Click=>Return to slide show. (no printing)

 Many instructions are implemented by PNG graphics,
 Text should be replace in your desired format/language/position/color.
 

#Configuration

######Under pyPhotoBooth_mouse.py##########

GEN_MASK = 1 		#if all other parameters are fixed and ran once, 
			this can be set to 0 (bypass image cropping procedure)
ENABLE_4IN1 = 0		#Enable 4in1 format, right click can enter 4in1 mode


picam_dir = "pict/“ 			#the PiCamera’s picture raw output
output_dir = "result/"			#the final processed picture output
print_output_dir = "print_result/"	#if user choose to print, final output will be 
					copied to here. Slide show will fetch pictures
					from here.
inter_dir = "inter/"			#processed 4-in-1 picture
welcome_page_dir = "title/"		#title images are placed here
preview_output_dir = "Preview_Mask/"	#Generated Preview Mask will be stored here, 
					They are auto generated if GEN_MASK=1
count_down_img_list = ("count_down_img/num3.png","count_down_img/num2.png","count_down_img/num1.png")
					#count-down image, number only
hint_mask = "count_down_img/Hint_Shoot.png"
					#Hint-instruction under SlideShow mode
					# “Left Click to Take Picture!”
					# (due to Right click is disabled)

#Printer Name
printer_name = "Canon_CP900_GUTEN"	#the Printer’s name in CUPS

#configure for Path Selection
bg_select_cur =0			
bg_selection_n = 2			#total Frame number, should be identical to 
					bg_selection_list’s length

bg_selection_list = ["Mask/demo_frame1.png" ,"Mask/demo_frame2.png" ]
					#your Frame, PNG 32bit with your desired
					transparent area

#set by Manual
overlay_size_list = [ (640,480), (866,626)]	#the transparent area’s x*y size 
						in a rectangular
overlay_shift_list = [(164,186) , (105,125)]
						#the upper-left x,y position of 
						the rectangular


######Under pyFrameSelect.py##########

   instruction_mask = PngOverlay("count_down_img/frame_select_text.png") 
 	# frame_select_text.png
	# tell user to
	# “Left click for next Frame”

   instruction_mask = PngOverlay("count_down_img/print_or_restart.png") 
 	# print_or_restart.png
	# tell user to
	# “Wait 5 seconds to Print”
	# “Left Click to Re-Photo, Right Click to Discard All Selection”  
