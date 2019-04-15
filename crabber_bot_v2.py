from io import BytesIO
from typing import Optional, Any
import discord
import io
import time
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import config

PERM_INT = '75776'

picture = "C:\\Users\\billy\\PycharmProjects\\crab-bot-v2\\crab-rave.jpg"
picture2 = "C:\\Users\\billy\\PycharmProjects\\crab-bot-v2\\the_rave.gif"
picture3 = "C:\\Users\\billy\\PycharmProjects\\crab-bot-v2\\chuul.jpg"

# e = discord.Embed(title='your_meme')

yung = "string length"
if len(yung) > 5:
    a = yung.split()
    p = len(a[0])


async def make_meme(msg, image, type, command, message):
    """Makes a meme with text (msg) overlaid on top of an image of file type when user enters command """
    start_time = time.time()
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
    print("--- %s seconds --- before internet" % (time.time() - start_time))
    await message.channel.send(file=discord.File(temp, 'your_meme.png'))
    print("--- %s seconds ---" % (time.time() - start_time))


class MyClient(discord.client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
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
            start_time = time.time()

            im: Optional[Any] = Image.open(picture2)
            frames = []
            crab_message = message.content.replace("!gif ", "").upper()
            char = len(crab_message)
            l, w = im.size
            sz = int((l / 1.83 / char) + 20)
            fnt = ImageFont.truetype('DUBAI-LIGHT.TTF', sz)
            shadow = (0, 0, 0)
            txt_clr = (255, 255, 255)
            arb_tex = ImageDraw.Draw(im)
            x, h = arb_tex.textsize(crab_message, font=fnt)
            adj_x, adj_h = (l - x) / 2, (w / 3.5) - (h / 20)
            for frame in ImageSequence.Iterator(im):
                frame = frame.convert('RGBA')
                tex = ImageDraw.Draw(frame)
                tex.text((adj_x, adj_h), crab_message, font=fnt)
                #   the black border
                tex.text((adj_x - 1, adj_h - 1), crab_message, font=fnt, fill=shadow)
                tex.text((adj_x + 1, adj_h - 1), crab_message, font=fnt, fill=shadow)
                tex.text((adj_x - 1, adj_h + 1), crab_message, font=fnt, fill=shadow)
                tex.text((adj_x + 1, adj_h + 1), crab_message, font=fnt, fill=shadow)
                #   the white text
                tex.text((adj_x, adj_h), crab_message, fill=txt_clr, font=fnt)
                del tex
                frames.append(frame)
            out = io.BytesIO()
            frames[0].save(out, save_all=True, append_images=frames[1:], format="GIF")
            out.seek(0)
            print("--- %s seconds --- before internet" % (time.time() - start_time))

            await message.channel.send(file=discord.File(out, 'your_meme.gif'))
            print("--- %s seconds ---" % (time.time() - start_time))

#   @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     #   THE CRAB SECTION
#     if message.content.startswith('!crabs') or message.content.endswith('!crabs'):
#         await make_meme(message.content, picture, 'png', '!crabs', message)
#     #   THE CHUUL SECTION
#     elif message.content.startswith('!chuul') or message.content.endswith('!chuul'):
#         await make_meme(message.content, picture3, 'png', '!chuul', message)
#     #   THE .GIF SECTION
#     elif message.content.startswith('!gif') or message.content.endswith('!gif'):
#         start_time = time.time()
#
#         im: Optional[Any] = Image.open(picture2)
#         frames = []
#         crab_message = message.content.replace("!gif ", "").upper()
#         char = len(crab_message)
#         l, w = im.size
#         sz = int((l / 1.83 / char) + 20)
#         fnt = ImageFont.truetype('DUBAI-LIGHT.TTF', sz)
#         shadow = (0, 0, 0)
#         txt_clr = (255, 255, 255)
#         arb_tex = ImageDraw.Draw(im)
#         x, h = arb_tex.textsize(crab_message, font=fnt)
#         adj_x, adj_h = (l - x) / 2, (w / 3.5) - (h / 20)
#         for frame in ImageSequence.Iterator(im):
#             frame = frame.convert('RGBA')
#             tex = ImageDraw.Draw(frame)
#             tex.text((adj_x, adj_h), crab_message, font=fnt)
#             #   the black border
#             tex.text((adj_x - 1, adj_h - 1), crab_message, font=fnt, fill=shadow)
#             tex.text((adj_x + 1, adj_h - 1), crab_message, font=fnt, fill=shadow)
#             tex.text((adj_x - 1, adj_h + 1), crab_message, font=fnt, fill=shadow)
#             tex.text((adj_x + 1, adj_h + 1), crab_message, font=fnt, fill=shadow)
#             #   the white text
#             tex.text((adj_x, adj_h), crab_message, fill=txt_clr, font=fnt)
#             del tex
#             frames.append(frame)
#         out = io.BytesIO()
#         frames[0].save(out, save_all=True, append_images=frames[1:], format="GIF")
#         out.seek(0)
#         print("--- %s seconds --- before internet" % (time.time() - start_time))
#
#         await message.channel.send(file=discord.File(out, 'your_meme.gif'))
#         print("--- %s seconds ---" % (time.time() - start_time))


# @client.event
# async def on_ready():
#     print('Logged in as')
#     print(client.user.name)
#     print(client.user.id)
#     print('------')

client = MyClient()

client.run(config.TOKEN)
