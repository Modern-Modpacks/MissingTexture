# IMPORTS

# Disable the fuzz warning
from warnings import filterwarnings
filterwarnings("ignore")

# Discord.py and related
import discord
from discord import NotFound, app_commands, interactions, ui
from discord.ext import tasks

# System stuff
from asyncio import sleep, coroutine
from os import getenv
from io import BytesIO
from threading import Thread
from traceback import format_exc

# Other built-in modules
from re import search, IGNORECASE
from random import choice
from json import loads, dumps
from sqlite3 import connect
from math import floor

# Dates and times
from datetime import datetime
from time import time
from pytz import all_timezones
from pytz import timezone as tz

# Web-related stuff
from flask import Flask
from requests import get, post
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
    "channels": {
        "id": "integer UNIQUE",
        "tags": "json"
    },
    "users": {
        "id": "integer UNIQUE",
        "pings": "json",
        "tz": "text",
        "trello": "text"
    },
    "macros": {
        "name": "text",
        "content": "text",
        "authorid": "integer",
        "timecreated": "integer",
        "timelastedited": "integer",
        "guildid": "integer",
        "uses": "integer",
        "CONSTRAINT": "U_name_guildid UNIQUE (name, guildid)"
    },
    "responses": {
        "name": "text",
        "content": "json",
        "authorid": "integer",
        "guildid": "integer",
        "memeonly": "integer",
        "CONSTRAINT": "U_name_guildid UNIQUE (name, guildid)"
    },

    "directdemocracy": {
        "channelid": "integer",
        "messageid": "integer",
        "secondannouncementsent": "integer"
    }
}
# Channel ids
CHANNELS = {
    "mm": {
        "translators": 1133844392495554560
    }
}
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
# Command groups
GROUPS = {
    "macros": app_commands.Group(name="macro", description="Commands that are related to macros"),
    "responses": app_commands.Group(name="response", description="Commands that are related to responses", default_permissions=discord.Permissions(8192)),
    "times": app_commands.Group(name="times", description="Set your timezone/get another person's tz")
}
KJSPKG_PKGS_LINK = "https://raw.githubusercontent.com/Modern-Modpacks/kjspkg/main/pkgs.json" # Link to kjspkg's pkgs.json
# directdemocracy tag consts
DEMOCRACY_SECOND_LOOP = 86400
POSITIVE_EMOTE = "<:hehehehaw:1222078888486895647>"
NEGATIVE_EMOTE = "<:grrr:1222078966341308506>"
PINGABLE_ROLE = "<@&1207441060666806312>"
IDEA_REGEX = r"^(.{1,35})\n*([\S\s]*)$"
TRELLO_LIST_ID = "65bfd68b1c0e6d367fe35bb8"

statusi = None # Status ticker position
logchannels : list[discord.TextChannel] = [] # Channels where the logs should be sent to

# EVENTS
@client.event
async def on_ready():
    async for guild in client.fetch_guilds(): # For every server in the bot is in
        if client.get_guild(guild.id)==None: continue # If the bot is not in the server, skip it
        await register_commands_on_guild(guild) # Otherwise, register the commands on it

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

    # Start the loops
    update_status.start()
    directdemocracy_loop.start()

    # Check and un-archive keepalive threads + get log channels
    channels = dbcursor.execute("SELECT * FROM channels").fetchall() # Get all known channels
    for id, tags in channels: # For each channel
        channel = await client.fetch_channel(id) # Fetch the channel
        if type(channel)==discord.Thread and channel.archived and "keepalive" in loads(tags): await unarchive_thread(channel) # If the thread is tagged "keepalive" and is archived, un-archive it
        if "log" in loads(tags): logchannels.append(channel) # If the channel is tagged "log", add it to log channel list

    print(f"Logged in as: {client.user}") # Notify when done
    await send_log_message(discord.Embed(title="I'm online again!", description="Hello world!", timestamp=datetime.today(), color=discord.Color.green()).set_thumbnail(url=get_user_pfp(client.user))) # Notify through discord
@client.event
async def on_guild_join(guild: discord.Guild): register_commands_on_guild(guild) # Add the commands to the server whenever the bot joins one
@client.event
async def on_message(message:discord.Message):
    if message.author.bot: return # Skip the message if the author is a bot
    guild = message.guild

    # Create thread if the channel has the appropriate tag
    thread = None
    if channel_has_tag(message.channel.id, "autothread"): thread = await message.create_thread(name="Post by "+message.author.display_name)

    # Add votes for directdemocracy tagged channels and add the message to db
    if channel_has_tag(message.channel.id, "directdemocracy"):
        if not search(IDEA_REGEX, message.content): # If the message is formatted wrongly according to regex, close it
            await message.add_reaction("<:red_cross_mark:1222622729845346414>")
            await thread.send("Invalid idea format.")
            await thread.edit(locked=True)
        else:
            await message.add_reaction(POSITIVE_EMOTE)
            await message.add_reaction(NEGATIVE_EMOTE)
            await thread.send(PINGABLE_ROLE)

            execute_and_commit("INSERT INTO directdemocracy (channelid, messageid, secondannouncementsent) VALUES (?, ?, ?)", [message.channel.id, message.id, 0])

    # Pings logic
    users = dbcursor.execute("SELECT * FROM users WHERE id != ?", [message.author.id]).fetchall() # Get all users except the author from db
    for id, pings, *_ in users:
        try: member = guild.get_member(id)
        except discord.NotFound: continue # If the member is not found, skip

        for ping in loads(pings): # For user's every ping trigger
            if search(r"\b"+ping+r"\b", message.content, IGNORECASE) and message.channel.permissions_for(member).read_messages: # Check if the word is in the message and the person can see the channel the message is in
                await member.send(f"You got pinged because you have \"{ping}\" as a word that you get pinged at. Message link: {message.jump_url}") # Send that person a DM
                break

    # Response logic
    ismeme = channel_has_tag(message.channel.id, "meme")
    responses = dbcursor.execute("SELECT * FROM responses WHERE guildid = ?", [guild.id]).fetchall() # Get all responses available in the current server from db
    for name, content, _authorid, _guildid, memeonly in responses: # For every automod response
        match = search(r"\b"+name+r"\b", message.content, IGNORECASE) # Check if the name/triggerword of the response is in the message
        content = choice(loads(content)) # Randomly select a value from the responses

        if (
            not match or f":{name}:" in message.content.lower() # If the trigger word is found and it's not a name of an emoji
            or (memeonly and not ismeme)
        ): continue
        
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
            if thread!=None: await thread.send(stickers=[i for i in (await guild.fetch_stickers()) if i.name == content.removeprefix("$")])
            else: await message.reply(stickers=[i for i in (await guild.fetch_stickers()) if i.name == content.removeprefix("$")], mention_author=False)

        await sleep(.5) # Delay between individual responses
@client.event
async def on_thread_update(before:discord.Thread, after:discord.Thread): # Keep threads alive
    if not channel_has_tag(after.id, "keepalive"): return # Check for "keepalive" tag
    if not before.archived and after.archived: await unarchive_thread(after) # Un-archive the keepalive thread

@tree.error
async def on_error(interaction: interactions.Interaction, err: discord.app_commands.AppCommandError): # On error, log to dev chat
    errorbed = discord.Embed(color=discord.Color.red(), title="I AM SHITTING MYSELF!1!1", description=f"""Details:
```
{format_exc()}
```
Channel: <#{interaction.channel.id}>
User: <@{interaction.user.id}>
Time: <t:{round(interaction.created_at.timestamp())}:f>""")
    if interaction.command!=None:
        originalcommand = f"{interaction.command.name} "+" ".join([i["name"]+(':'+i["value"] if "value" in i.keys() else '') for i in interaction.data["options"]])
        errorbed.set_footer(text=f"The command that caused the error: \"/{originalcommand}\"")
    await send_log_message(errorbed)

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
@tasks.loop(seconds=DEMOCRACY_SECOND_LOOP)
async def directdemocracy_loop(): # directdemocracy tag logic
    ideas = dbcursor.execute("SELECT * FROM directdemocracy").fetchall() # Get all uncompleted messages
    for channelid, messageid, secondannouncementsent in ideas: # For uncompleted message
        try: message = await (await client.fetch_channel(channelid)).fetch_message(messageid) # Get the message object
        except NotFound: # If the message was removed, yeet it from the db
            execute_and_commit(f"DELETE FROM directdemocracy WHERE messageid = ?", [messageid])
            continue

        author = message.author # Get the author
        reactions = message.reactions # Get the reactions
        thread = await message.fetch_thread() # Get the thread underneath the message

        # Count the positive and negative reactions
        positives = 0
        negatives = 0
        for r in reactions:
            users = [user.id async for user in r.users()]
            if str(r.emoji) == POSITIVE_EMOTE: positives = r.count - (2 if author.id in users else 1)
            elif str(r.emoji) == NEGATIVE_EMOTE: negatives = r.count - (2 if author.id in users else 1)

        if not positives and not negatives and not secondannouncementsent: # If there is no reactions, remind people to add them
            await thread.send(f"{PINGABLE_ROLE} The poll for this idea has received no activity for a long time. If no votes will be added in the next {DEMOCRACY_SECOND_LOOP} seconds, it will be automatically accepted.")
            execute_and_commit(f"UPDATE directdemocracy SET secondannouncementsent = 1 WHERE messageid = ?", [messageid])
        elif negatives > positives: execute_and_commit(f"UPDATE directdemocracy SET secondannouncementsent = 1 WHERE messageid = ?", [messageid]) # If there is more negatives than positives, wait and don't send the reminder
        else: # If there is more positives than negatives
            execute_and_commit(f"DELETE FROM directdemocracy WHERE messageid = ?", [messageid]) # Mark as complete by deleting

            await message.add_reaction("✅") # Add a confirming reaction
            await thread.send(f"{PINGABLE_ROLE} Idea passed.") # Remind everyone that it has been passed
            await thread.edit(locked=True) # Lock the thread

            title, description = search(IDEA_REGEX, message.content).groups() # Get title and description using regex
            authortrello = dbcursor.execute(f"SELECT trello FROM users WHERE id = {author.id}").fetchone()[0] # Get author's trello
            if authortrello: description += "\n---\nSuggested by @"+authortrello # Mention author if his trello is in the db
            post("https://api.trello.com/1/cards", headers={"Accept": "application/json"}, params={ # Make a new card on trello
                "key": getenv("TRELLO_KEY"),
                "token": getenv("TRELLO_TOKEN"),

                "idList": TRELLO_LIST_ID,
                "name": title,
                "desc": description 
            })

# HELPER FUNCTIONS
def add_user_to_data(user:discord.User) -> None: # Add a user to the sqlite db
    execute_and_commit(f"""INSERT OR IGNORE INTO users VALUES (
        ?,
        "[]",
        "",
        ""
    )""", [user.id])
def fuzz_autocomplete(choices): # The fuzz autocomplete
    async def _autocomplete(interaction: interactions.Interaction, current:str) -> list: # Define an autocomplete coroutine
        if type(choices)==str: newchoices = [i[0] for i in dbcursor.execute(f"SELECT name FROM {choices} WHERE guildid = ?", [interaction.guild.id]).fetchall()] # If a string is passed, get all elements' names where guildid equals to the interaction guild id from a db table which has that name
        else: newchoices = list(choices) # Else, make sure that choices is a list
        return [app_commands.Choice(name=i, value=i) for i in ([v for v, s in process.extract(current, newchoices, limit=10) if s>60] if current else newchoices[:10])] # Find the closest ones based on fuzz
    return _autocomplete # Return the coroutine
def execute_and_commit(instruction:str, params:list=[]): # Execute a sql command and commit
    db.execute(instruction, params)
    db.commit()
def channel_has_tag(id:int, tag:str) -> bool: # Check if the provided channel has the proived tag in the db
    channeltags = dbcursor.execute("SELECT tags FROM channels WHERE id = ?", [id]).fetchone() # Get the tags channel from db
    if channeltags==None: return False

    channeltags = loads(channeltags[0])
    return tag in channeltags
def get_user_pfp(user:discord.User) -> str: # Get user pfp or return the default one
    if user.avatar!=None: return user.avatar.url
    return user.default_avatar.url
def insert_macro(name:str, content:str, interaction:discord.Interaction): # Insert a macro into the db
    execute_and_commit("INSERT INTO macros (name, content, authorid, timecreated, timelastedited, guildid, uses) VALUES (?, ?, ?, ?, ?, ?, ?)", [name, content, interaction.user.id, floor(time()), floor(time()), interaction.guild.id, 0])
async def register_commands_on_guild(guild:discord.Guild) -> None: # Register commands on a guild
    for group in GROUPS.values(): tree.add_command(group, guild=guild) # Add the command groups
    tree.copy_global_to(guild=guild) # Copy global commands locally
    await tree.sync(guild=guild) # Sync
async def send_log_message(embed:discord.Embed): # Send an embed to log channels
    for c in logchannels: await c.send(embed=embed)
async def send_macroesque_log_message(noun:str, name:str, content:str, previouscontent:str, authorid:int, user:discord.User, guild:discord.Guild, action:str, color:discord.Colour): # Send a log message that's related to macros
    sep = "\n"
    macrobed = discord.Embed(color=color, title=f"A {noun} has been {action.lower()}!", description=f"""Details:

Server: **{guild.name}**
Name: `{name}`
Creator: <@{authorid}>{sep+f'''Old content: ```
{previouscontent}
```''' if previouscontent else ''}
{'New c' if previouscontent else 'C'}ontent: ```
{content}
```""")
    macrobed.set_thumbnail(url=guild.icon.url)
    macrobed.set_footer(text=f"{action.title()} by @{user.name}", icon_url=get_user_pfp(user))
    await send_log_message(macrobed)
async def unarchive_thread(thread:discord.Thread): # Unarchive thread by sending a ping message and quickly deleting it
    await (await thread.send(".")).delete()

# HELPER CLASSES
class ConfirmaionView(ui.View): # Yes/No view prompt
    def __init__(self, callback: coroutine):
        super().__init__()
        self.callback = callback
    
    @ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="✅")
    async def confirm(self, interaction: discord.Interaction, _button: ui.Button): # If yes is clicked, call the callback
        await interaction.response.defer()
        await interaction.delete_original_response()
        await self.callback()
    @ui.button(label="No", style=discord.ButtonStyle.red, emoji="<:red_cross_mark:1222622729845346414>")
    async def cancel(self, interaction: discord.Interaction, _button: ui.Button): await interaction.response.edit_message(content="Action aborted!", view=None, embed=None) # If no is clicked, abort the action
class AddOrEditModal(ui.Modal): # /macro or /response add/edit modal
    content = ui.TextInput(label="Content", style=discord.TextStyle.paragraph) # The content of the macro/response

    def __init__(self, name:str, precontent:str="", isresponse:bool=False, memeonly:bool=None):
        self.name = name # The name of the macro/response
        self.precontent = "|;".join(loads(precontent)) if isresponse and precontent else precontent # The previous content of the macro/response
        self.isresponse = isresponse # What is being added/modified, macro or response
        self.memeonly = memeonly # If the response is meme channel only
        self.noun = "response" if isresponse else "macro" # Select the correct noun

        self.content.default = self.precontent # Set the content if already exists
        super().__init__(title=f"{'Editing' if precontent else 'Adding'} \"{name}\" {self.noun}") # Set the title (adding if doesn't exist, editing if does)

    async def on_submit(self, interaction: discord.Interaction): # When the modal is sumbitted
        content = dumps(self.content.value.split("|;")) if self.isresponse else self.content.value

        if self.precontent: execute_and_commit(f"UPDATE {self.noun}s SET content = ?, {'memeonly' if self.isresponse else 'timelastedited'} = ? WHERE name = ? AND guildid = ?", [content, (int(self.memeonly) if self.isresponse else floor(time())), self.name, interaction.guild.id]) # Edit the macro/response if it exists
        else: # Insert macro/response into the db if doesn't exist
            if self.isresponse: execute_and_commit("INSERT INTO responses (name, content, authorid, guildid, memeonly) VALUES (?, ?, ?, ?, ?)", [self.name, content, interaction.user.id, interaction.guild.id, int(self.memeonly)])
            else: insert_macro(self.name, content, interaction)

        verb = "edited" if self.precontent else "added" # Get the correct action (added if doesn't exist, edited if does)
        await send_macroesque_log_message(self.noun, self.name, self.content.value, self.precontent, interaction.user.id, interaction.user, interaction.guild, verb, (discord.Color.yellow() if self.precontent else discord.Color.purple())) # Notify the mods
        await interaction.response.send_message(f"{self.noun.title()} `{self.name}` has successfully been {verb}!", ephemeral=True) # Yipee

# COMMANDS
@GROUPS["macros"].command(name="run", description="Sends a quick macro message to the chat")
@app_commands.autocomplete(name=fuzz_autocomplete("macros"))
@app_commands.describe(name="The name of the macro you want to run")
async def macro(interaction:interactions.Interaction, name:str): # Run a macro
    name = name.lower()
    content = dbcursor.execute("SELECT content FROM macros WHERE guildid = ? AND name = ?", [interaction.guild.id, name]).fetchone()

    if not content:
        await interaction.response.send_message(content="Unknown macro: `"+name+"`", ephemeral=True)
        return
    content = content[0]

    # Find the alias if the macro content begins with @
    alias = None
    if content.startswith("@"):
        aliasname = content.removeprefix("@")
        alias = dbcursor.execute("SELECT content FROM macros WHERE guildid = ? AND name = ?", [interaction.guild.id, aliasname]).fetchone()

    if alias!=None: await interaction.response.send_message(content=alias[0]) # Send the contents of the linked macro if found
    else: await interaction.response.send_message(content=content) # Otherwise, send the content of the macro itself

    execute_and_commit("UPDATE macros SET uses = uses + 1 WHERE guildid = ? AND name = ?", [interaction.guild.id, (aliasname if alias!=None else name)]) # Add +1 use to either the macro itself or the linked one
@GROUPS["macros"].command(name="list", description="Lists all available macros")
async def macrolist(interaction:interactions.Interaction): # List macros
    localmacros = dbcursor.execute(f"SELECT name FROM macros WHERE guildid = ?", [interaction.guild.id]).fetchall()

    if localmacros: await interaction.response.send_message(content=" | ".join([i[0] for i in localmacros]), ephemeral=True)
    else: await interaction.response.send_message(content="No macros found!", ephemeral=True)
@GROUPS["macros"].command(name="info", description="Get info about a macro")
@app_commands.autocomplete(name=fuzz_autocomplete("macros"))
@app_commands.describe(name="The name of the macro you want to get info about")
async def macroinfo(interaction:interactions.Interaction, name:str): # Get info about a macro
    name = name.lower()
    selectedmacro = dbcursor.execute("SELECT * FROM macros WHERE guildid = ? AND name = ?", [interaction.guild.id, name]).fetchone()

    if not selectedmacro:
        await interaction.response.send_message(content="Unknown macro: `"+name+"`", ephemeral=True)
        return

    macrobed = discord.Embed(title=f"`{name}` macro", description=f"""Author: <@{selectedmacro[2]}>
{f'**Alias macro for `{selectedmacro[1].removeprefix("@")}`**' if selectedmacro[1].startswith("@") else f'Uses: {selectedmacro[6]}'}
Created on: <t:{selectedmacro[3]}:f>
Last modified on: <t:{selectedmacro[4]}:f>""", color=discord.Color.blurple())
    await interaction.response.send_message(embed=macrobed)

async def macroeqsueadd(interaction:interactions.Interaction, name:str, isresponse:bool, memeonly:bool, openmodal:bool): # Add a macro/response
    name = name.lower()
    noun = "response" if isresponse else "macro"

    if not interaction.user.guild_permissions.manage_messages: # Check perms
        await interaction.response.send_message(f"You don't have enough permissions to add {noun}s to this server. {'Not neat!' if isresponse else 'Tough luck!'}", ephemeral=True)
        return
    
    if dbcursor.execute(f"SELECT * FROM {noun}s WHERE name = ? AND guildid = ?", [name, interaction.guild.id]).fetchone()!=None: # Check if the macro/response of the same name exists on the server
        await interaction.response.send_message(f"{noun.title()} `{name}` already exists on this server. Try a different name", ephemeral=True) # Refuse to add
        return
    
    if openmodal: await interaction.response.send_modal(AddOrEditModal(name, "", isresponse, memeonly)) # Open the modal
@GROUPS["macros"].command(name="add", description="Add a macro")
@app_commands.autocomplete(alias=fuzz_autocomplete("macros"))
@app_commands.describe(name="The name of the macro you want to add", alias="Enter the name of another macro if you want to create an alias macro (will just respond with the same message)")
async def macroadd(interaction:interactions.Interaction, name:str, alias:str=""): # Add a macro
    await macroeqsueadd(interaction, name, False, None, not alias)
    if not alias: return 
        
    content = "@"+alias
    insert_macro(name, content, interaction) # Insert alias macro into the db
    await send_macroesque_log_message("macro", name, content, "", interaction.user.id, interaction.user, interaction.guild, "created", discord.Color.purple())
    await interaction.response.send_message(f"Alias macro `{name}` successfully created and linked to `{alias}`!", ephemeral=True) # Yay
@GROUPS["responses"].command(name="add", description="Add an automod response. Use \"|;\" as a random separator")
@app_commands.describe(name="The trigger word of the response you want to add", memeonly="Whether you want the response to only work in channels tagged as 'meme'")
async def responseadd(interaction:interactions.Interaction, name:str, memeonly:bool=True): # Add a response
    await macroeqsueadd(interaction, name, True, memeonly, True)
async def macroesqueedit(interaction:interactions.Interaction, name:str, isresponse:bool, memeonly:bool): # Edit a macro/response
    name = name.lower()
    noun = "response" if isresponse else "macro"
    selected = dbcursor.execute(f"SELECT content, authorid{', memeonly' if isresponse else ''} FROM {noun}s WHERE guildid = ? AND name = ?", [interaction.guild.id, name]).fetchone()

    if not selected: # Check if the response/macro already exists
        await interaction.response.send_message(content=f"Unknown {noun}: `{name}`", ephemeral=True) # Refuse to edit if it doesn't
        return

    if not interaction.user.guild_permissions.administrator and interaction.user.id!=selected[1]: # Check perms
        await interaction.response.send_message(f"You don't have enough permissions to edit the `{name}` {noun}. Sorry!", ephemeral=True)
        return
    
    if isresponse and memeonly==None: memeonly = selected[2]
    await interaction.response.send_modal(AddOrEditModal(name, selected[0], isresponse, memeonly)) # Open the modal
@GROUPS["macros"].command(name="edit", description="Edit a macro")
@app_commands.autocomplete(name=fuzz_autocomplete("macros"))
@app_commands.describe(name="The name of the macro you want to edit")
async def macroedit(interaction:interactions.Interaction, name:str): # Edit a macro
    await macroesqueedit(interaction, name, False, None)
@GROUPS["responses"].command(name="edit", description="Edit an automod response. Use \"|;\" as a random separator")
@app_commands.autocomplete(name=fuzz_autocomplete("responses"))
@app_commands.describe(name="The name of the response you want to edit", memeonly="Whether you want the response to only work in channels tagged as 'meme'")
async def responseedit(interaction:interactions.Interaction, name:str, memeonly:bool=None): # Edit a response
    await macroesqueedit(interaction, name, True, memeonly)
async def macroesqueremove(interaction:interactions.Interaction, name:str, isresponse:bool): # Remove a macro/response
    name = name.lower()
    noun = "response" if isresponse else "macro"
    selected = dbcursor.execute(f"SELECT content, authorid FROM {noun}s WHERE guildid = ? AND name = ?", [interaction.guild.id, name]).fetchone()

    if not selected: # Check if the response/macro already exists
        await interaction.response.send_message(content=f"Unknown {noun}: `{name}`", ephemeral=True) # Refuse to remove if it doesn't
        return

    if not interaction.user.guild_permissions.administrator and interaction.user.id!=selected[1]: # Check perms
        await interaction.response.send_message(f"You don't have enough permissions to remove the `{name}` {noun}. Sorry!", ephemeral=True)
        return
    
    async def delete():
        execute_and_commit(f"DELETE FROM {noun}s WHERE guildid = ? AND name = ?", [interaction.guild.id, name]) # Remove the macro/response from db

        content = "|;".join(loads(selected[0])) if isresponse else selected[0]
        await send_macroesque_log_message(noun, name, content, "", selected[1], interaction.user, interaction.guild, "removed", discord.Color.red()) # Notify the mods
        await interaction.followup.send(content=f"{noun.title()} `{name}` successfully removed!", ephemeral=True) # Kill

    await interaction.response.send_message(
        embed=discord.Embed(title=f"Are you sure you want to remove the `{name}` {noun}?", color=discord.Color.red()),
        view=ConfirmaionView(delete),
        ephemeral=True
    ) # Confirmation
@GROUPS["macros"].command(name="remove", description="Remove a macro")
@app_commands.autocomplete(name=fuzz_autocomplete("macros"))
@app_commands.describe(name="The name of the macro you want to remove")
async def macroremove(interaction:interactions.Interaction, name:str): # Remove a macro
    await macroesqueremove(interaction, name, False)
@GROUPS["responses"].command(name="remove", description="Remove an automod response")
@app_commands.autocomplete(name=fuzz_autocomplete("responses"))
@app_commands.describe(name="The name of the response you want to remove")
async def responseremove(interaction:interactions.Interaction, name:str): # Remove a response
    await macroesqueremove(interaction, name, True)

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
    execute_and_commit(f"UPDATE users SET pings = ? WHERE id = {interaction.user.id}", [dumps(pings)])

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
        tzbed.set_thumbnail(url=get_user_pfp(user))
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
    
@tree.command(name = "thisrecipedoesnotexist", description = "Generate a random crafting table recipe")
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

        buttons = ui.View()
        if links!=None: buttons.add_item(ui.Button(label="KubeJS", url=links[0])) # If exportrecipe is passed, create and send the link to the kjs exported recipe
        await interaction.followup.send(file=discord.File(fp=imgbin, filename=f"recipe{type}.png"), view=buttons)

@tree.command(name = "kjspkglookup", description = "Get info about a KJSPKG package")
@app_commands.autocomplete(package=fuzz_autocomplete(sorted(get(KJSPKG_PKGS_LINK).json().keys())))
@app_commands.describe(package="Package name")
async def kjspkg(interaction:interactions.Interaction, package:str): # kjspkglookup
    # Create an embed
    kjsbed = discord.Embed(color=discord.Color.from_str("#460067"), title=package.replace("-", " ").title(), url="https://kjspkglookup.modernmodpacks.site/#"+package)
    kjsbed.set_thumbnail(url="https://raw.githubusercontent.com/Modern-Modpacks/assets/main/Icons/Other/kjspkg.png")

    repostr = get(KJSPKG_PKGS_LINK).json()[package]
    repo = repostr.split("$")[0].split("@")[0]
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
    ghinfo = get("https://api.github.com/repos/"+repo, headers={"Authorization": "Bearer "+getenv("GITHUB_KEY")} if getenv("GITHUB_KEY")!=None else {})
    if ghinfo.status_code==200:
        ghinfo = ghinfo.json()
        authoravatar = ghinfo["owner"]["avatar_url"]

    kjsbed.set_footer(text=f"Package made by {info['author']}. Info provided by KJSPKG.", icon_url=authoravatar) # Set the footer

    await interaction.response.send_message(embed=kjsbed) # Send the embed

@tree.command(name = "eval", description = "Execute JS code")
@app_commands.describe(code="The inline code to execute")
async def eval(interaction:interactions.Interaction, code:str): # eval
    await interaction.response.send_message(file=discord.File(BytesIO(get("https://eval-deez-nuts.xyz/static/eval-deez-nuts.mp3").content), filename="result.mp3")) # :troll:

# FLASK ENDPOINTS

# Status checker
@server.get("/")
async def on_root_get():
	return "OK" # Return 👍

# START BOT
try:
    token = getenv("DISCORD_KEY") # Get the key from env
    if token!=None: client.run(token) # Launch the bot if it's present
    else: print("Token not found!") # Else, quit
except KeyboardInterrupt: pass # Kill the bot on ctrl+c
