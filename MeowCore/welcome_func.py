
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
