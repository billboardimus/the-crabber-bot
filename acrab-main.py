from io import BytesIO
from typing import Optional, Any
import discord
import io
from PIL import Image, ImageDraw, ImageFont, ImageSequence


TOKEN = ' '

PERM_INT = '75776'

client = discord.Client()
picture = "C:\\Users\\billy\\PycharmProjects\\auto-crabber\\crab-rave.jpg"
picture2 = "C:\\Users\\billy\\PycharmProjects\\auto-crabber\\the_rave.gif"
picture3 = "C:\\Users\\billy\\PycharmProjects\\auto-crabber\\chuul.jpg"

yung = "string length"
if len(yung) > 5:
    a = yung.split()
    p = len(a[0])


async def make_meme(msg, image, type, command, message):
    """Makes a meme with text (msg) overlaid on top of an image of file type when user enters command """
    im = Image.open(image)
    tex = ImageDraw.Draw(im)
    caps_msg = msg.replace(command, "").upper()
    char = len(caps_msg)
    shadow = (0, 0, 0)
    txt_clr = (255, 255, 255)
    l, w = im.size
    sz = int((l / 1.5 / char) + 20)
    fnt = ImageFont.truetype('DUBAI-LIGHT.TTF', sz)
    x, h = tex.textsize(caps_msg, font=fnt)
    adj_x, adj_h = (l - x) / 2, (w / 3.5) - (h / 20)

    #   the black border
    tex.text((adj_x - 1, adj_h - 1), caps_msg, font=fnt, fill=shadow)
    tex.text((adj_x + 1, adj_h - 1), caps_msg, font=fnt, fill=shadow)
    tex.text((adj_x - 1, adj_h + 1), caps_msg, font=fnt, fill=shadow)
    tex.text((adj_x + 1, adj_h + 1), caps_msg, font=fnt, fill=shadow)
    #   the white text
    tex.text((adj_x, adj_h), caps_msg, fill=txt_clr, font=fnt)
    temp: BytesIO = io.BytesIO()
    im.save(temp, type)
    temp.seek(0)
    await client.send_file(message.channel, temp, filename='your_meme.png')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #   THE CRAB SECTION
    if message.content.startswith('!crabs') or message.content.endswith('!crabs'):
        await make_meme(message.content, picture, 'png', '!crabs', message)
    #   THE CHUUL SECTION
    elif message.content.startswith('!chuul') or message.content.endswith('!chuul'):
        await make_meme(message.content, picture3, 'png', '!chuul', message)
    #   THE .GIF SECTION
    elif message.content.startswith('!gif') or message.content.endswith('!gif'):
        im: Optional[Any] = Image.open(picture2)
        frames = []
        crab_message = message.content.replace("!gif", "").upper()
        char = len(crab_message)
        l, w = im.size
        sz = int((l / 1.83 / char) + 20)
        fnt = ImageFont.truetype('DUBAI-LIGHT.TTF', sz)
        shadow = (0, 0, 0)
        txt_clr = (255, 255, 255)
        for frame in ImageSequence.Iterator(im):
            frame = frame.convert('RGBA')
            tex = ImageDraw.Draw(frame)
            x, h = tex.textsize(crab_message, font=fnt)
            adj_x, adj_h = (l - x) / 2, (w / 3.5) - (h / 20)
            tex.text((adj_x, adj_h), crab_message, font=fnt)
            #   the black border
            tex.text((adj_x - 1, adj_h - 1), crab_message, font=fnt, fill=shadow)
            tex.text((adj_x + 1, adj_h - 1), crab_message, font=fnt, fill=shadow)
            tex.text((adj_x - 1, adj_h + 1), crab_message, font=fnt, fill=shadow)
            tex.text((adj_x + 1, adj_h + 1), crab_message, font=fnt, fill=shadow)
            #   the white text
            tex.text((adj_x, adj_h), crab_message, fill=txt_clr, font=fnt)
            del tex
            temp = io.BytesIO()
            frame.save(temp, format="GIF", save_all=True, append_images=frames[1:])
            frames.append(frame)
        out = io.BytesIO()
        frames[0].save(out, save_all=True, append_images=frames[1:], format="GIF")
        out.seek(0)

        await client.send_file(message.channel, out, filename='your_crab.gif')
        #   await client.send_message(message.channel, str(im.size))    #   prints the size


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
