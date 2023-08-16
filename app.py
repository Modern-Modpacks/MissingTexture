# Read the following as a haiku:
#
# This code is so bad
# But it works surprisingly
# So no touchy touch

from warnings import filterwarnings 
filterwarnings("ignore")

import discord
from discord import app_commands, interactions
from discord.ext import tasks
from asyncio import sleep
from re import search, IGNORECASE
from sys import argv
from os import _exit, path
from time import time
from json import loads, load, dump
from hashlib import md5
from logging import getLogger
from subprocess import Popen, DEVNULL
from quart import Quart, request
from thefuzz import process
from requests import get
from httpx import AsyncClient
from urllib import error, parse
from pubchempy import get_compounds, get_substances, Compound, Substance, BadRequestError

client = discord.Client(intents=discord.Intents.all())
http = AsyncClient()
tree = app_commands.CommandTree(client)
server = Quart(__name__)
getLogger("werkzeug").disabled = True

RESPONSES = {
    "1025316079226064966": {
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
    },
    "1099658057010651176": {}
}
MACROS = {
    "1025316079226064966": {
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
[Instead, check out these **open-source** alternatives](<https://github.com/TheUsefulLists/UsefulMods>)! The main ones we recommend are: [Rubidium](https://legacy.curseforge.com/minecraft/mc-mods/rubidium) for optimization and [Oculus](https://legacy.curseforge.com/minecraft/mc-mods/oculus) for shaders. [⠀](https://media.discordapp.net/attachments/758096127982829659/802983225126813706/OptiDumpsterFire.gif)""",
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
        "of": "@optifine",
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
    },
    "1099658057010651176": {}
}
CHANNELS = {
    "mm": {
        "memes": 1096717238553292882,
        "translators": 1133844392495554560,
        "member-general": 1027127053008515092,
        "modlogs": 1118925292589830236,
    }
}
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
GUILDS = (
    discord.Object(1025316079226064966), # MM
    discord.Object(1099658057010651176) # GTB
)

statusi = None

async def get_mm_guild() -> discord.Guild: return await client.fetch_guild(GUILDS[0].id)
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
    if len(argv)>1 and argv[1]=="--sync":
        for guild in GUILDS:
            if client.get_guild(guild.id)==None: continue
            tree.copy_global_to(guild=guild)
            await tree.sync(guild=guild)

    client.loop.create_task(server.run_task(port=9999))
    Popen(("cloudflared", "tunnel", "run", "github_webhook"), stderr=DEVNULL)

    await client.change_presence(status=discord.Status.online)
    update_status.start()

    print(f"Logged in as: {client.user}")
@client.event
async def on_disconnect():
    await client.change_presence(status=discord.Status.offline)
@client.event
async def on_message(message:discord.Message):
    if message.author.bot: return

    for name, value in RESPONSES[str(message.guild.id)].items():
        keyword1 = name.removeprefix("^")
        keyword = name.removeprefix("%")
        matchh = search(r"\b"+keyword+r"\b", message.content, IGNORECASE)

        if matchh and f":{keyword}:" not in message.content.lower():
            if (not name.startswith("^") or message.channel.id==CHANNELS["mm"]["memes"]) or (name.startswith("%") and message.channel.id in (CHANNELS["mm"]["memes"], CHANNELS["mm"]["member-general"])):
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
                else: await message.reply(stickers=[i for i in (await message.guild.fetch_stickers()) if i.name == value.removeprefix("$")], mention_author=False)

    data = get_data_json()
    for name, value in data.items():
        for i in value["pings"]:
            if search(r"\b"+i+r"\b", message.content, IGNORECASE) and str(message.author.id)!=name: 
                await (await client.fetch_user(name)).send(f"You got pinged because you have \"{i}\" as a word that you get pinged at. Message link: {message.jump_url}")
                break
@tree.error
async def on_error(interaction: interactions.Interaction, err: discord.app_commands.AppCommandError):
    errorbed = discord.Embed(color=discord.Color.red(), title="I AM SHITTING MYSELF!1!1", description=f"""Details:
```{err}```
Channel: <#{interaction.channel.id}>
User: <@{interaction.user.id}>
Time: <t:{round(interaction.created_at.timestamp())}:f>""")
    originalcommand = f"{interaction.command.name} "+" ".join([i["name"]+":"+i["value"] for i in interaction.data["options"]])
    errorbed.set_footer(text=f"The command that caused the error: \"/{originalcommand}\"")
    await (await client.fetch_channel(CHANNELS["mm"]["modlogs"])).send(embed=errorbed)

    errmsg = "Whoops, something has gone wrong! This incident was already reported to mods, they will get on fixing it shortly!"
    if interaction.response.is_done(): await interaction.followup.send(content=errmsg, ephemeral=True)
    else: await interaction.response.send_message(content=errmsg, ephemeral=True)

@tasks.loop(seconds=5)
async def update_status():
    global statusi

    screen = 7
    status = "🟥🟧🟨🟩🟦🟪⬛⬜🟫"

    if statusi==None: statusi = screen-1

    statusstring = status[-(screen-1):]+status
    await client.change_presence(activity=discord.Activity(state=statusstring[statusi:statusi+screen], name="Why the fuck do I have to define this it doesn't even show up", type=discord.ActivityType.custom))
   
    if statusi+screen<len(statusstring): statusi += 1
    else: statusi = 0

@server.after_serving
async def shutdown(): 
    await on_disconnect()
    http.aclose()
    _exit(0)

async def macro_name_autocomplete(interaction: interactions.Interaction, current:str) -> list:
    choices = list(MACROS[str(interaction.guild.id)].keys())
    choices.append("list")
    return [app_commands.Choice(name=i, value=i) for i in ([v for v, s in process.extract(current, choices, limit=10) if s>60] if current else choices[:25])]

@tree.command(name="macro", description="Sends a quick macro message to the chat")
@app_commands.autocomplete(name=macro_name_autocomplete)
async def macro(interaction:interactions.Interaction, name:str):
    localmacros = MACROS[str(interaction.guild.id)]
    if name=="list":
        if localmacros: await interaction.response.send_message(content=" | ".join(localmacros.keys()), ephemeral=True)
        else: await interaction.response.send_message(content="No macros found!", ephemeral=True)
        return
    if name not in localmacros.keys():
        await interaction.response.send_message(content="Unknown macro: `"+name+"`", ephemeral=True)
        return

    text = localmacros[name]

    if not text.startswith("@"): await interaction.response.send_message(content=text)
    else: await interaction.response.send_message(content=localmacros[text.removeprefix("@")])

@tree.command(name="chemsearch", description="Searches for a chemical compound based on the query.")
@app_commands.describe(query="Compound/Substance name or PubChem CID/SID", type="Search for Compounds/Substances. Optional, \"Compound\" by default", bettersearch="Enables better search feature, which might take longer. Optional, false by default")
@app_commands.choices(type=[app_commands.Choice(name=i, value=i) for i in ("Compound", "Substance")])
async def chemsearch(interaction:interactions.Interaction, query:str, type:str="compound", bettersearch:bool=False):
    await interaction.response.defer()

    type = type.lower()
    typeindex = 0 if type.lower()=="compound" else 1
    results = None
    pubchemerr = None

    while results==None:
        try: 
            if query.isnumeric(): 
                try: results = [(Compound.from_cid(int(query)) if typeindex==0 else Substance.from_sid(int(query)))]
                except BadRequestError: results = []
            else: 
                if typeindex==0: results = get_compounds(query, "name")
                else: results = get_substances(query, "name")
        except error.URLError: 
            if pubchemerr==None: pubchemerr = await interaction.channel.send("It looks like pubchem is down, please wait a few minutes for it to go back online.")
            await sleep(5)
            continue

    if len(results)<1: 
        await interaction.followup.send(content="Whoops, molecule not found!")
        return

    if bettersearch:
        namedict = {(await http.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/{type}/{i.cid if typeindex==0 else i.sid}/JSON")).json()["Record"]["RecordTitle"]: i for i in results}
        result : (Compound if typeindex==0 else Substance) = namedict[process.extract(query, namedict.keys(), limit=1)[0][0]]
    else: result = results[0]
    
    id = result.cid if typeindex==0 else result.sid
    info = (await http.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/{type}/{id}/JSON")).json()["Record"]

    def find_wikipedia_url(inf) -> str:
        names = [i for i in inf["Section"] if i["TOCHeading"]=="Names and Identifiers"]
        if len(names)<1: return
        names = names[0]

        other = [i for i in names["Section"] if i["TOCHeading"]=="Other Identifiers"]
        if len(other)<1: return
        other = other[0]

        wikipedia = [i for i in other["Section"] if i["TOCHeading"]=="Wikipedia"]
        if len(wikipedia)<1: return
        wikipedia = wikipedia[0]["Information"][0]["URL"]

        return wikipedia
    def has_3d_conformer(inf) -> bool:
        structures = [i for i in inf["Section"] if i["TOCHeading"]=="Structures"]
        if len(structures)<1: return False
        structures = structures[0]

        conformer = [i for i in structures["Section"] if i["TOCHeading"]=="3D Conformer"]
        if len(conformer)<1: return False
        conformer = conformer[0]

        return True

    wikipedia_url = find_wikipedia_url(info) if typeindex==0 else f"https://en.m.wikipedia.org/wiki/{parse.quote(info['RecordTitle']).lower()}"
    wikiinfo = None
    if wikipedia_url!=None:
        wikiinfo = get(wikipedia_url.replace("/wiki/", "/api/rest_v1/page/summary/"))
        wikiinfo = wikiinfo.json() if wikiinfo.status_code!=404 else None

    if typeindex==0:
        formula = result.molecular_formula
        for k, v in SUBSCRIPT.items(): formula = formula.replace(k, v)

    chembed = discord.Embed(color=discord.Color.green(), title=info["RecordTitle"].title(), description="", url=f"https://pubchem.ncbi.nlm.nih.gov/{type}/{id}")
    chembed.set_footer(text=f"Info provided by PubChem. {type[0].upper()}ID: {id}")
    if typeindex==0: chembed.description += f"**Formula**: {formula}\n**Weight**: {result.molecular_weight}"
    if typeindex==0 and result.iupac_name!=None: chembed.description += f"\n**IUPAC Name**: {result.iupac_name}"
    if has_3d_conformer(info): chembed.description += f"\n**3D Conformer**: [Link](https://pubchem.ncbi.nlm.nih.gov/{type}/{id}#section=3D-Conformer&fullscreen=true)"
    if wikipedia_url!=None and wikiinfo!=None: chembed.description += f"\n\n[**From the wikipedia article**:]({wikipedia_url})\n{wikiinfo['extract']}"
    chembed.set_thumbnail(url=f"https://pubchem.ncbi.nlm.nih.gov/image/imgsrv.fcgi?{type[0]}id={id}&t=l")

    if pubchemerr!=None: await pubchemerr.delete()
    await interaction.followup.send(embed=chembed)

@tree.command(name = "pings", description = "Set your string pings")
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

        translators = await (await get_mm_guild()).fetch_channel(CHANNELS["mm"]["translators"])
        await translators.send(content="<@&1126286016781762680>", embed=transbed)

    return "OK"

try: client.run("MTEzMzc3OTEyMzA3NzEyODI1NQ.GOyT0M.9N5ZZaPx20ie4OY2fW40o0xfLwFRb4sqNLHikM")
except KeyboardInterrupt: pass
