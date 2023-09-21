"""
LICENSE: WTFPL

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
"""

from random import sample, choice, randrange
from math import floor
from glob import glob
from os.path import exists
from PIL import Image, ImageEnhance, ImageDraw
from flask import Flask, request, send_file
from typing import Coroutine
from io import BytesIO
from privatebinapi import send

def run_server():
    app = Flask(__name__)

    @app.get("/")
    def recipe():
        imgbin = BytesIO()
        img, links = create(request.args.get("type"), request.args.get("output"), False)
        img.save(imgbin, "PNG")
        imgbin.seek(0)
        return send_file(imgbin, "image/png")

    app.run(port=3333)

def _get_item(path:str) -> str: return ":".join(path.split("/")[-2:]).removesuffix(".png")
def get_path(itemid:str) -> str: 
    path = f"assets/thisrecipedoesnotexist/items/{itemid.replace(':', '/')}.png"
    if not exists(path): return None
    return path

def _generate_kjs_script(items: list[str], type: str) -> str:
    output = items.pop()
    tiernums = {
        "3x3": 1,
        "5x5": 2,
        "7x7": 3,
        "9x9": 4
    }
    sep = ",\n    "
    return f"""
/*
    ! NOTE: This will not work out-of-the-box

    To get it working:
    1. Put the code below in either onEvent("recipes", event => {{<code here>}}) or ServerEvents.recipes(event => {{<code here>}}) depending on your version (the first one is for 1.16/1.18, the second one id for 1.19/1.20)
    2. Replace the modids with the correct ones in MODIDS
    3. Remove all items that do not exist in your current instance 
*/

MODIDS = {{
    {sep.join([f'"{i}": "{i}"' for i in set([j.split(":")[0] for j in items])])}
}}
event.recipes.extendedcrafting.shapeless_table("{output}", [
    {sep.join([f"MODIDS['{i.split(':')[0]}']+':{i.split(':')[1]}'" for i in items])}
]).merge({{tier: {tiernums[type]}}})
"""

def create(type:str, outputitem:str, generatepastes:bool) -> (Image.Image, tuple[str]):
    PARAMS = {
        "3x3": ((122, 68), (318, 38), 60, 12, 3, "basic_table"),
        "5x5": ((58, 73), (270, 57), 60, 12, 5, "advanced_table"),
        "7x7": ((32, 72), (256, 63), 62, 10, 7, "elite_table"),
        "9x9": ((32, 72), (248, 63), 64, 8, 9, "ultimate_table")
    }

    if type==None or type not in PARAMS.keys(): type=choice(list(PARAMS.keys()))
    
    selectedparams = PARAMS[type]
    offset = selectedparams[0]
    outputoffset = selectedparams[1]
    itemsize = selectedparams[2]
    gap = selectedparams[3]
    benchsize = selectedparams[4]
    name = selectedparams[5]

    files = glob("assets/thisrecipedoesnotexist/items/**/*.png")
    if outputitem!=None:
        if ":" not in outputitem: outputitem = "minecraft:"+outputitem
        outputitem = get_path(outputitem)
        if outputitem!=None: files.remove(outputitem)
    inputs = []
    randitems = sample(files, k=(benchsize**2)+(1 if outputitem==None else 0))
    if outputitem!=None: randitems.append(outputitem)

    for i in randitems:
        img : Image.Image = Image.open(i)
        if img.height!=img.width: 
            randpart = randrange(1, floor(img.height/img.width))
            img = img.crop((0, img.width*randpart, img.width, img.width*(randpart+1)))
        inputs.append(img.resize((itemsize, itemsize), Image.NEAREST).convert("RGBA"))
    output = inputs.pop()

    cell = itemsize*benchsize
    grid : Image.Image = Image.open(f"assets/thisrecipedoesnotexist/gui/{name}.png")
    grid = grid.resize((grid.width*4, grid.height*4), Image.NEAREST)
    for i, img in enumerate(inputs): grid.paste(img, (offset[0]+(itemsize+gap)*(i%benchsize), offset[1]+(itemsize+gap)*(i//benchsize)), img if img.mode=="RGBA" else None)
    grid.paste(output, (cell+outputoffset[0], (offset[1]+cell+outputoffset[1])//2), output if output.mode=="RGBA" else None)

    bg : Image.Image = Image.open(choice(glob("assets/thisrecipedoesnotexist/bg/*.png")))
    bg = ImageEnhance.Brightness(bg).enhance(.3)
    grid.thumbnail((grid.width/1.5, grid.height), Image.Resampling.LANCZOS)

    pastepoint = (bg.width//2-grid.width//2, bg.height//2-grid.height//2)
    bg.paste(grid, pastepoint, grid)

    minoffset = -25
    maxoffset = 100
    bg = bg.crop((pastepoint[0]-randrange(minoffset, maxoffset), pastepoint[1]-randrange(minoffset, maxoffset), pastepoint[0]+grid.width+randrange(minoffset, maxoffset), pastepoint[1]+grid.height))

    draw = ImageDraw.Draw(bg)
    draw.rectangle(((bg.width-30, 0), (bg.width-15, 15)), "#f80cf966")
    draw.rectangle(((bg.width-15, 15), (bg.width, 30)), "#f80cf966")
    draw.rectangle(((bg.width-15, 0), (bg.width, 15)), "#00000066")
    draw.rectangle(((bg.width-30, 15), (bg.width-15, 30)), "#00000066")

    kjslink = None
    if generatepastes: kjslink = send("https://privatebin.net/", text=_generate_kjs_script([_get_item(i) for i in randitems], type))["full_url"]

    return bg, ((kjslink, "") if generatepastes else None)

if __name__=="__main__": run_server()