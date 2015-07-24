from PIL import Image, ImageOps


RESIZE_METHOD = Image.LANCZOS

# img_h_flip, input file, and output a horizonal mirrored image
# source_path[in]: input image file path
# output_path[out]: output image file path
# return N/A
def img_h_flip(source_path, output_path):
   im = img_h_flip_fipo(source_path)
   im.save(output_path)

# img_v_flip, input file, and output a vertically flipped image
# source_path[in]: input image file path
# output_path[out]: output image file path
# return N/A
def img_v_flip(source_path, output_path):
   im = img_v_flip_fipo(source_path)
   im.save(output_path, quality=90)

# img_h_flip_fipo, input file, and output a horizontal mirrored image
#                  fipo: [f]ile [i]put, [p]il [o]utput
# source_path[in]: input image file path
# return: PIL image object
def img_h_flip_fipo(source_path):  
   im = Image.open(source_path)
   im = ImageOps.mirror(im)
   return im

# img_v_flip_fipo, input file, and output a vertically flipped image
#                  fipo: [f]ile [i]put, [p]il [o]utput
# source_path[in]: input image file path
# return: PIL image object
def img_v_flip_fipo(source_path):  #fipo: [f]ile [i]put, [p]il [o]utput
   im = Image.open(source_path)
   im = ImageOps.flip(im)
   return im

# img_4to1, input file"s", and output a 4-in-1 file
# source_path[in]: input image file path LIST, contains 4 images in 1 list
# output_path[out]: output image file path
def img_4to1(source_path, output_path):
   img = img_4to1_fipo(source_path)
   img.save(output_path, quality=90)

# img_4to1_fipo, input file"s", and output a 4-in-1 PIL image object
#           fipo: [f]ile [i]put, [p]il [o]utput
# source_path[in]: input image file path LIST, contains 4 images in 1 list
# return: PIL image object
def img_4to1_fipo(source_path):
   if len(source_path) == 4:
      img_size = (0,0)
      img = Image.open(source_path[0])
      img_size = img.size
      half_img_size = (img_size[0]/2, img_size[1]/2)

      pos_x = (0 ,img_size[0]/2, 0,             img_size[0]/2)    #calculate each images position
      pos_y = (0 ,0,             img_size[1]/2, img_size[1]/2)

      bg_img = Image.new("RGB", img_size , "white")               #createv a new white base image

      for i in range(0,4):
         sub_img = Image.open( source_path[i] )
         sub_img = sub_img.resize(half_img_size, RESIZE_METHOD)
         #print source_path[i]
         bg_img.paste(sub_img, (pos_x[i], pos_y[i]) )
      return bg_img


# img_over_bg, input file, paste it on a background image with
#              specific size(target_size) and position(target_pos, upper,left)
# source_path[in]: input image file path
# target_size[in]: desired image size i.e. (800,600)
# target_pos[in]:  desired shift position for source image. i.e. (100,50) for upper left
# fill_type[in]:   Method to fit source image to target_size
#   fill_type =0: fill image with original w/h ratio with-in target_size
#   fill_type =1: fill image with original w/h ratio, and let one of the w/h fit screen's w/h
#   fill_type =2: fill image directly to screen's w/h without maintaining its w/h ratio
# bg_path[in]:      input Background image file path
# output_path[out]: output image file path

def img_over_bg(source_path, target_size, target_pos, fill_type,
                bg_path, output_path):
   bg_img = Image.open(bg_path)
   img = Image.open(source_path)

   o_img= img_over_bg_pipo(img, target_size, target_pos, fill_type,
             bg_img)

   o_img.save(output_path, quality=90)

# mask_over_img, input file, paste it on a background image with
#              specific size(target_size) and position(target_pos, upper,left)
# source_path[in]: input image file path
# target_size[in]: desired image size i.e. (800,600)
# target_pos[in]:  desired shift position for source image. i.e. (100,50) for upper left
# fill_type[in]:   Method to fit source image to target_size
#   fill_type =0: fill image with original w/h ratio with-in target_size
#   fill_type =1: fill image with original w/h ratio, and let one of the w/h fit screen's w/h
#   fill_type =2: fill image directly to screen's w/h without maintaining its w/h ratio
# bg_path[in]:      input ForeGround & Background image file path
#                   Have to be PNG so the foreground has transparent area for input image file to display
# output_path[out]: output image file path

def mask_over_img(source_path, target_size, target_pos, fill_type,
                bg_path, output_path):
   bg_img = Image.open(bg_path)
   img = Image.open(source_path)

   o_img= mask_over_img_pipo(img, target_size, target_pos, fill_type,
             bg_img)

   o_img.save(output_path, quality=90)


# mask_over_img_pipo, input file, paste it on a background image with
#              specific size(target_size) and position(target_pos, upper,left)
#               and covered with a PNG foreground
#               at last, return a PIL image object
#             fipo: [f]ile [i]put, [p]il [o]utput
# source_img[in]: input PIL image object
# target_size[in]: desired image size i.e. (800,600)
# target_pos[in]:  desired shift position for source image. i.e. (100,50) for upper left
# fill_type[in]:   Method to fit source image to target_size
#   fill_type =0: fill image with original w/h ratio with-in target_size
#   fill_type =1: fill image with original w/h ratio, and let one of the w/h fit screen's w/h
#   fill_type =2: fill image directly to screen's w/h without maintaining its w/h ratio
# mask image[in]: input ForeGround & Background PIL image object
#                   Have to be PNG so the foreground has transparent area for input image file to display
# return: PIL image object
def mask_over_img_pipo(source_img, target_size, target_pos, fill_type,
                mask_img):
   # mask(png) over picture(camera, jpeg input) on mask_img(png, same as mask)
   white_bg = Image.new("RGBA",mask_img.size,"white")
   bg = img_over_bg_pipo(source_img, target_size, target_pos, fill_type,
             mask_img)
   bg.paste(mask_img, (0,0) ,mask_img)
   white_bg.paste(bg, (0,0) , bg)
   return white_bg

# img_over_bg_pipo, input file, paste it on a background image with
#              specific size(target_size) and position(target_pos, upper,left)
#               and return a PIL image object
#             fipo: [f]ile [i]put, [p]il [o]utput
# source_img[in]: input PIL image object
# target_size[in]: desired image size i.e. (800,600)
# target_pos[in]:  desired shift position for source image. i.e. (100,50) for upper left
# fill_type[in]:   Method to fit source image to target_size
#   fill_type =0: fill image with original w/h ratio with-in target_size
#   fill_type =1: fill image with original w/h ratio, and let one of the w/h fit screen's w/h
#   fill_type =2: fill image directly to screen's w/h without maintaining its w/h ratio
# bg image[in]: input Background PIL image object
#                   Have to be PNG so the foreground has transparent area for input image file to display
# return: PIL image object
def img_over_bg_pipo(source_img, target_size, target_pos, fill_type,
                bg_img):
   bg_img = bg_img.copy()
   img = source_img.copy()

   #-resize img first
   tgt_w = target_size[0]
   tgt_h = target_size[1]
   tgt_ratio = tgt_w/tgt_h
   img_w = img.size[0]
   img_h = img.size[1]
   img_ratio = img_w/img_h
   if fill_type >2:
      fill_type = 2
   if fill_type ==0:
      if img_ratio > tgt_ratio:
         scale_fact = tgt_w/float(img_w)
         scale_h = int(round(img_h * scale_fact))
         img = img.resize( (tgt_w, scale_h) , RESIZE_METHOD )
      else:
         scale_fact = tgt_h/float(img_h)
         scale_w = int(round(img_w * scale_fact))
         img = img.resize( (scale_w, tgt_h) , RESIZE_METHOD)
   elif fill_type == 1:
      if img_ratio > tgt_ratio:
         scale_fact = tgt_h/float(img_h)
         scale_w = int(round(img_w * scale_fact))
         img = img.resize( (scale_w, tgt_h) , RESIZE_METHOD)
      else:
         scale_fact = tgt_w/float(img_w)
         scale_h = int(round(img_h * scale_fact))
         img = img.resize( ( tgt_w, scale_h) , RESIZE_METHOD)
   elif fill_type == 2:
      img = img.resize( (tgt_w, tgt_h) , RESIZE_METHOD)
   bg_img.paste(img, (target_pos[0], target_pos[1]) )
   return bg_img



# img_over_bg, direct file transfer test function
if 0:
   img_over_bg("pict/20150417214420.jpg", (800,600), (100,100),0,
               "Mask/1_0_hor.png", "result/over.jpg")



   mask_over_img("pict/20150417214420.jpg", (1200,900), (0,0),0,
                     "Mask/2_0_hor.png", "result/mask_over.jpg")

   source_path=("pict/20150417213538_0.jpg",
                "pict/20150417213538_1.jpg",
                "pict/20150417213538_2.jpg",
                "pict/20150417213538_3.jpg")
   output_path="inter/4in1.jpg"
   img_4to1(source_path, output_path)


   # img_h_flip test code
   # Have changed to using Pillow

   img_h_flip("Mask/1.png","result/flop.jpg")
   img_v_flip("Mask/1.png","result/flip.jpg")
    

