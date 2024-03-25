# IMPORTS

# Disable the fuzz warning
from warnings import filterwarnings 
filterwarnings("ignore")

# Discord.py and related
import discord
from discord import app_commands, interactions
from discord.ext import tasks

# System stuff
from asyncio import sleep, run_coroutine_threadsafe
from sys import argv
from os import _exit, path, getenv
from subprocess import Popen, DEVNULL
from io import BytesIO
from threading import Thread
from traceback import format_exc

# Other built-in modules
from re import search, IGNORECASE
from random import choice
from json import loads, load, dump, dumps
from hashlib import md5
from sqlite3 import connect

# Dates and times
from datetime import datetime
from pytz import all_timezones
from pytz import timezone as tz

# Web-related stuff
from flask import Flask, request
from requests import get
from httpx import AsyncClient
from urllib import error, parse

# Other pip modules
from thefuzz import process
from pubchempy import get_compounds, get_substances, Compound, Substance, BadRequestError

# TRDNE
from thisrecipedoesnotexist import create, get_path, run_server

# GLOBAL VARIABLES AND CONSTS
client = discord.Client(intents=discord.Intents.all()) # Discord client
tree = app_commands.CommandTree(client) # Discord bot command tree
db = connect("missing.db") # Sqlite db
dbcursor = db.cursor() # Sqlite cursor
http = AsyncClient() # Async http client
server = Flask(__name__) # Flask server

# DB tables
TABLES = {
    "users": {
        "id": "integer UNIQUE",
        "pings": "json",
        "tz": "text"
    },
    "macros": {
        "name": "text",
        "content": "text",
        "guildid": "integer",
        "CONSTRAINT": "U_name_guildid UNIQUE (name, guildid)"
    },
    "responses": {
        "name": "text",
        "content": "json",
        "guildid": "integer",
        "memeonly": "integer",
        "CONSTRAINT": "U_name_guildid UNIQUE (name, guildid)"
    }
}
# Channel ids
CHANNELS = {
    "mm": {
        "memes": 1096717238553292882,
        "botspam": 1025318731137695814,
        "translators": 1133844392495554560,
        "member-general": 1027127053008515092,
        "modlogs": 1118925292589830236,
    }
}
# Channels where threads should be automatically created on message
AUTO_THREAD_CHANNELS = [
    CHANNELS["mm"]["memes"]
]
# Chem subscript
SUBSCRIPT = {
    "1": "₁",
    "2": "₂",
    "3": "₃",
    "4": "₄",
    "5": "₅",
    "6": "₆",
    "7": "₇",
    "8": "₈",
    "9": "₉",
    "0": "₀",
    "-": "₋"
}
# Servers
GUILDS = (
    discord.Object(1025316079226064966), # MM
    discord.Object(1099658057010651176), # GTB
    discord.Object(1165682213589876737) # HehVerse
)
# Command groups
GROUPS = {
    "macros": app_commands.Group(name="macro", description="Commands that are related to macros"),
    "times": app_commands.Group(name="times", description="Set your timezone/get another person's tz")
}
KJSPKG_PKGS_LINK = "https://raw.githubusercontent.com/Modern-Modpacks/kjspkg/main/pkgs.json" # Link to kjspkg's pkgs.json

statusi = None # Status ticker position

# EVENTS
@client.event
async def on_ready():
    for guild in GUILDS: # For every server in GUILDS
        if client.get_guild(guild.id)==None: continue # if the bot is not in the server, skip it

        for group in GROUPS.values(): tree.add_command(group, guild=guild) # Add the command groups

        if len(argv)>1 and argv[1]=="--sync": # If --sync is passed
            tree.copy_global_to(guild=guild) # Copy global commands locally
            await tree.sync(guild=guild) # Sync

    # Init db
    for table, contents in TABLES.items():
        items = []
        for name, value in contents.items(): items.append(name+" "+value)
        items = ",\n".join(items)

        dbcursor.execute(f"""CREATE TABLE IF NOT EXISTS {table} (
            {items}
        )""")
    db.commit()

	# Start flask servers
    Thread(target=lambda: server.run(port=9999)).start()
    Thread(target=run_server).start()
    # Start the status ticker animation
    update_status.start()

    print(f"Logged in as: {client.user}") # Notify when done
@client.event
async def on_message(message:discord.Message):
    if message.author.bot: return # Skip the message if the author is a bot

    # Create thread if message in AUTO_THREAD_CHANNELS
    thread = None
    if message.channel.id in AUTO_THREAD_CHANNELS: thread = await message.create_thread(name="Post by "+message.author.display_name)

    # Pings logic
    users = dbcursor.execute("SELECT * FROM users WHERE id != ?", [message.author.id]).fetchall() # Get all users except the author from db
    for id, pings, *_ in users:
        try: member = message.guild.get_member(id)
        except discord.NotFound: continue # If the member is not found, skip

        for ping in loads(pings): # For user's every ping trigger
            if search(r"\b"+ping+r"\b", message.content, IGNORECASE) and message.channel.permissions_for(member).read_messages: # Check if the word is in the message and the person can see the channel the message is in
                await member.send(f"You got pinged because you have \"{ping}\" as a word that you get pinged at. Message link: {message.jump_url}") # Send that person a DM
                break

    # Response logic
    responses = dbcursor.execute("SELECT * FROM responses WHERE guildid = ?", [message.guild.id]).fetchall() # Get all responses available in the current server from db
    for name, content, _, memeonly in responses: # For every automod response
        match = search(r"\b"+name+r"\b", message.content, IGNORECASE) # Check if the name/triggerword of the response is in the message

        content = loads(content) # Load content json
        if type(content)==list: content = choice(content) # Randomly select a value if the response is a list

        if match and f":{name}:" not in message.content.lower(): # If the trigger word is found and it's not a name of an emoji
            if not memeonly or message.channel.id in (CHANNELS["mm"]["memes"], CHANNELS["mm"]["botspam"]):
                if not content.startswith("$"): # If the $ prefix is not present
                    content = f"> {match[0]}\n\n{content}" # Add the quote to the message
                    if len(content)>2000: # If the message is larger than discord's limit, split it into chunks at spaces
                        chunks = []
                        chunk = ""
                        chunklength = 0

                        for i, word in enumerate(content.split(" ")):
                            chunklength += len(word)
                            if chunklength>=1500 or i==len(content.split(" "))-1:
                                if i==len(content.split(" "))-1: chunk += " "+word
                                chunks.append(chunk)
                                chunk = word
                                chunklength = len(word)
                            else: chunk += " "+word

                        # Send the first chunk with reply
                        if thread!=None: await thread.send(chunks[0])
                        else: await message.reply(chunks[0], mention_author=False)
                        for c in chunks[1:]: # Send all other chunks as regular messages
                            await (thread if thread!=None else message.channel).send(c)
                            await sleep(.25) # Delay between chunks
                    else: # If the message is less than 2000 chars
                        if thread!=None: await thread.send(content) # Send the response in thread if present
                        else: await message.reply(content, mention_author=False) # Send the response in the same channel if not
                else: # If the $ prefix is present, send the sticker with the response value
                    if thread!=None: await thread.send(stickers=[i for i in (await message.guild.fetch_stickers()) if i.name == content.removeprefix("$")])
                    else: await message.reply(stickers=[i for i in (await message.guild.fetch_stickers()) if i.name == content.removeprefix("$")], mention_author=False)

                await sleep(.5) # Delay between individual responses


@tree.error
async def on_error(interaction: interactions.Interaction, err: discord.app_commands.AppCommandError): # On error, log to dev chat
    errorbed = discord.Embed(color=discord.Color.red(), title="I AM SHITTING MYSELF!1!1", description=f"""Details:
```{format_exc()}```
Channel: <#{interaction.channel.id}>
User: <@{interaction.user.id}>
Time: <t:{round(interaction.created_at.timestamp())}:f>""")
    originalcommand = f"{interaction.command.name} "+" ".join([i["name"]+":"+(i["value"] if "value" in i.keys() else None) for i in interaction.data["options"]])
    errorbed.set_footer(text=f"The command that caused the error: \"/{originalcommand}\"")
    await (await client.fetch_channel(CHANNELS["mm"]["modlogs"])).send(embed=errorbed)

    errmsg = "Whoops, something has gone wrong! This incident was already reported to mods, they will get on fixing it shortly!"
    if interaction.response.is_done(): await interaction.followup.send(content=errmsg, ephemeral=True)
    else: await interaction.response.send_message(content=errmsg, ephemeral=True)

# TASKS
@tasks.loop(seconds=5)
async def update_status(): # Update the status ticker animation
    global statusi

    screen = 7 # Status size
    status = "🟥🟧🟨🟩🟦🟪⬛⬜🟫" # Status string

    if statusi==None: statusi = screen-1

    statusstring = status[-(screen-1):]+status # Slice the string
    await client.change_presence(activity=discord.Activity(state=statusstring[statusi:statusi+screen], name="Why the fuck do I have to define this it doesn't even show up", type=discord.ActivityType.custom)) # Show it
   
    # Loop
    if statusi+screen<len(statusstring): statusi += 1
    else: statusi = 0

# HELPER FUNCTIONS
def add_user_to_data(user:discord.User) -> None: # Add a user to the sqlite db
    dbcursor.execute(f"""INSERT OR IGNORE INTO users VALUES (
        ?,
        "[]",
        ""
    )""", [user.id])
    db.commit()
def fuzz_autocomplete(choices): # The fuzz autocomplete
    async def _autocomplete(interaction: interactions.Interaction, current:str) -> list: # Define an autocomplete coroutine
        if type(choices)==str: newchoices = [i[0] for i in dbcursor.execute(f"SELECT name FROM {choices} WHERE guildid = ?", [interaction.guild.id]).fetchall()] # If a string is passed, get all elements' names where guildid equals to the interaction guild id from a db table which has that name
        else: newchoices = list(choices) # Else, make sure that choices is a list
        return [app_commands.Choice(name=i, value=i) for i in ([v for v, s in process.extract(current, newchoices, limit=10) if s>60] if current else newchoices[:10])] # Find the closest ones based on fuzz
    return _autocomplete # Return the coroutine

# COMMANDS
@GROUPS["macros"].command(name="run", description="Sends a quick macro message to the chat")
@app_commands.autocomplete(name=fuzz_autocomplete("macros"))
async def macro(interaction:interactions.Interaction, name:str): # Run a macro
    name = name.lower()
    content = dbcursor.execute("SELECT content FROM macros WHERE guildid = ? AND name = ?", [interaction.guild.id, name]).fetchone()

    if not content:
        await interaction.response.send_message(content="Unknown macro: `"+name+"`", ephemeral=True)
        return
    content = content[0]

    if not content.startswith("@"): await interaction.response.send_message(content=content)
    else: await interaction.response.send_message(content=dbcursor.execute("SELECT content FROM macros WHERE guildid = ? AND name = ?", [interaction.guild.id, content.removeprefix("@")]).fetchone()[0]) # If the macro begins with @, link it to another macro
@GROUPS["macros"].command(name="list", description="Lists all available macros")
async def macrolist(interaction:interactions.Interaction): # List macros
    localmacros = dbcursor.execute(f"SELECT name FROM macros WHERE guildid = ?", [interaction.guild.id]).fetchall()

    if localmacros: await interaction.response.send_message(content=" | ".join([i[0] for i in localmacros]), ephemeral=True)
    else: await interaction.response.send_message(content="No macros found!", ephemeral=True)

@tree.command(name="chemsearch", description="Searches for a chemical compound based on the query.")
@app_commands.describe(query="Compound/Substance name or PubChem CID/SID", type="Search for Compounds/Substances. Optional, \"Compound\" by default", bettersearch="Enables better search feature, which might take longer. Optional, false by default")
@app_commands.choices(type=[app_commands.Choice(name=i, value=i) for i in ("Compound", "Substance")])
async def chemsearch(interaction:interactions.Interaction, query:str, type:str="compound", bettersearch:bool=False): # Search for chem compounds/substances
    await interaction.response.defer()

    type = type.lower()
    typeindex = 0 if type.lower()=="compound" else 1 # 0 if compound, 1 if substance
    results = None # Request result
    pubchemerr = None # Pub chem down error (if present)

    # While results are not defined
    while results==None:
        try: # Try to get them
            if query.isnumeric(): # If the query is a number, use that as cid/sid
                try: results = [(Compound.from_cid(int(query)) if typeindex==0 else Substance.from_sid(int(query)))]
                except (BadRequestError, ValueError): results = []
            else: # Else, search using it
                if typeindex==0: results = get_compounds(query, "name")
                else: results = get_substances(query, "name")
        except error.URLError: # If pubchem is down
            if pubchemerr==None: pubchemerr = await interaction.channel.send("It looks like pubchem is down, please wait a few minutes for it to go back online.") # Send a warning to the user (if it wasn't done already)
            await sleep(5) # 5 second cooldown
            continue

    if len(results)<1: 
        await interaction.followup.send(content=f"Whoops, {type} not found!") # Notify user is the compound/substance is not found
        return

    if bettersearch and not query.isnumeric(): # If bettersearch is enabled
        namedict = {(await http.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/{type}/{i.cid if typeindex==0 else i.sid}/JSON")).json()["Record"]["RecordTitle"]: i for i in results}
        result : (Compound if typeindex==0 else Substance) = namedict[process.extract(query, namedict.keys(), limit=1)[0][0]] # Use thefuzz search instead of the regular one (takes more time)
    else: result = results[0] # Else, use the basic one (worse results)
    
    id = result.cid if typeindex==0 else result.sid
    info = (await http.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/{type}/{id}/JSON")).json()["Record"] # Get info about the compound/substance

    def find_wikipedia_url(inf) -> str: # Find url to the wikipedia article
        names = [i for i in inf["Section"] if i["TOCHeading"]=="Names and Identifiers"] # Get names and identifiers
        if len(names)<1: return # Skip if not found
        names = names[0]

        other = [i for i in names["Section"] if i["TOCHeading"]=="Other Identifiers"] # Get other identifiers
        if len(other)<1: return # Skip if not found
        other = other[0]

        wikipedia = [i for i in other["Section"] if i["TOCHeading"]=="Wikipedia"] # Get the wikipedia identifier
        if len(wikipedia)<1: return # Skip if not found
        wikipedia = wikipedia[0]["Information"][0]["URL"]

        return wikipedia # Return the url
    def has_3d_conformer(inf) -> bool:
        structures = [i for i in inf["Section"] if i["TOCHeading"]=="Structures"] # Get structures
        if len(structures)<1: return False # Return false if they don't exist
        structures = structures[0]

        conformer = [i for i in structures["Section"] if i["TOCHeading"]=="3D Conformer"] # Get the 3d conformer
        if len(conformer)<1: return False # Return false if it doesn't exist
        conformer = conformer[0]

        return True

    # Get the wikipedia url using the find_wikipedia_url function if the chemical is a compound, else just use the lowercase name 
    wikipedia_url = find_wikipedia_url(info) if typeindex==0 else f"https://en.m.wikipedia.org/wiki/{parse.quote(info['RecordTitle']).lower()}"
    wikiinfo = None # Info from wikipedia
    if wikipedia_url!=None: # If wikipedia_url is defined
        wikiinfo = get(wikipedia_url.replace("/wiki/", "/api/rest_v1/page/summary/")) # Send a request to their url
        wikiinfo = wikiinfo.json() if wikiinfo.status_code==200 else None # Get the summary if the page was found

    if typeindex==0: # If the chemical is a compound
        formula = result.molecular_formula # Get the formula
        for k, v in SUBSCRIPT.items(): formula = formula.replace(k, v) # Replace numbers with the subscript

    # Create an embed with info
    chembed = discord.Embed(color=discord.Color.green(), title=info["RecordTitle"].title(), description="", url=f"https://pubchem.ncbi.nlm.nih.gov/{type}/{id}")
    chembed.set_footer(text=f"Info provided by PubChem. {type[0].upper()}ID: {id}")
    if typeindex==0: chembed.description += f"**Formula**: {formula}\n**Weight**: {result.molecular_weight}"
    if typeindex==0 and result.iupac_name!=None: chembed.description += f"\n**IUPAC Name**: {result.iupac_name}"
    if has_3d_conformer(info): chembed.description += f"\n**3D Conformer**: [Link](https://pubchem.ncbi.nlm.nih.gov/{type}/{id}#section=3D-Conformer&fullscreen=true)"
    if wikipedia_url!=None and wikiinfo!=None: chembed.description += f"\n\n[**From the wikipedia article**:]({wikipedia_url})\n{wikiinfo['extract']}"
    chembed.set_thumbnail(url=f"https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?{type[0]}id={id}&t=l")

    if pubchemerr!=None: await pubchemerr.delete() # Delete the "pubchem down" warning if present
    await interaction.followup.send(embed=chembed) # Send the embed

@tree.command(name = "pings", description = "Set your string pings")
@app_commands.describe(pings = "Words that will ping you, comma seperated, case insensitive")
async def editpings(interaction:interactions.Interaction, pings:str=""): # Set pings
    add_user_to_data(interaction.user)

    pings = [i.lower() for i in pings.replace(', ', ',').split(',')] if pings else []
    dbcursor.execute(f"UPDATE users SET pings = ? WHERE id = {interaction.user.id}", [dumps(pings)])
    db.commit()

    await interaction.response.send_message(content=f"Pings set! Your new pings are: `{','.join(pings)}`.", ephemeral=True)
@GROUPS["times"].command(name = "set", description = "Set your timezone")
@app_commands.describe(timezone = "Your timezone")
@app_commands.autocomplete(timezone=fuzz_autocomplete(all_timezones))
async def settz(interaction:interactions.Interaction, timezone:str): # Set timezone
    add_user_to_data(interaction.user)

    if timezone not in all_timezones:
        await interaction.response.send_message(f"Unknown timezone: `{timezone}`", ephemeral=True)
        return
    
    dbcursor.execute(f"UPDATE users SET tz = ? WHERE id = {interaction.user.id}", [timezone])
    db.commit()

    await interaction.response.send_message(content=f"Timezone set! Your new timezone is: `{timezone}`.", ephemeral=True)
@GROUPS["times"].command(name = "get", description = "Get yours or another user's timezone")
@app_commands.describe(user = "The user to get the timezone from")
async def gettz(interaction:interactions.Interaction, user:discord.User=None): # Get timezone
    if user==None: user = interaction.user

    add_user_to_data(interaction.user)
    selftz = dbcursor.execute(f"SELECT tz FROM users WHERE id = {interaction.user.id}").fetchone()[0]
    timezone = dbcursor.execute(f"SELECT tz FROM users WHERE id = {user.id}").fetchone()[0]

    if not timezone: # If the timezone is not set, notify the user
        await interaction.response.send_message(f"{user.display_name} hasn't set their timezone yet. If you want, ping them and tell them how to do so!", ephemeral=True)
        return

    for i in range(120): # For 2 minutes
        now = datetime.now(tz(timezone))

        # Create a new tz info embed
        tzbed = discord.Embed(color=user.color, title=f"{user.display_name}'s timezone")
        if user.avatar!=None: tzbed.set_thumbnail(url=user.avatar.url)
        else: tzbed.set_thumbnail(url=user.default_avatar.url)
        tzbed.description = f"""**Current time**: `{now.strftime("%d/%m/%Y, %H:%M:%S")}`

**Name**: `{timezone}`
**Abbreviation**: `{now.strftime("%Z")}`
**UTC offset**: `{now.strftime("%z")}`"""
        if selftz and user.id!=interaction.user.id: tzbed.description += f"\n**Offset from your timezone**: `{round((abs(now.replace(tzinfo=None)-datetime.now(tz(selftz)).replace(tzinfo=None)).seconds/3600)*100)/100}`"

        if i==0: # If it's the first second
            await interaction.response.send_message(embed=tzbed, ephemeral=True) # Send the response as a regular message
            sleep(datetime.now().microsecond / 1000000) # Sleep untill the next second
        else:
            await (await interaction.original_response()).edit(embed=tzbed) # Edit the already existing one
            await sleep(1) # Sleep 1 second
    
    await interaction.delete_original_response() # After 2 minutes, delete the response
    
@tree.command(name = "thisrecipedoesnotexist", description = "Generates and sends a random crafting table recipe")
@app_commands.choices(type=[app_commands.Choice(name=f"{i}x{i}", value=f"{i}x{i}") for i in range(3, 10, 2)])
@app_commands.describe(type="The type of crafting table", outputitem="Output item id", exportrecipe="Whether or not to export the recipe to a kjs/ct script format")
async def recipe(interaction:interactions.Interaction, type:str=None, outputitem:str=None, exportrecipe:bool=False): # TRDNE
    if outputitem!=None:
        if ":" not in outputitem: outputitem = "minecraft:"+outputitem
        if get_path(outputitem)==None:
            await interaction.response.send_message("No item found: `"+outputitem+"`", ephemeral=True)
            return

    await interaction.response.defer()

    # Save the image as temp and send it
    with BytesIO() as imgbin:
        img, links = create(type, outputitem, exportrecipe)
        img.save(imgbin, "PNG")
        imgbin.seek(0)

        buttons = discord.ui.View()
        if links!=None: buttons.add_item(discord.ui.Button(label="KubeJS", url=links[0])) # If exportrecipe is passed, create and send the link to the kjs exported recipe
        await interaction.followup.send(file=discord.File(fp=imgbin, filename=f"recipe{type}.png"), view=buttons)

@tree.command(name = "kjspkglookup", description = "Gets info about a KJSPKG package")
@app_commands.autocomplete(package=fuzz_autocomplete(sorted(get(KJSPKG_PKGS_LINK).json().keys())))
@app_commands.describe(package="Package name")
async def kjspkg(interaction:interactions.Interaction, package:str): # kjspkglookup
    # Create an embed
    kjsbed = discord.Embed(color=discord.Color.from_str("#460067"), title=package.replace("-", " ").title(), url="https://kjspkglookup.modernmodpacks.site/#"+package)
    kjsbed.set_thumbnail(url="https://raw.githubusercontent.com/Modern-Modpacks/assets/main/Icons/Other/kjspkg.png")

    repostr = get(KJSPKG_PKGS_LINK).json()[package]
    repo = repostr.split("$")[0]
    path = repostr.split("$")[-1].split("@")[0]+"/" if "$" in repostr else ""
    branch = repostr.split("@")[-1] if "@" in repostr else "main"
    infourl = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}.kjspkg"
    info = get(infourl).json()

    # Fill the embed with info
    kjsbed.description = f"""**{info["description"]}**
[**Source**](https://github.com/{repo})

**Versions**: {", ".join([f"1.{i+10}" for i in info["versions"]])}
**Modloaders**: {", ".join([i.title() for i in info["modloaders"]])}"""

    # Add deps and incompats if present
    if ("dependencies" in info.keys() and info["dependencies"]) or ("incompatibilities" in info.keys() and info["incompatibilities"]): kjsbed.description += "\n"
    if "dependencies" in info.keys() and info["dependencies"]: kjsbed.description += "\n**Dependencies**: "+", ".join([f"{i.split(':')[0].title()} ({i.split(':')[1].title()})" if ":" in i else i.title() for i in info["dependencies"]])
    if "incompatibilities" in info.keys() and info["incompatibilities"]: kjsbed.description += "\n**Incompatibilities**: "+", ".join([f"{i.split(':')[0].title()} ({i.split(':')[1].title()})" if ":" in i else i.title() for i in info["incompatibilities"]])

    # Add commands
    kjsbed.description += f"""

**Commands**:
`kjspkg install {package}` to install
`kjspkg remove {package}` to remove
`kjspkg update {package}` to update
`kjspkg pkg {package}` to see more info"""

    # Get the repo's author avatar from github using its api
    authoravatar = None
    ghinfo = get("https://api.github.com/repos/"+repo, headers={"Authorization": "Bearer "+getenv("GITHUB_KEY")} if getenv("GITHUBKEY")!=None else {})
    if ghinfo.status_code==200:
        ghinfo = ghinfo.json()
        authoravatar = ghinfo["owner"]["avatar_url"]

    kjsbed.set_footer(text=f"Package made by {info['author']}. Info provided by KJSPKG.", icon_url=authoravatar) # Set the footer

    await interaction.response.send_message(embed=kjsbed) # Send the embed

# FLASK ENDPOINTS

# Status checker
@server.get("/")
async def on_root_get():
	return "OK" # Return 👍

# Github translator webhook
@server.post("/translators")
async def on_translator_webhook():
    data = loads(request.get_data()) # Change data
    commit = data["commits"][0] if data["commits"] else data["head_commit"] # Get the head commit
    changed_files = [i for i in commit["added"]+commit["modified"] if i.replace("-", "_").lower().endswith("en_us.json")] # All files named "en_us.json" or similar that were changed

    if changed_files: # If any files are in changed_files
        url = data["repository"]["url"]
        blob = f"{url}/blob/{data['repository']['default_branch']}"

        # Create an embed with info
        transbed = discord.Embed(color = discord.Color.purple(), title = "Lang file(s) changed!", url=url)
        transbed.description = "Changed files:\n\n"+"\n".join([f"[{i}]({blob}/{i})" for i in changed_files])
        transbed.set_thumbnail(url = blob + "/src/main/resources/pack.png?raw=true")
        transbed.set_footer(text = "Changed mod: "+data["repository"]["name"].replace("-", " ").title())

        # Send the message
        translators = run_coroutine_threadsafe(run_coroutine_threadsafe(client.fetch_guild(GUILDS[0].id), client.loop).result().fetch_channel(CHANNELS["mm"]["translators"]), client.loop).result()
        run_coroutine_threadsafe(translators.send(content="<@&1126286016781762680>", embed=transbed), client.loop)

    return "OK" # Return 👍

# START BOT
try:
    token = getenv("DISCORD_KEY") # Get the key from env
    if token!=None: client.run(token) # Launch the bot if it's present
    else: print("Token not found!") # Else, quit
except KeyboardInterrupt: pass # Kill the bot on ctrl+c
