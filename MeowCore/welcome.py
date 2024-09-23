# A helper function for Telegram Category uses


from PIL import Image, ImageDraw, ImageOps, ImageFont
import os


class WelcomeFunc:
    async def check_welcome_template(self, template_id):
        if template_id in self.WELCOME_TEMPLATE:
            data = self.WELCOME_TEMPLATE[template_id]
            return data
        else:
            return None

    async def build_welcome(self, template_id, user, chat, data):
        """
        Builds a welcome image by overlaying user and chat profile pictures, and
        adding personalized text over a background image.
        """
        bg_path = f"{chat.id}bgimage.png"
        build_data = data["data"]
        user_pfp = build_data["user_pfp"]
        user_pfp = f"downloads/{user.id}userpfp.jpg"
        chat_pfp = build_data["chat_pfp"]
        chat_pfp = f"downloads/{user.id}chatpfp.jpg"
        
        tempbg_open = Image.open(bg_path)

        # User Profile Picture
        if user_pfp:
            user_pfp_data = build_data["user_pfp_data"]
            user_pfp_img, user_pfp_pos = await self.circular_crop(
                user_pfp, 
                user_pfp_data["size"], 
                user_pfp_data["circle"], 
                user_pfp_data["location"]
            )
            tempbg_open.paste(user_pfp_img, user_pfp_pos, user_pfp_img)

        # Chat Profile Picture
        if chat_pfp:
            chat_pfp_data = build_data["chat_pfp_data"]
            chat_pfp_img, chat_pfp_pos = await self.circular_crop(
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
        
            await self.add_text(
                draw, 
                text, 
                (text_data["horizontal"], text_data["vertical"]), 
                font, 
                text_data["font"]["color"]
            )

        # Save the final image
        tempbg_open.save(f"{user_id}complete.png")

        # clean up memory
        try:
            tempbg_open.close()
            if user_pfp:
                user_pfp_img.close()
            if chat_pfp:
                chat_pfp_img.close()
        except:
            pass
        return
            
    async def circular_crop(self, image_path, size, circle_scale, location):
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


    async def add_text(self, draw, text, position, font, color):
        """
        Helper function to draw text on an image.
        """
        draw.text(position, text, fill=color, font=font)


