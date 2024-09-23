# a helper function for Telegram Category uses


from PIL import Image, ImageDraw, ImageOps, ImageFont


def circular_crop(image_path, size, circle_scale, location):
    """
    Helper function to crop an image into a circular shape and resize it.
    """
    img = Image.open(image_path).resize((640, 640))

    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)
    
    circular_img = ImageOps.fit(img, mask.size)
    circular_img.putalpha(mask)

    width, height = circular_img.size
    new_width = int(width * circle_scale)
    new_height = int(height * circle_scale)
    circular_img = circular_img.resize((new_width, new_height))

    return circular_img, (location["horizontal"], location["vertical"])


def add_text(draw, text, position, font, color):
    """
    Helper function to draw text on an image.
    """
    draw.text(position, text, fill=color, font=font)


def build_welcome(user_id, first_name, bg_path, build_data, user_pfp=None, chat_pfp=None):
    tempbg_open = Image.open(bg_path)
    
    # User Profile Picture
    if user_pfp:
        user_pfp_data = build_data["user_pfp_data"]
        user_pfp_img, user_pfp_pos = circular_crop(
            user_pfp, 
            user_pfp_data["size"], 
            user_pfp_data["circle"], 
            user_pfp_data["location"]
        )
        tempbg_open.paste(user_pfp_img, user_pfp_pos, user_pfp_img)

    # Chat Profile Picture
    if chat_pfp:
        chat_pfp_data = build_data["chat_pfp_data"]
        chat_pfp_img, chat_pfp_pos = circular_crop(
            chat_pfp, 
            chat_pfp_data["size"], 
            chat_pfp_data["circle"], 
            chat_pfp_data["location"]
        )
        tempbg_open.paste(chat_pfp_img, chat_pfp_pos, chat_pfp_img)

    # Add Text
    draw = ImageDraw.Draw(tempbg_open)
    all_text_data = build_data["text_data"]
    
    for text_data in all_text_data:
        font = ImageFont.truetype(text_data["font"]["font"], size=text_data["font"]["size"])
        text = text_data["text"]
        if text == "$user_id":
            text = str(user_id)
        elif text == "$first_name":
            text = first_name
        
        add_text(
            draw, 
            text, 
            (text_data["horizontal"], text_data["vertical"]), 
            font, 
            text_data["font"]["color"]
        )

    # Save the final image
    tempbg_open.save("complete.png")
