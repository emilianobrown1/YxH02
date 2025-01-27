from PIL import Image, ImageDraw, ImageFont
import glob

def make_image(text, username):
    text = text.capitalize()
    x = 'Images/fwbg.png'
    f = glob.glob('Fonts/*')
    im = glob.glob('saved_images/*')
    if f'{text}.jpg' in im:
        return f'saved_images/{text}.jpg'
    i = Image.open(x)
    wi, he = i.size
    d = ImageDraw.Draw(i)
    font = ImageFont.truetype(f[0], 60)
    font1 = ImageFont.truetype(f[0], 30)
    # Use textbbox to get the bounding box of the text
    bbox = d.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    new_w = (wi - w) / 2
    new_h = (he - h) / 2
    emoji_blue = (85, 172, 238)  
    d.text((new_w, new_h + 150), text, fill=emoji_blue, font=font)
    d.text((5, 5), username, fill=emoji_blue, font=font1)
    i.save(f'saved_images/{text}.jpg')
    return f'saved_images/{text}.jpg'