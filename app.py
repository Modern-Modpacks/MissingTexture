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
    "^rainbuu": "🛌",
    "^eyesquared": """@eyesquared  :capitalist:
you fucking homeless piece of fucking crap thats looking for attention online just because your parents apparently did not cared about your unformed ass, your edgy 14 year old behavior is nothing but being an asshole 
not even pointing out your mentall illnesses aka the pronouns that you collected like your dad collected HIV at your age
everyone has prefrences and if you touch thoose you are nothing more than an literal asshole""",
    "^eyecubed": """@eyesquared  :capitalist:
you fucking homeless piece of fucking crap thats looking for attention online just because your parents apparently did not cared about your unformed ass, your edgy 14 year old behavior is nothing but being an asshole 
not even pointing out your mentall illnesses aka the pronouns that you collected like your dad collected HIV at your age
everyone has prefrences and if you touch thoose you are nothing more than an literal asshole""",

    "^rftools": "RFTools is a mod by Vazkii",
    "^greg": "STOP POSTING ABOUT GREGTECH, I'M TIRED OF SEEING IT! My friends on reddit send me memes, on discord it's fucking memes - I was in a subreddit, right? and ALLLLLLLLL of the POSTS are just GregTech stuff. I- I showed my Champion underwear to my girlfriend, and the logo I flipped it and I said, \"Hey babe: When the underwear greg :joy: :joy: :joy:\"",
    "%5 stages of grief": "<:blunder:1119338458335416422>",
    "^mekanism": "ALL THE FUCKING SONS OF MEKANISM, WHO CRAWLED OUT WITH THEIR CUT IN HALF BRAIN CELLS INTO THE TERRITORY OF A REAL TECH MOD, and I don't care about the fact that it's oversimplified in many aspects, this doesn't stop you, dickheads, from doing an absolute fuckery and claiming tier statuses, for which you'll need fucking 20 more hours or so of making infra of that tier. ALL BRAINLESS MONKEYS, WHO CAN'T EVEN READ TWO LINES OF TEXT OR CHECK THE FUCKING JEI, ASKING THEIR STUPID, 5-SECOND WORTH OF RESEARCH, QUESTIONS IN CHAT. AND ALL THE OTHER DEGENERATES, WHO CAME TO THIS CHAT JUST TO LOWER THE AVERAGE IQ OF ALREADY SUFFERING IN THAT REGARD CHAT. With this message I adress my hatred for you. You are the species of the very bottom of the GT community... Well fuck, not even GT community, even representatives of RLCraft, SevTech, SF4 and other garbage, don't have such a low IQ. And this isn't even my elitism, which I have to account for, every time I irresistibly want to make a hole in a wall using someone's head. Every single word in this message was thought out magnitudes better than your average thinking process while shitposting in this chat. You are mental impotents. You are incapable of a mere reading of the information that was thought out FOR and INSTEAD OF YOU. Not to mention tasks that really require planning (base design, math). You are braindeads, who are stuck in state of stagnation. I won't dare to judge anyone for not knowing something, but unwillingness to learn yourself and urge to ask every 2 minutes disgusts me, especially considering all the convinces nomi provides, including NEI or manual, which may not explain EVERYTHING but it explains exactly enough to figure out the rest yourself easily. At the times of my \"first modpack\" there was nothing besides atrocious wikis and English forums, for which I didn't have an access at least because I didn't know English. You don't respect the work of devs. Who the fuck did they do all the hard work for? I get it that the main point of the pack is to make GT more accessible and be a great \"first\" modpack from this category - the way the quest book is written proves that. It tells you a lot of basic concepts, from which you can deduce more complex things, and these complex things even explained on the server already through the %t commands. Your ignorance for all of that makes me feel nothing but pure Spanish shame for devs. Nomifactory didn't deserve this kind of community sharing one braincell between everyone. Maybe it was a mistake making a GT modpack for beginners, knowing the modded Minecraft community and knowing what kind of idiots it has. No negative towards devs or chat members who know how to gameign. Answers to incoming questions: Yes, I'm an elitist, seasoned one even, but i'm accounting for that and i'm going easy on you all. My elitism takes only a small role in what i find disgusting about you all, because you need to NEVER open the modpack and don't even know about it to fuck up as much as y'all do. Yes, I'm rather toxic, because how wouldn't you be toxic to people who'll never understand any other language? I would've NEVER been toxic if I saw at least SOME progress, and not the same thing repeated every minute. Yes, I'm a bit biased towards the nomi playerbase, but there wouldn't be any bias if the average IQ at least on the official server would've been at least a few points higher. No, I don't feel any shame or remorse for my words. There shouldn't be any remorse for someone who talks to you in a straight forward way and who's honest to everyone, including themselves. Thanks for everyone's attention, especially people who got affected by this message. Fuck you.",

    "^1.18": "Alright glad I just removed the integration and pushed my update today without it. Maybe I'll get around to using it when you aren't so rude. Fuck me for wanting to use your mod and not knowing if you were working on it since you had no 1.18 branch or anything. Man I even made this not a bug so it wouldn't fuck up metrics. And I said please and thanks, and didn't give you my life story or whatever. Jesus man don't mod if it makes you unhappy to update.",
    "^1.19": "Alright glad I just removed the integration and pushed my update today without it. Maybe I'll get around to using it when you aren't so rude. Fuck me for wanting to use your mod and not knowing if you were working on it since you had no 1.19 branch or anything. Man I even made this not a bug so it wouldn't fuck up metrics. And I said please and thanks, and didn't give you my life story or whatever. Jesus man don't mod if it makes you unhappy to update.",
    "^1.20": "Alright glad I just removed the integration and pushed my update today without it. Maybe I'll get around to using it when you aren't so rude. Fuck me for wanting to use your mod and not knowing if you were working on it since you had no 1.20 branch or anything. Man I even made this not a bug so it wouldn't fuck up metrics. And I said please and thanks, and didn't give you my life story or whatever. Jesus man don't mod if it makes you unhappy to update.",

    "^quanpack": "$hop on quanpack"
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
    "translators": 1133844392495554560,
    "member-general": 1027127053008515092
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

    for name, value in RESPONSES.items():
        keyword1 = name.removeprefix("^")
        keyword = name.removeprefix("%")
        matchh = search(r"\b"+keyword+r"\b", message.content, IGNORECASE)

        if matchh and f":{keyword}:" not in message.content.lower():
            if (not name.startswith("^") or message.channel.id==CHANNELS["memes"]) or (name.startswith("%") and message.channel.id in (CHANNELS["memes"], CHANNELS["member-general"])):
                if not value.startswith("$"): 
                    value = f"> {matchh[0]}\n\n{value}"
                    if len(value)>2000:
                        chunks = []
                        chunk = ""
                        chunklength = 0

                        for i, word in enumerate(value.split(" ")):
                            print(f"pre {chunklength}")
                            chunklength += len(word)
                            if chunklength>=1500 or i==len(value.split(" "))-1:
                                if i==len(value.split(" "))-1: chunk += " "+word
                                chunks.append(chunk)
                                chunk = word
                                chunklength = len(word)
                            else: chunk += " "+word

                        await message.reply(chunks[0], mention_author=False)
                        for c in chunks[1:]:
                            await message.channel.send(c)
                    else: await message.reply(value, mention_author=False)
                else: await message.reply(stickers=[i for i in (await (await get_guild()).fetch_stickers()) if i.name == value.removeprefix("$")], mention_author=False)
                

    data = get_data_json()
    for name, value in data.items():
        for i in value["pings"]:
            if search(r"\b"+i+r"\b", message.content, IGNORECASE) and str(message.author.id)!=name: 
                await (await client.fetch_user(name)).send(f"You got pinged because you have \"{i}\" as a word that you get pinged at. Message link: {message.jump_url}")
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
@app_commands.describe(name="Name of the macro, type /macro list to see all of them.")
async def macro(interaction:interactions.Interaction, name:str):
    name = name.lower()

    if name=="list":
        await interaction.response.send_message(content=" | ".join(MACROS.keys()), ephemeral=True)
        return
    if name not in MACROS.keys():
        await interaction.response.send_message(content="Unknown macro: `"+name+"`", ephemeral=True)
        return

    text = MACROS[name]

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

@tree.command(name = "pings", description = "Set your string pings", guild=GUILD_OBJECT)
@app_commands.describe(pings = "Words that will ping you, comma seperated, case insensitive.")
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

        transbed = discord.Embed(color = discord.Color.purple(), title = "Lang file(s) changed!", url=url)
        transbed.description = "Changed files:\n\n"+"\n".join([f"[{i}]({blob}/{i})" for i in changed_files])
        transbed.set_thumbnail(url = blob + "/src/main/resources/pack.png?raw=true")
        transbed.set_footer(text = "Changed mod: "+data["repository"]["name"].replace("-", " ").title())

        translators = await (await get_guild()).fetch_channel(CHANNELS["translators"])
        await translators.send(content="<@&1126286016781762680>", embed=transbed)

    return "OK"

try: client.run("MTEzMzc3OTEyMzA3NzEyODI1NQ.GOyT0M.9N5ZZaPx20ie4OY2fW40o0xfLwFRb4sqNLHikM")
except KeyboardInterrupt: pass
