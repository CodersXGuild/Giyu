
import unidecode 
from PIL import *
from Water import *

def Pics(pics , user , id , uname):
    background = Image.open("Giyu.jpg")
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('defaults.ttf', size=40)
    welcome_font = ImageFont.truetype('defaults.ttf', size=60)
    draw.text((30, 300), f'NAME: {unidecode(user)}', fill=(255, 255, 255), font=font)
    draw.text((30, 370), f'ID: {id}', fill=(255, 255, 255), font=font)
    draw.text((30, 40), f"Welcome to {unidecode(chat)}", fill=(225, 225, 225), font=welcome_font)
    draw.text((30,430), f"USERNAME : {uname}", fill=(255,255,255),font=font)  
    background.save(
        f"downloads/welcome#{id}.png"
    )
    return f"downloads/welcome#{id}.png"
