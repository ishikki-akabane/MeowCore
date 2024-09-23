
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import requests


async def build_welcome(user_id, first_name, bg_path, build_data, user_pfp=None, chat_pfp=None):
    tempbg_open = Image.open(bg_path)

    if user_pfp:
        user_pfp_data = build_data["user_pfp_data"]
        
        # user pfp editing into circle shape
        user_pfp_img = Image.open(user_pfp)
        user_pfp_img = user_pfp_img.resize((640, 640))
        
        mask = Image.new("L", user_pfp_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + user_pfp_img.size, fill=255)
        user_pfp_image = ImageOps.fit(user_pfp_img, mask.size, centering=(user_pfp_data["size"]["horizontal"], user_pfp_data["size"]["vertical"])
        user_pfp_image.putalpha(mask)

        user_pfp_circle = user_pfp_data["circle"]
        width, height = user_pfp_image.size
        new_width = int(width * user_pfp_circle)
        new_height = int(height * user_pfp_circle)
        pfp_image = user_pfp_image.resize((new_width, new_height))
        pfp_image.save(f"{user_id}_user_pfp.png")

        # Pasting image on the template
        user_image = Image.open(f"{user_id}_user_pfp.png")
        mask = Image.new("L", user_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + user_image.size, fill=255)
        tempbg_open.paste(user_image, (user_pfp_data["location"]["horizontal"], user_pfp_data["location"]["vertical"]), mask)
    

    if chat_pfp:
        chat_pfp_data = build_data["chat_pfp_data"]
        
        # chat pfp editing into circle shape
        chat_pfp_img = Image.open(chat_pfp)
        chat_pfp_img = chat_pfp_img.resize((640, 640))

        mask = Image.new("L", chat_pfp_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + chat_pfp_img.size, fill=255)
        chat_pfp_image = ImageOps.fit(chat_pfp_img, mask.size, centering=(chat_pfp_data["size"]["horizontal"], chat_pfp_data["size"]["vertical"])
        chat_pfp_image.putalpha(mask)

        chat_pfp_circle = chat_pfp_data["circle"]
        width, height = chat_pfp_image.size
        new_width = int(width * chat_pfp_circle)
        new_height = int(height * chat_pfp_circle)
        pfp_image = chat_pfp_image.resize((new_width, new_height))
        pfp_image.save(f"{user_id}_chat_pfp.png")

        # Pasting image on the template
        chat_image = Image.open(f"{user_id}_user_pfp.png")
        mask = Image.new("L", chat_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + chat_image.size, fill=255)
        tempbg_open.paste(chat_image, (chat_pfp_data["location"]["horizontal"], chat_pfp_data["location"]["vertical"]), mask)


    all_text_data = build_data["text_data"]
    for text_data in all_text_data:
        text_font = ImageFont.truetype(
            text_data["font"]["font"],
            size=text_data["font"]["size"]
        )
        text_color = text_data["font"]["color"]

        text = text_data["text"]
        if text == "$user_id":
            text = f"{user_id}"
        elif text == "$first_name":
            text = f"{first_name}"
        else:
            pass
        
        draw = ImageDraw.Draw(tempbg_open)
        draw.text(
            (text_data["horizontal"], text_data["vertical"]),
            text,
            fill=text_color,
            font=text_font,
        )
        
    tempbg_open.save("complete1.png")
    
