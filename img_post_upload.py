#required to install mechanize (if you'd like to upload image to another Web server & print is handled by that web server)
# sudo eazy_install mechanize
from mechanize import Browser
import os

url = 'http://192.168.1.101/file_transfer/'
form_name = 'img_input'
test_img = "title.jpg"

def upload_img(path, form, img):
   br = Browser()
   br.open(path)
   br.select_form(name=form)
   br.form.add_file(open(img), 'image', img)
   br.submit()


def upload_print(img):
   form_name = 'img_input'
   upload_img(url, form_name, img)

def cups_cli_print(printer, img):
   cmd = ''
   cmd = cmd+'lp -d '
   cmd = cmd+ printer
   cmd = cmd+' '
   cmd = cmd + img
   os.system(cmd)

def cups_queue_enable(printer):
   cmd = ''
   cmd = cmd+'sudo cupsenable '
   cmd = cmd+ printer
   os.system(cmd)

def cups_service_restart():
   cmd = ''
   cmd = cmd+'sudo service cups restart'
   os.system(cmd)

if 0:
   upload_img(url, form_name, test_img)
   upload_print(test_img)
   cups_queue_enable("Canon_CP900_GUTEN")
   cups_cli_print("Canon_CP900_GUTEN", test_img)

