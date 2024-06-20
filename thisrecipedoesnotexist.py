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

# IMPORTS
from random import sample, choice, randrange
from math import floor
from glob import glob
from os.path import exists
from PIL import Image, ImageEnhance, ImageDraw
from flask import Flask, request, send_file
from io import BytesIO
from privatebinapi import send

# Main run server function
def run_server():
    app = Flask(__name__) # Create a flask app

    @app.get("/")
    def recipe(): # Root path (nested functions wow)
        if "Discordbot" in request.user_agent.string: return "" # Disable discord embeds by blocking useragents with "DiscordBot" in them
        
        # Create the image
        imgbin = BytesIO() # Make a temp png
        img, _ = create(request.args.get("type"), request.args.get("output"), False) # Generate the image with provided args
        img.save(imgbin, "PNG") # Save it to the temp png io
        imgbin.seek(0) # Write to memory

        # Response logic
        response = send_file(imgbin, "image/png") # Initiate the response with "image/png" type
        # Disable cache
        response.headers["Cache-Control"] = "no-store, must-revalidate"
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response # Send the response

    app.run(port=3333) # Run flask app on 3333

# HELPER FUNCTIONS
def _get_item(path:str) -> str: return ":".join(path.split("/")[-2:]).removesuffix(".png") # Get the item name from the png filename
def get_path(itemid:str) -> str: # Get the path from the item id
    path = f"assets/thisrecipedoesnotexist/items/{itemid.replace(':', '/')}.png"
    if not exists(path): return None
    return path

# Generate a kjs script that adds the imaginary recipe
def _generate_kjs_script(items: list[str], type: str) -> str:
    output = items.pop() # Get the last item as output, leaving only inputs in the items argument
    tiernums = { # Map crafting table sizes to their tier numbers
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

# MAIN FUNCTION
def create(type:str, outputitem:str, generatepastes:bool) -> (Image.Image, tuple[str]):
    PARAMS = { # Set different parameters based on the crafting table size requested
        "3x3": ((122, 68), (318, 38), 60, 12, 3, "basic_table"),
        "5x5": ((58, 73), (270, 57), 60, 12, 5, "advanced_table"),
        "7x7": ((32, 72), (256, 63), 62, 10, 7, "elite_table"),
        "9x9": ((32, 72), (248, 63), 64, 8, 9, "ultimate_table")
    }

    if type==None or type not in PARAMS.keys(): type=choice(list(PARAMS.keys())) # Randomly select a crafting table if not provided
    
    # Convert random ass data from tuples into readable variables
    selectedparams = PARAMS[type]
    offset = selectedparams[0]
    outputoffset = selectedparams[1]
    itemsize = selectedparams[2]
    gap = selectedparams[3]
    benchsize = selectedparams[4]
    name = selectedparams[5]

    files = glob("assets/thisrecipedoesnotexist/items/**/*.png") # Get all texture files from assets/thisrecipedoesnotexist/items
    if outputitem!=None: # If the output item id was provided, convert it to the texture file path and make it so it can't be an input
        if ":" not in outputitem: outputitem = "minecraft:"+outputitem
        outputitem = get_path(outputitem)
        if outputitem!=None: files.remove(outputitem)
    randitems = sample(files, k=(benchsize**2)+(1 if outputitem==None else 0)) # Randomly pick input items and 1 output item
    if outputitem!=None: randitems.append(outputitem) # Add the output item to the randitems list if specified

    # Iterate over all of the randomly selected items
    inputs = []
    for i in randitems:
        img : Image.Image = Image.open(i) # Open the texture image
        if img.height!=img.width: # Make the image a square so it wouldn't stretch
            randpart = randrange(1, floor(img.height/img.width))
            img = img.crop((0, img.width*randpart, img.width, img.width*(randpart+1)))
        inputs.append(img.resize((itemsize, itemsize), Image.NEAREST).convert("RGBA")) # Add the image object to inputs list
    output = inputs.pop() # Pop the last input and make it an output

    cell = itemsize*benchsize # Find the place where the output should be pasted
    grid : Image.Image = Image.open(f"assets/thisrecipedoesnotexist/gui/{name}.png") # Open the crafting bench GUI image
    grid = grid.resize((grid.width*4, grid.height*4), Image.NEAREST) # Resize it to be a little big bigger with nearest neighbor
    for i, img in enumerate(inputs): # Place the inputs
        imgfull = Image.new("RGBA", (grid.width, grid.height), "#00000000")
        imgfull.paste(img, (offset[0]+(itemsize+gap)*(i%benchsize), offset[1]+(itemsize+gap)*(i//benchsize)), img if img.mode=="RGBA" else None)
        grid = Image.alpha_composite(grid, imgfull)
    # Place the output
    outputfull = Image.new("RGBA", (grid.width, grid.height), "#00000000")
    outputfull.paste(output, (cell+outputoffset[0], (offset[1]+cell+outputoffset[1])//2), output if output.mode=="RGBA" else None)
    grid = Image.alpha_composite(grid, outputfull)

    bg : Image.Image = Image.open(choice(glob("assets/thisrecipedoesnotexist/bg/*.png"))) # Open a random background image
    bg = ImageEnhance.Brightness(bg).enhance(.3) # Reduce the brightness to make it look realistic
    grid.thumbnail((grid.width/1.5, grid.height), Image.Resampling.LANCZOS) # Resize the GUI image

    pastepoint = (bg.width//2-grid.width//2, bg.height//2-grid.height//2) # Get the center of the background image
    bg.paste(grid, pastepoint, grid) # Paste the GUI atop of the background image

    # Randomly select an offset so the "screenshot" looks more realistic
    minoffset = -25
    maxoffset = 100
    bg = bg.crop((pastepoint[0]-randrange(minoffset, maxoffset), pastepoint[1]-randrange(minoffset, maxoffset), pastepoint[0]+grid.width+randrange(minoffset, maxoffset), pastepoint[1]+grid.height))

    # Add watermark
    watermark = Image.new("RGBA", (bg.width, bg.height), "#00000000")
    draw = ImageDraw.Draw(watermark)
    draw.rectangle(((bg.width-30, 0), (bg.width-15, 15)), "#f80cf966")
    draw.rectangle(((bg.width-15, 15), (bg.width, 30)), "#f80cf966")
    draw.rectangle(((bg.width-15, 0), (bg.width, 15)), "#00000066")
    draw.rectangle(((bg.width-30, 15), (bg.width-15, 30)), "#00000066")
    bg = Image.alpha_composite(bg, watermark)

    # Generate a kjs script and post it to privatebin if requested
    kjslink = None
    if generatepastes: kjslink = send("https://privatebin.net/", text=_generate_kjs_script([_get_item(i) for i in randitems], type))["full_url"]

    return bg, ((kjslink, "") if generatepastes else None) # Return the image and links (if requested)

if __name__=="__main__": run_server() # Run the flask server if the file is not imported

# ok that's it ty for your attention