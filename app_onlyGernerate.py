from instabot import Bot
import os 
import glob
import requests
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from random import randrange
import textwrap
from string import ascii_letters
from dotenv import load_dotenv

load_dotenv()
INSTAGRAM_PASSWORD=os.environ.get('INSTAGRAM_PASSWORD')
FACTS_API_KEY=os.environ.get('FACTS_API_KEY')
IMAGE_API_KEY=os.environ.get('IMAGE_API_KEY')


# getting the fact -------------------------------

api_url = 'https://api.api-ninjas.com/v1/facts'
res = requests.get(api_url, headers={'X-Api-Key':FACTS_API_KEY}).json()
fact = res[0]["fact"]

# getting the base image --------------------------

r = requests.get("https://api.unsplash.com/photos/random/?client_id="+ IMAGE_API_KEY +"&query=abstract")

res = r.json()
image_link = res["links"]["download"]

# testing image
#random = randrange(4000)+1
#image_link = "https://picsum.photos/" + str(random)
# -------------

res_image = requests.get(image_link)
image = open('image.jpg', 'wb') 
image.write(res_image.content)
image.close()


# cropping and adding text -----------------------

im = Image.open("image.jpg")
w, h = im.size

diff = abs(w-h)
x = 0
y = 0
if (w>h):
    y = diff // 2
if (w<h):
    x = diff // 2

w = min(w,h)
h = w


im = im.crop((y, x, w+y, h+x))


# resize 
size = 1080, 1080
im_resized = im.resize(size, Image.Resampling.LANCZOS)

enhancer = ImageEnhance.Brightness(im_resized)
im_enhanced = enhancer.enhance(0.5)

im = im_enhanced



# adding text

img = im
font = ImageFont.truetype(font='font/Roboto-Regular.ttf', size=86)
draw = ImageDraw.Draw(im=img)
text = fact
avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
max_char_count = int(img.size[0] * .95 / avg_char_width)

text = textwrap.fill(text=text, width=max_char_count)
draw.text(xy=(img.size[0]/2, img.size[1] / 2), text=text, font=font, fill='#ffffff', anchor='mm')

img.save('image.jpg', "JPEG")

# posting the image ------------------------------
