from png_overlay import *
from time import sleep

p = PngOverlay("count_down_img/print_or_restart.png")
num = PngOverlay("count_down_img/num1.png", 5)

p.show()
num.show()

sleep(3)

p.setImage("count_down_img/frame_select_text.png")
num.setImage("count_down_img/num2.png")

sleep(3)

num.setImage("count_down_img/num3.png")

sleep(2)
p.hide()
num.hide()
