import io
import time
import config
import discord
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from moviepy.editor import *
from io import BytesIO

client = discord.Client()

#   POINTS TO THE FILE LOCATION OF ANY POSSIBLE PICTURE FOR CLEAN CODE TM
picture = "C:\\Users\\billy\\PycharmProjects\\crab-bot-v2\\crab-rave.jpg"
picture2 = "C:\\Users\\billy\\PycharmProjects\\crab-bot-v2\\the_rave.gif"
picture3 = "C:\\Users\\billy\\PycharmProjects\\crab-bot-v2\\chuul.jpg"
video = "C:\\Users\\billy\\PycharmProjects\\crab-bot-v2\\vod.mp4"

#   INTITIALIZES GIF FILES WITH THE BOT FOR OPTIMIZATION
gif = Image.open(picture2)

#   INITIALIZES VIDEO FILES WITH THE BOT FOR OPTIMIZATION
vid = VideoFileClip(video)
vid = vid.volumex(0.8)

#   COLORS FOR THE MAIN TEXT AND TEXT 'OUTLINE' ('SHADOW')
shadow = (0, 0, 0)
txt_clr = (255, 255, 255)


async def make_meme(msg, image, filetype, command, message):
    """Makes a meme with text (msg) overlaid on top of an image of file type when user enters command """
    start_time = time.time()
    im = Image.open(image)
    tex = ImageDraw.Draw(im)
    caps_msg = msg.replace(command, "").upper()
    char = len(caps_msg)
    if char == 0:
        await message.channel.send("Please add something after the command.")
        return
    sz = int((im.size[0] / 1.5 / char) + 20)
    fnt = ImageFont.truetype('DUBAI-LIGHT.TTF', sz)
    x, h = tex.textsize(caps_msg, font=fnt)
    adj_x, adj_h = (im.size[0] - x) / 2, (im.size[1] / 3.5) - (h / 20)
    #   THE OUTLINE
    tex.text((adj_x - 1, adj_h - 1), caps_msg, font=fnt, fill=shadow)
    tex.text((adj_x + 1, adj_h - 1), caps_msg, font=fnt, fill=shadow)
    tex.text((adj_x - 1, adj_h + 1), caps_msg, font=fnt, fill=shadow)
    tex.text((adj_x + 1, adj_h + 1), caps_msg, font=fnt, fill=shadow)
    #   THE MAIN TEXT [SHADOW MUST COME FIRST, BEHIND NORMAL TEXT]
    tex.text((adj_x, adj_h), caps_msg, fill=txt_clr, font=fnt)
    temp: BytesIO = io.BytesIO()
    im.save(temp, filetype)
    temp.seek(0)
    print("--- %s seconds --- before internet" % (time.time() - start_time))
    await message.channel.send(file=discord.File(temp, 'your_meme.png'))
    print("--- %s seconds ---" % (time.time() - start_time))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))
    if message.author == client.user:
        return
    #   THE CRAB SECTION
    if message.content.startswith('!crabs'):
        await make_meme(message.content, picture, 'png', '!crabs', message)
    #   THE CHUUL SECTION
    elif message.content.startswith('!chuul'):
        await make_meme(message.content, picture3, 'png', '!chuul', message)
    #   THE RAVE.GIF SECTION
    elif message.content.startswith('!gif'):
        start_time = time.time()
        frames = []
        crab_message = message.content.replace("!gif", "").upper()
        char = len(crab_message)
        if char == 0:
            await message.channel.send("Please add something after the command.")
            return
        l, w = gif.size
        sz = int((l / 1.83 / char) + 20)
        fnt = ImageFont.truetype('DUBAI-LIGHT.TTF', sz)

        #   Makes a new image of just the text, the exact size of the gif, to be overlayed later [per A. Taber]
        tex_img = Image.new("RGBA", gif.size, (255, 255, 255, 0))
        arb_tex = ImageDraw.Draw(tex_img)
        x, h = arb_tex.textsize(crab_message, font=fnt)
        adj_x, adj_h = (l - x) / 2, (w / 3.5) - (h / 20)
        arb_tex.text((adj_x, adj_h), crab_message, font=fnt)

        #   THE OUTLINE
        arb_tex.text((adj_x - 1, adj_h - 1), crab_message, font=fnt, fill=shadow)
        arb_tex.text((adj_x + 1, adj_h - 1), crab_message, font=fnt, fill=shadow)
        arb_tex.text((adj_x - 1, adj_h + 1), crab_message, font=fnt, fill=shadow)
        arb_tex.text((adj_x + 1, adj_h + 1), crab_message, font=fnt, fill=shadow)
        #   THE MAIN TEXT [SHADOW MUST COME FIRST, BEHIND NORMAL TEXT]
        arb_tex.text((adj_x, adj_h), crab_message, fill=txt_clr, font=fnt)

        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert('RGBA')
            frames.append(Image.alpha_composite(frame, tex_img))

        out = io.BytesIO()
        frames[0].save(out, save_all=True, append_images=frames[1:], format="GIF")
        out.seek(0)
        print("--- %s seconds --- before internet" % (time.time() - start_time))
        await message.channel.send(file=discord.File(out, 'your_meme.gif'))
        print("--- %s seconds ---" % (time.time() - start_time))
    #   THE RAVE.MOV SECTION
    elif message.content.startswith('!vid'):
        start_time = time.time()
        crab_message = message.content.replace("!gif", "").upper()
        char = len(crab_message)
        if char == 0:
            await message.channel.send("Please add something after the command.")
            return
        l, w = gif.size
        sz = int((l / 1.83 / char) + 20)
        tex_img = TextClip(crab_message, fontsize=sz, color='white', font='DUBAI-LIGHT.TTF')
        tex_img = tex_img.set_pos('center').set_duration(10)
        video1 = CompositeVideoClip([vid, tex_img])
        print("--- %s seconds --- before internet" % (time.time() - start_time))
        video1.write_videofile("video.mp4", codec='libx264', audio=True)
        await message.channel.send(file=discord.File(video1, 'your_meme.mp4'))
        print("--- %s seconds ---" % (time.time() - start_time))
client.run(config.TOKEN)
