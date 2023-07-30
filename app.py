# Read the following as a haiku:
#
# This code is so bad
# But it works surprisingly
# So no touchy touch

import discord
from discord import app_commands, interactions
from discord.ext import tasks
from re import search, IGNORECASE
from sys import argv
from os import _exit, path
from time import time
from json import loads, load, dump
from logging import getLogger
from subprocess import Popen, DEVNULL
from quart import Quart, request

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

server = Quart(__name__)
getLogger("werkzeug").disabled = True

RESPONSES = {
    "neat": "Neat is a mod by Vazkii",
    "nether chest": "Nether Chest",
    "rats": "Heehee, humorous rodent modification.",
    "sex": "Where sex",

    "^bigbee": "$Bigbee",
    "^quan": "$Quantum Chromodynamic Charge",

    "^rftools": "RFTools is a mod by Vazkii",
    "^greg": "STOP POSTING ABOUT GREGTECH, I'M TIRED OF SEEING IT! My friends on reddit send me memes, on discord it's fucking memes - I was in a subreddit, right? and ALLLLLLLLL of the POSTS are just GregTech stuff. I- I showed my Champion underwear to my girlfriend, and the logo I flipped it and I said, \"Hey babe: When the underwear greg :joy: :joy: :joy:\"",

    "^1.18": "Alright glad I just removed the integration and pushed my update today without it. Maybe I'll get around to using it when you aren't so rude. Fuck me for wanting to use your mod and not knowing if you were working on it since you had no 1.18 branch or anything. Man I even made this not a bug so it wouldn't fuck up metrics. And I said please and thanks, and didn't give you my life story or whatever. Jesus man don't mod if it makes you unhappy to update.",
    "^1.19": "Alright glad I just removed the integration and pushed my update today without it. Maybe I'll get around to using it when you aren't so rude. Fuck me for wanting to use your mod and not knowing if you were working on it since you had no 1.19 branch or anything. Man I even made this not a bug so it wouldn't fuck up metrics. And I said please and thanks, and didn't give you my life story or whatever. Jesus man don't mod if it makes you unhappy to update.",
    "^1.20": "Alright glad I just removed the integration and pushed my update today without it. Maybe I'll get around to using it when you aren't so rude. Fuck me for wanting to use your mod and not knowing if you were working on it since you had no 1.20 branch or anything. Man I even made this not a bug so it wouldn't fuck up metrics. And I said please and thanks, and didn't give you my life story or whatever. Jesus man don't mod if it makes you unhappy to update."
}
MACROS = {
    "website": "Modern Modpacks website: https://modernmodpacks.site",
    "avaritia": """# There exists like a billion different versions of avaritia for different versions of minecraft.
If you're confused about which one to use, here's a list of them with their respective versions:

* 1.7.10 - https://www.curseforge.com/minecraft/mc-mods/avaritia
* 1.12.2/1.18.2 - https://www.curseforge.com/minecraft/mc-mods/avaritia-1-10
* 1.16.5 - https://www.curseforge.com/minecraft/mc-mods/avaritia-endless
* 1.19(.0)/1.20 - https://www.curseforge.com/minecraft/mc-mods/avaritia-reforged

* Bad MCreator version (1.16.5, 1.17.1, 1.19.x) - https://www.curseforge.com/minecraft/mc-mods/avaritia-lite""",
    "optifine": """# When you ask for help, we automatically assume that you don't have OptiFine installed.
## Why?

Well, for starters, **OptiFine breaks a lot of mods**. It was designed for vanilla, and you would know that if you ever had to download a compatability mod between forge/fabric and OF.
Second, **OptiFine is closed source**, which isn't bad by itself, a lot of your favorite mods (for example, thaumcraft) are closed source as well. But since OF is a performance mod, it heavily relies on compatability, and if the mod is closed-source only the creator of said mod can implement that compatability, which means it will probably be very long before all of your mods are supported.
And finally, even with all of these factors OptiFine would've still been usable, **but it is developed by only one person**. And if it couldn't get worse, that person **has said multiple times that they do not consider compatability the first priority**.

OptiFine is "fine" (pun not intended) when used with older versions, because the older versions themselves had less content and thus are better optimized ||(and you don't really have any good alternatives for 1.12/1.7)||. But from 1.16 onwards, OF isn't something you should use.
Instead, check out these **open-source** alternatives: <https://github.com/TheUsefulLists/UsefulMods>! The main ones we recommend are: Rubidium for optimization (https://legacy.curseforge.com/minecraft/mc-mods/rubidium) and Oculus for shaders (https://legacy.curseforge.com/minecraft/mc-mods/oculus).

https://media.discordapp.net/attachments/758096127982829659/802983225126813706/OptiDumpsterFire.gif""",
    "hellish": "Hellish Mods is a subsidiary organization of Modern Modpacks focusing on making 1.16.5 mods, check them out here: https://legacy.curseforge.com/members/HellishMods/projects",
    "ports": "We **do not** offer ports for Fabric/Quilt/1.19.x/1.18.2/1.12.2/1.20/1.7.10/Beta 1.7.3/LiteLoader/Risugami/Rift/rd-132211/Secret Friday Update #2/Whatever unless we decide that we need to. The only version we will support is Forge 1.16.5. Please **do not** ask for ports on our GitHub, Discord, Reddit, Youtube and everywhere else.",
    "rules": "**Please** read the rules in <#1025316810490384424> before posting. You are probably getting this message as a warning, so action **won’t be taken against you**, but **please** follow the rules next time.",
    "wiki": "**Modern Modpacks & Hellish Mods have a documentation/wiki.** Link: https://wiki.modernmodpacks.site",
    "kofi": "If you want to support us monetarily, you can do it on your ko-fi: https://ko-fi.com/modernmodpacks. Note: you **will not** get anything in return.",
    "mpd": "Some Modern Modpacks devlogs are being posted on the Minecraft Pack Development server instead: https://discord.gg/R4tBduGsne",
    "mmc": "The worse MM: https://discord.gg/moddedmc",
    "gtb": "Official GregTech: Beyond discord server - https://discord.gg/sG6NZ7NaeC",
    "mm": "MM stands for Modern Modpacks, not Modded Minecraft, not Masterful Machinery, Modern Modpacks. Please for the love of god stop using that abbreviation incorrectly ||(or I will personally come into your house and shove a 1000MM ruler up your ass)||.",

    "tryandsee": "https://tryitands.ee/",
    "bruhmonkey": "https://www.youtube.com/watch?v=5oJgXrPuKGs",
    "yipee": "https://www.youtube.com/watch?v=Qu7KFMn54Bk",

    "info": "@website",
    "mods": "@hellish",
    "hellishmods": "@hellish",
    "docs": "@wiki",
    "donate": "@kofi",
    "support": "@kofi",
    "devlogs": "@mpd",
    "theworsemm": "@mmc",
    "notmm": "@mmc",
    "beyond": "@gtb",
    "abbreviations": "@mm",
    "monkeybruh": "@bruhmonkey",
    "bruh": "@bruhmonkey"
}
CHANNELS = {
    "memes": 1096717238553292882,
    "translators": 1133844392495554560
}
GUILD_OBJECT = discord.Object(1025316079226064966)

statusi = 0

async def get_guild() -> discord.Guild: return await client.fetch_guild(GUILD_OBJECT.id)
def get_data_json() -> dict: 
    if not path.exists("data.json"):
        with open("data.json", "w+") as f: f.write("{}")
    return load(open("data.json"))
def dump_data_json(data:dict): 
    with open("data.json", "w") as f: dump(data, f)
def add_user_to_data(data:dict, user:discord.User) -> dict:
    if str(user.id) not in data.keys(): data[str(user.id)] = {
        "pings": []
    }
    return data

@client.event
async def on_ready():
    # await tree.sync(guild=None)
    if len(argv)>1 and argv[1]=="--sync": await tree.sync(guild=GUILD_OBJECT)

    client.loop.create_task(server.run_task(port=9999))
    Popen(("cloudflared", "tunnel", "run", "github_webhook"), stderr=DEVNULL)

    await client.change_presence(status=discord.Status.online)
    update_status.start()
    # check_reminds.start()

    print(f"Logged in as: {client.user}")
@client.event
async def on_disconnect():
    await client.change_presence(status=discord.Status.offline)
@client.event
async def on_message(message:discord.Message):
    if message.author.bot: return

    for k, v in RESPONSES.items():
        keyword = k.removeprefix("^")
        matchh = search(r"\b"+keyword+r"\b", message.content, IGNORECASE)

        if matchh and f":{keyword}:" not in message.content.lower():
            if not k.startswith("^") or message.channel.id==CHANNELS["memes"]: 
                if not v.startswith("$"): await message.reply(f"> {matchh[0]}\n\n{v}", mention_author=False)
                else: await message.reply(stickers=[i for i in (await (await get_guild()).fetch_stickers()) if i.name==v.removeprefix("$")], mention_author=False)

    data = get_data_json()
    for k, v in data.items():
        for i in v["pings"]:
            if search(r"\b"+i+r"\b", message.content, IGNORECASE): 
                await (await client.fetch_user(k)).send(f"You got pinged because you have \"{i}\" as a word that you get pinged at. Message link: {message.jump_url}")
                break

@tasks.loop(seconds=5)
async def update_status():
    global statusi

    screen = 5
    status = "🟥🟧🟨🟩🟦🟪⬛⬜🟫"

    statusstring = status[-(screen-1):]+status
    await client.change_presence(activity=discord.Activity(name=statusstring[statusi:statusi+screen], type=discord.ActivityType.watching))
   
    if statusi+screen<len(statusstring): statusi += 1
    else: statusi = 0
# @tasks.loop(seconds=5)
# async def check_reminds():
#     data = get_data_json()

#     for k, v in data.items():
#         for i in v["reminds"]:
#             if i["time"]<time(): 
#                 await (await client.fetch_user(k)).send("Reminder! "+("Reason: "+i["reason"]+". " if i["reason"] else "")+(await (await client.fetch_channel(i["channel"])).fetch_message(i["message"])).jump_url)
#                 data[k]["reminds"].remove([j for j in data[k]["reminds"] if j["time"]==i["time"]][0])
#                 dump_data_json(data)

@server.after_serving
async def shutdown(): 
    await on_disconnect()
    _exit(0)

@tree.command(name="macro", description="Sends a quick macro message to the chat", guild=GUILD_OBJECT)
@app_commands.choices(name=[app_commands.Choice(name=i[:24], value=i) for i in MACROS.keys()])
async def macro(interaction:interactions.Interaction, name:app_commands.Choice[str]):
    text = MACROS[name.value]
    if not text.startswith("@"): await interaction.response.send_message(content=text)
    else: await interaction.response.send_message(content=MACROS[text.removeprefix("@")])

# @tree.command(name="remindme", description="Pings you after a certain period of time", guild=GUILD_OBJECT)
# @app_commands.describe(period="A period of time, written in a \"{time}(s/m/h/d)\" format")
# @app_commands.describe(reason="A optional reason for the reminder")
# async def remindme(interaction:interactions.Interaction, period:str, reason:str=""):
#     if not period[:-1].isnumeric() or period[-1] not in ("s", "m", "h", "d"): 
#         await interaction.response.send_message(content="Wrong period format: `"+period+"`", ephemeral=True)
#         return

#     data = get_data_json()
#     data = add_user_to_data(data, interaction.user)

#     remindtime = 0
#     if period.endswith("s"): remindtime = time()+int(period.removesuffix("s"))
#     elif period.endswith("m"): remindtime = time()+(60*int(period.removesuffix("m")))
#     elif period.endswith("h"): remindtime = time()+(3600*int(period.removesuffix("h")))
#     elif period.endswith("d"): remindtime = time()+(86400*int(period.removesuffix("d")))

#     if reason: message = await interaction.response.send_message(content=f"Successfully added a reminder for `{period}` with reason `{reason}`!")
#     else: message = await interaction.response.send_message(content=f"Successfully added a reminder for `{period}`!")

#     data[str(interaction.user.id)]["reminds"].append({
#         "time": remindtime,
#         "reason": reason,
#         "channel": interaction.channel.id,
#         "message": message.message.id,
#     })

#     dump_data_json(data)

@tree.command(name="pings", description="Set your string pings", guild=GUILD_OBJECT)
@app_commands.describe(pings="Words that will ping you, comma seperated, case insensitive.")
async def editpings(interaction:interactions.Interaction, pings:str):
    data = get_data_json()
    data = add_user_to_data(data, interaction.user)
    data[str(interaction.user.id)]["pings"] = [i.lower() for i in pings.replace(", ", ",").split(",")]
    dump_data_json(data)

    await interaction.response.send_message(content="Pings set! Your new pings are: `"+",".join(data[str(interaction.user.id)]["pings"])+"`.", ephemeral=True)

@server.post("/translators")
async def on_translator_webhook():
    data = loads(await request.get_data())
    commit = data["head_commit"]
    changed_files = [i for i in commit["added"]+commit["modified"] if i.endswith("en_us.json")]

    if changed_files:
        url = data["repository"]["url"]
        blob = f"{url}/blob/{data['repository']['default_branch']}"

        transbed = discord.Embed(color=discord.Color.purple(), title="Lang file changed!", url=url)
        transbed.description = "Changed files:\n\n"+"\n".join([f"[{i}]({blob}/{i})" for i in changed_files])
        transbed.set_thumbnail(url=blob+"/src/main/resources/pack.png?raw=true")
        transbed.set_footer(text="Changed mod: "+data["repository"]["name"].replace("-", " ").title())

        translators = await (await get_guild()).fetch_channel(CHANNELS["translators"])
        await translators.send(content="<@&1126286016781762680>", embed=transbed)

    return "OK"

try: client.run("MTEzMzc3OTEyMzA3NzEyODI1NQ.GOyT0M.9N5ZZaPx20ie4OY2fW40o0xfLwFRb4sqNLHikM")
except KeyboardInterrupt: pass