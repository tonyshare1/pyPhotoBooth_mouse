from wand.image import Image
from wand.display import display


def img_h_flip(source_path, output_path):
   with Image(filename=source_path) as img:
      print(img.size)
      img.flop()
      #display(img)
      img.save(filename=output_path)

def img_v_flip(source_path, output_path):
   with Image(filename=source_path) as img:
      print(img.size)
      img.flip()
      #display(img)
      img.save(filename=output_path)

def img_4to1(source_path, output_path):
   if len(source_path) == 4:
      img_size = (0,0)
      with Image(filename=source_path[0]) as img:
         img_size = img.size
         #print img_size
      pos_x = (0 ,img_size[0]/2, 0,             img_size[0]/2)
      pos_y = (0 ,0,             img_size[1]/2, img_size[1]/2)

      with Image(width=img_size[0], height=img_size[1]) as bg_img:
         for i in range(0,4):
            with Image(filename = source_path[i]) as img:
               img.resize(img_size[0]/2,img_size[1]/2)
               #print img.size
               bg_img.composite(img, pos_x[i], pos_y[i])
         bg_img.save(filename=output_path)
         #display(bg_img)

#==fill_type =0: fill image with original w/h ratio with-in screen
#==fill_type =1: fill image with original w/h ratio, and let one of the w/h fit screen's w/h
#==fill_type =2: fill image directly to screen's w/h without maintaining its w/h ratio
def img_over_bg(source_path, target_size, target_pos, fill_type,
               bg_path, output_path):
   print(bg_path)
   print(source_path)
   with Image(filename=bg_path) as bg_img:
      with Image(filename=source_path) as img:
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
               #img_w will fit tgt_w
               scale_fact = tgt_w/float(img_w)
               scale_h = int(round(img_h * scale_fact))
               print(scale_h)
               img.resize( tgt_w, scale_h)
            else:
               #img_h will fit tgt_h
               scale_fact = tgt_h/float(img_h)
               scale_w = int(round(img_w * scale_fact))
               print(scale_w)
               img.resize( scale_w, tgt_h)
         elif fill_type == 1:
            if img_ratio > tgt_ratio:
               #img_h will fit tgt_h
               scale_fact = tgt_h/float(img_h)
               scale_w = int(round(img_w * scale_fact))
               print(scale_w)
               img.resize( scale_w, tgt_h)
            else:
               #img_w will fit tgt_w
               scale_fact = tgt_w/float(img_w)
               scale_h = int(round(img_h * scale_fact))
               print(scale_h)
               img.resize( tgt_w, scale_h)
         elif fill_type == 2:
            img.resize(tgt_w, tgt_h)
         print(img.size)
         overlay_x = target_pos[0] + (tgt_w - img.size[0])/2
         overlay_y = target_pos[1] + (tgt_h - img.size[1])/2
         bg_img.composite(img, overlay_x, overlay_y)
      bg_img.save(filename=output_path)
      #display(bg_img)

if 0:
   img_over_bg("pict/20140901000057.jpg", (800,600), (100,100),0,
            "Mask/1_0_hor.png", "result/over.jpg")

   source_path=("pict/20140905002012_0.jpg",
             "pict/20140905002012_1.jpg",
             "pict/20140905002012_2.jpg",
             "pict/20140905002012_3.jpg")
   output_path="inter/20140905002012.jpg"
   img_4to1(source_path, output_path)


   #img_h_flip test code
   img_h_flip("Mask/1_0_hor.png","result/flop.jpg")
   img_v_flip("Mask/1_0_hor.png","result/flip.jpg")
    

   with Image(filename='foo.jpg') as img:
      print(img.size)
      img.format='jpeg'
      display(img)
   with Image(filename='overlay.png') as overlay:
      overlay.flop()
      display(overlay)
      img.composite(overlay,0,0)
      display(img)
      img.save(filename='output.jpg')


   #require a horizonal flop funtion
   #require a simple overlay (1 on 1)
   #require a function to merge 4 pic into 1

    
