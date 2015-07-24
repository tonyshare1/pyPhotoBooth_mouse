from PIL import Image, ImageOps


def cal_preview_screen( preview_size_list,gen_preview_list,screen_x, screen_y):
   num_preview = len(preview_size_list)
   x_y_ratio = float(screen_x)/screen_y
   for i in xrange(0,num_preview):
      pict_xy =preview_size_list[i] 
      pict_x =pict_xy[0] 
      pict_y =pict_xy[1] 

      pict_ratio = float(pict_x)/pict_y
      if (pict_ratio>x_y_ratio):
         output_ratio = (screen_x, pict_y * screen_x/pict_x)
      if (pict_ratio<=x_y_ratio):
         output_ratio = (pict_x * screen_y/pict_y, screen_y)
         
      gen_preview_list.append(output_ratio)
   print gen_preview_list

def cal_image_capture_size_norm_y( preview_size_list,gen_preview_list, screen_y):
   num_preview = len(preview_size_list)
   
   for i in xrange(0,num_preview):
      pict_xy =preview_size_list[i] 
      pict_x =pict_xy[0] 
      pict_y =pict_xy[1] 

      output_ratio = (pict_x * screen_y/pict_y, screen_y)
      print pict_x
      print pict_y
      print output_ratio

      gen_preview_list.append(output_ratio)
   print gen_preview_list


def gen_preview_1shot( preview_list, preview_size_list, preview_shift_list, preview_mask_dir, preview_mask_size,
                        gen_preview_list, generate_img):
   num_preview = len(preview_list)
   for i in xrange(0,num_preview):
      shift = preview_shift_list[i]
      size  = preview_size_list[i]
      crop_box = (shift[0], shift[1], shift[0]+size[0], shift[1]+size[1])
      output_path = preview_mask_dir + str(i) + ".png"
      if (generate_img):
         im = Image.open(preview_list[i])		#load image
         im = im.crop(crop_box)
         im = im.resize(preview_mask_size[i])
         im.save(output_path)
      gen_preview_list.append(output_path)
      
   print gen_preview_list


#bug in 2nd round crop image generation, the crop size will be x/2, y/2
# or the x/y position is shifted
def gen_preview_nshot( preview_list, preview_size_list, preview_shift_list, preview_mask_dir, x_by_y, preview_mask_size,
                        gen_preview_list,generate_img):
   num_preview = len(preview_list)
   for i in xrange(0,num_preview):
      shift = preview_shift_list[i]
      size  = preview_size_list[i]
      output_path_list =[]
      output_path = preview_mask_dir + str(i) + "_"      		#Preview_Mask/1_

      unit_x = size[0]/x_by_y[0]
      unit_y = size[1]/x_by_y[1]

      if (generate_img):		
         im = Image.open(preview_list[i])		#load image

      for j_y in xrange(0, x_by_y[1]):
         for j_x in xrange(0, x_by_y[0]):
            num = j_x + j_y*x_by_y[0]
            output_path_sub = output_path + str(num) + ".png"		#Preview_Mask/1_ add i.png
            
            crop_box = (shift[0]+ j_x*unit_x, shift[1]+j_y*unit_y, shift[0]+(j_x+1)*unit_x, shift[1]+(j_y+1)*unit_y)
            #print crop_box
            if (generate_img):
               im_sub = im.copy()
               im_sub = im_sub.crop( crop_box )
               im_sub = im_sub.resize(preview_mask_size[i])
               im_sub.save(output_path_sub)
            output_path_list.append(output_path_sub)
	
      gen_preview_list.append(output_path_list)
   print gen_preview_list


if 0:		#Test function
   bg_selection_list = ["Mask/2_0_hor.png" , "Mask/overlay.png"]
   picam_res_list = [(1024,768), (1024, 768)] #image size
   overlay_size_list = ( (1200,900), (1200,900) )
   overlay_shift_list = ((160,160) , (600,0))
   preview_output_dir = "Preview_Mask/"
   GENERATE_IMG =1

   preview_list =[]
   preview_nshot_list =[]



   print preview_list

   a=[]
   b=[]
   
   gen_preview_1shot( bg_selection_list, overlay_size_list, overlay_shift_list, preview_output_dir, picam_res_list,a, GENERATE_IMG)
   
   gen_preview_nshot( bg_selection_list, overlay_size_list, overlay_shift_list, preview_output_dir, (2,2), picam_res_list,b, GENERATE_IMG)
   
   print a
   print b
