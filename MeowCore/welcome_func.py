
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import requests


BASE_URL = f'https://api.telegram.org/bot'



async def get_user_pfp(user_id, TOKEN):
    response  = requests.get(f"{BASE_URL}{TOKEN}/getUserProfilePhotos?user_id={user_id}")
    file_id = response.json()["result"]["photos"][0][-1]["file_id"]
    
    response2 = requests.get(f"{BASE_URL}{TOKEN}/getFile?file_id={file_id}")
    file_path = response2.json()["result"]["file_path"]
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"


    if file_url.startswith("https://"):
        filename = os.path.basename(file_url)
    else:
        filename = file_url.split("/")[-1]
    file_path = os.path.join(os.getcwd(), filename)
    with requests.get(file_url, stream=True) as r:
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return filename


async def build_welcome(bg_path, build_data, user_pfp=None, chat_pfp=None):
    tempbg_open = Image.open(bg_path)

    if user_pfp:
        user_pfp_data = build_data["user_pfp_data"]
        
        # user pfp editing into circle shape
        user_pfp_img = Image.open(user_pfp)
        user_pfp_img = user_pfp_img.resize((640, 640))
        
        mask = Image.new("L", user_pfp_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + user_pfp_img.size, fill=255)
        user_pfp_img = ImageOps.fit(user_pfp_img, mask.size, centering=(user_pfp_data["size"]["horizontal"], user_pfp_data["size"]["vertical"])
        user_pfp_img.putalpha(mask)

    if chat_pfp:
        chat_pfp_data = build_data["chat_pfp_data"]
        
        # chat pfp editing into circle shape
        chat_pfp_img = Image.open(chat_pfp)
        chat_pfp_img = chat_pfp_img.resize((640, 640))

        mask = Image.new("L", chat_pfp_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + chat_pfp_img.size, fill=255)
        chat_pfp_img = ImageOps.fit(chat_pfp_img, mask.size, centering=(chat_pfp_data["size"]["horizontal"], chat_pfp_data["size"]["vertical"])
        chat_pfp_img.putalpha(mask)

    
