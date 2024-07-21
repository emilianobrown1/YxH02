from PIL import Image, ImageDraw, ImageFont

def colourify(im, word: str, text: str, height):
    width = 55
    wi = im.size[0]
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("./Fonts/font.ttf", 120)
    for i in range(0, 5):
        if text[i] == word[i]:
            clr = "green"
        else:
            if text[i] in word:
                clr = "yellow"
            else:
                clr = "white"
        w, h = d.textsize(text[i].upper(), f)
        d.text((width, height), text[i].upper(), fill=clr, font=f)
        d.line((0, height + 5, wi, height + 5))
        d.line((0, height + h + 5, wi, height + h + 5))
        width += 90

async def make_secured_image(user_id: int, word: str, lis: list) -> str:
    f = ImageFont.truetype("./Fonts/font.ttf", 10)
    le = len(lis)
    if le == 1:
        x = Image.open("Images/wordle.jpg")
        un = "@YxHGameBot"  # Replace with your bot's username
        ImageDraw.Draw(x).text((5, 5), un, fill="white", font=f)
    else:
        x = Image.open(f"user_images/{user_id}.jpg")
    he = x.size[1]
    he_co_or = (le * he / 7) - he / 14
    colourify(x, word, lis[-1], he_co_or)
    x.save(f"user_images/{user_id}.jpg")
    return f"user_images/{user_id}.jpg"
