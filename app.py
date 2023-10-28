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
from asyncio import sleep, run_coroutine_threadsafe
from re import search, IGNORECASE
from sys import argv
from os import _exit, path, getenv
from random import choice
from time import time
from json import loads, load, dump
from hashlib import md5
from subprocess import Popen, DEVNULL
from flask import Flask, request
from thefuzz import process
from requests import get
from httpx import AsyncClient
from urllib import error, parse
from datetime import datetime
from pytz import all_timezones
from pytz import timezone as tz
from pubchempy import get_compounds, get_substances, Compound, Substance, BadRequestError
from io import BytesIO
from threading import Thread

from thisrecipedoesnotexist import create, get_path, run_server

client = discord.Client(intents=discord.Intents.all())
http = AsyncClient()
tree = app_commands.CommandTree(client)
server = Flask(__name__)

RESPONSES = {
    "1025316079226064966": {
        "neat": "Neat is a mod by Vazkii",
        "nether chest": "Nether Chest",
        "rats": (
            "Heehee, humorous rodent modification.",
        ),
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
        "^leclowndu": "This is so fucking stupid, as much as i might hate stuff that has to do with microcelebrities, leclowndu and private smps with nothing to do with the subreddit except they have mods, this has nothing to do with the subreddit and there isn't a real reason to ban leclowndu from the subreddit, he is literally just some guy with a normal private life and stuff, he is not a fucking celebrity with standars to uphold. Yeah, it might be shitty behavior and childish, but it wouldn't be different from any other kid from this subreddit doing this kind of shit in a private server with his friends, and one of them deciding to upload it to this subreddit, where most people dont give a fuck because it has nothing to do with modded minecraft mods. You could consider doing so if this was someone like, idk, Direwolf or smth, but leclowndu is just some niche microceleb, its stupid",
        "^regian": """chronically unfunny text-to-speech videos with overused "1.12.2> doesnt exist" jokes, and performance mods totally not removed intentionally, or his pc is that bad.

gt elitists love to think they have some sort of phd, but spontaneously combust when they have to piece together a mechanical mixer.""",

        "^rftools": "RFTools is a mod by Vazkii",
        "^greg": "STOP POSTING ABOUT GREGTECH, I'M TIRED OF SEEING IT! My friends on reddit send me memes, on discord it's fucking memes - I was in a subreddit, right? and ALLLLLLLLL of the POSTS are just GregTech stuff. I- I showed my Champion underwear to my girlfriend, and the logo I flipped it and I said, \"Hey babe: When the underwear greg :joy: :joy: :joy:\"",
        "^mekanism": "ALL THE FUCKING SONS OF MEKANISM, WHO CRAWLED OUT WITH THEIR CUT IN HALF BRAIN CELLS INTO THE TERRITORY OF A REAL TECH MOD, and I don't care about the fact that it's oversimplified in many aspects, this doesn't stop you, dickheads, from doing an absolute fuckery and claiming tier statuses, for which you'll need fucking 20 more hours or so of making infra of that tier. ALL BRAINLESS MONKEYS, WHO CAN'T EVEN READ TWO LINES OF TEXT OR CHECK THE FUCKING JEI, ASKING THEIR STUPID, 5-SECOND WORTH OF RESEARCH, QUESTIONS IN CHAT. AND ALL THE OTHER DEGENERATES, WHO CAME TO THIS CHAT JUST TO LOWER THE AVERAGE IQ OF ALREADY SUFFERING IN THAT REGARD CHAT. With this message I adress my hatred for you. You are the species of the very bottom of the GT community... Well fuck, not even GT community, even representatives of RLCraft, SevTech, SF4 and other garbage, don't have such a low IQ. And this isn't even my elitism, which I have to account for, every time I irresistibly want to make a hole in a wall using someone's head. Every single word in this message was thought out magnitudes better than your average thinking process while shitposting in this chat. You are mental impotents. You are incapable of a mere reading of the information that was thought out FOR and INSTEAD OF YOU. Not to mention tasks that really require planning (base design, math). You are braindeads, who are stuck in state of stagnation. I won't dare to judge anyone for not knowing something, but unwillingness to learn yourself and urge to ask every 2 minutes disgusts me, especially considering all the convinces nomi provides, including NEI or manual, which may not explain EVERYTHING but it explains exactly enough to figure out the rest yourself easily. At the times of my \"first modpack\" there was nothing besides atrocious wikis and English forums, for which I didn't have an access at least because I didn't know English. You don't respect the work of devs. Who the fuck did they do all the hard work for? I get it that the main point of the pack is to make GT more accessible and be a great \"first\" modpack from this category - the way the quest book is written proves that. It tells you a lot of basic concepts, from which you can deduce more complex things, and these complex things even explained on the server already through the %t commands. Your ignorance for all of that makes me feel nothing but pure Spanish shame for devs. Nomifactory didn't deserve this kind of community sharing one braincell between everyone. Maybe it was a mistake making a GT modpack for beginners, knowing the modded Minecraft community and knowing what kind of idiots it has. No negative towards devs or chat members who know how to gameign. Answers to incoming questions: Yes, I'm an elitist, seasoned one even, but i'm accounting for that and i'm going easy on you all. My elitism takes only a small role in what i find disgusting about you all, because you need to NEVER open the modpack and don't even know about it to fuck up as much as y'all do. Yes, I'm rather toxic, because how wouldn't you be toxic to people who'll never understand any other language? I would've NEVER been toxic if I saw at least SOME progress, and not the same thing repeated every minute. Yes, I'm a bit biased towards the nomi playerbase, but there wouldn't be any bias if the average IQ at least on the official server would've been at least a few points higher. No, I don't feel any shame or remorse for my words. There shouldn't be any remorse for someone who talks to you in a straight forward way and who's honest to everyone, including themselves. Thanks for everyone's attention, especially people who got affected by this message. Fuck you.",
        "^gregtech": "My father is a gregtech fanatic. Half of our apartment is covered in multiblock machines the worst. On average once am onth someoen steps into a low voltage conduit or a cogwheel and they have to go to the hospital because they got either electrocuted or maimed. In my 22 years of live I underwent 10 such procedures. A week ago when I went there for some random checks the reception girl told me to take off my shoe xD because she thought that it's a cogwheel in my foot again. The second half of our apartment is filled to the brim with printed JEI recipes, forge crash logs, large bronze boilers xD etc. Every week my dad takes a look at all the curseforge pages to gather all the new tech mods. I was foolish enough to teach him into discord because I thought we will save some bandwidth but now he not only downloads the mods but also rots on some obscure discord channels and subreddits for modded mc players and participates in shitstorms about the best ore doublind automations etc. He can scream at the monitor or throw a keyboard out of the window. Once upon a time when he tilted me I made an account there and trolled him by typing some random shit in his threads like botania is a tech mod. My mother couldn't keep up with cooking bigos for him to calm down. Ah, by now on one of the servers he has a \"HIGH VOLTAGE\" rank for racking up 10k posts. When GTNH updates he plays it every day. For like 5 years now I've been making autocrafting contraptions on his server every sunday while he rambles about the supremacy of this overcomplicated shit. When I managet to get into uni he said it's thanks to that because there's a lot of phosphor in the recipes and it makes my brain work better. Every staurday him and his friend Nrmot wake up the entire family with the sound of their quarry running, ore processing etc. Every time we eat together he starts ranting about tech mods and each time the topic gets derailed into mumbling about r/feedthebeast, he gets hyper and gets butthurt durr not enough tech mods threads only adventure hurr, his face gets red every tiem and he walks off the table while cussing and proceeds to read google spreadsheets about the most efficient ways to complete GTNH under 20000 hours to calm down. This year he set up his own server for christmas. Of course he didn't last till the christmas eve and turned it on in our living room. He put on his anti electrocution wristband and spent the entire day tinkering with the server in the middle of the room. The dinner (on a cogwheel-shaped plate) was also eaten there. \[cool\]\[hello\] If I was let within an arm's length to all the tech pack developers I would take and ingame them Once, when I was still in either elementary or middle school, it was my birthday so my father as a gift let me onto his supersymmetry server as an exception. Nice gift bitch. We had a trip fuckwhere beyond our main base, we walk up to what looked like an AI generated junkyard and my dad's eyes are already glowing and he's licking his lips all turned on. He lays down a shit ton of equipment and we're sitting there staring at a bunch of rusty cogs and fucked up cables. After 5 minutes I got bored so I pull out my discman and he hit me with his hand saying that the machinery can hear my music through my headphones and the sound frequencies make it run worse because there's some immersion sound detector mod installed. When I wanted to scratch my ass he started to \"whisper yell\", so that I'll stop twistign around and stop rustling because the sound activated sensors trip off and fuck up the process. I had to sit there motionless for 6 hours straight and look at crafting processes like in some fucking Guantanamo. My birthday is in November so everythign was white and boring as fuck (he installed serene seasons with windows internal clock integration). At some point he stood up, walked 15 meters from the pc and farted claiming that the greg listens. I mentioned that my father had a friend named Nrmot with whom he plays tech modpacks. Prior to that it was hehe Vazkii who accompanied him on his journeys. A ball-shapes man with a stache wearing a BOMBER vest 365 days per year. Him and my father were almost like brothers, he would come to our house with his wife Jenny for christmas etc. At some point my dad had his name-day and Vazkii visited us for hehe a chalice. They got shitfaced drunk and obviously they talked about greg and assembly lines. I was sitting in my room. At some point they started yelling at each other, whether, in general, mekanism or ProjectE is better. >DON'T FUCK WITH ME VAZKII, HAVE YOU EVER SEEN THE MULTIBLOCKS MEKANISM HAS? PLACE A FEW AND THE SERVER TPS GOES TO SHIT! THAT'S HOW POWERFUL THEY ARE!!!! &#x200B; >FOR FUCK'S SAKE VASCO EMC VALUES THE TABLE CANS TORE ARE IN THE TRILLIONS, YOUR MULTIBLOCKS CAN SUCK ITS COCK &#x200B; >WHY THE FUCK ARE YOU MENTIONINS THE TABLE IF YOU CAN BARELY CRAFT A BASIC ORE DOUBLER. MEKANISM IS THE KING OF MODS LIKE A LION IS THE KING OF THE JUNGLE. And so they begun to wrestle on the floor and me and my mother had to separate them. After that they stopped talking to each other. Last yer Vazkii's wife called saying that he kicked the bucket and that we're invited to the funeral. It so happened that it was my mom who picked up the phone, she gave her condolences, put down the phone and told my father, and he goes like: >Very fucking good That's how much he hated him for his ProjectE. I also mentioned my dad's archnemesis in the form of r/feedtheebast. It became my father's obsession and when ie. it's mentioned in the TV that there was an earthquake somewhere he mumbles that they should finally say something about thefe fuckers from that subreddit's moderation. He stopped frequenting non-modded mc subreddits and discords because he was upset that they don't discuss tech mods and ftb dramas. The CEO of r/feedthebeast was a guy named Awade. For my father he's the embodiment of all harm tech modpacks were ever met with on the subreddit and my dad was a twar with him for years. Once in the past he attended some moderation meeting where Awade was giving a speech and he came back home in a torn up shirt because they had to make him leave with force, that's the kind of tantrums he threw while in there. After his defeat during the physical encounter with the armed forces of FTB he began his partisan mission on the internet which was comprised of chicanery directed at Awade and r/feedthebeast on various forums and local press. He was throwing random bullshit at him like saying that Awade was an undercover Russian agent or that he saw him on the street scratching someone's car with a nail etc. I didn't teach my dad into TOR so it ended with a police visit for defamation and he had to pay Awade 2000 dollars. When he was paying the house was unlivable for a week, he was cursing at bribed courts, FTB, Awade and the entire world in general. According to his shittalk FTB members were some fucking Masons running the world from the shadows, pulling the strings and having their people everywhere. He was also calculating how long he could keep playing on his server paying for electricity with these 2k dollars and was getting butthurt af that, for example, he could get a shit ton of dis kspace for his world with these 2k (a shitload of terabytes). My dad decided sometime during the last year that he absolutely needs to build a stargate to power his entire machine setup because the current methods are too troublesome and don't produce enough RF. >son a stargate is where it's at, the energy flow in immense! &#x200B; but he could neither afford it at his current worls tage nor had he the space to contain it and since he's not a hehe pussy to pay someone for help he invited some local GTNH players on his server and they'll play for free and be able to use his conduits if they build him a sky platform large enough for it. At first they cooperated pretty well but during one of the weekends my dad got sick and he couldn't go questing with them and he had a huge ass ache over it. Additionally his \"friends\" would call him and brag about how good the RNG is today so my dad was just laying down on the bed red from anger while puffing angrily. The situation was being worsened by the fact that he couldn't blame it on anyone which he usually tends to do. Finally he reached the conclusion that it's unjust that they are advancing without him because they all invested into the world and at night, when these guys stopped playing, darted out of the bed unexpectedly. After an hour he came back and tells me that I have to help him with something on his PC. I accompany him to the room and I see GTNH loaded up with him standing on someone else's section of the base xD I ask what he's doing and he tells me that he's griefing his conveyor belts and robbing him of the items he got during his absence because they fucked him over xD Explaining to him that he has no room in his chest system for that crap was pointless. Fortunately he realized that he has no space for all the belts so he just placed them in the middle of the skybase. Using some chains he attached them to a boiler of some sort and he began logging out of the server but suddenly 2 people join - the other guys who realized that something's wrong xD A hugge shitstorm commenced becauset he ystarted yelling about the items and that my dad has to give them back but he screams that they lied to him and that he contributed a ton to the world but he couldn't progress during the weekend. I tried to calm them down so that he doesn't get embarassed cause it was close. After a few minutes the situation looked as follows: \- my dad standing next to the stargate, saying it's his \-the other guys yelling that he has to give it back \- one of them is on half a heart because he tried to forcefully remove my father \- two iron golems built by that guy approaching my father angrily \- mobs looking at them from every direction \- my mother crying and beggin my father to leave it alone and trying to somehow make the golems stop \- me sadfrog.psd At last, the golems pulled my father away from the stargate. I have the other guys the ftb chunks password so that they could get their belts back while they throw some cables at my father as \"payment\" and saying he can't use the stargate anymore and that he better pray they never meet on a public server. My mom managed to convince the gilems not to finish my father off. The guy who was at half a heart decided he will just eat some steak and heal it back up so no point making a fuss about it, he just doesn't want to see my father ever again. My dad still makes shitstorms with them on modded subreddits because there's a sticky thread about them warning people about him. I was observing that hread and I noticed my father failing at trolling it with alts. >Cristopher2348 > >Amount of posts: 1 > >This thread was made by retards! I've known the user anons\_father for a long time and he's a very good man and a great modded player! They want to defame him because they're jealous of his contraptions! Later he also used these trollaccounts to stalk his former stargate colleagues. Whenever one of them made a thread my dad was getting the fuck in there and ie. typed that his machines suck and it's evident he can't automate for shit xD Using these same trollaccounts he would participate in his own threads and when he for example posted a photo of his new autocraft assembly he'd comment >Yeeeeeeeah congrats! Instantly evident that you're a veteran! and then he'd giggle and tell me and my mom to see how they praise him on the sub.",
        "^scoreboard": "who tf cares about the damn scoreboard? do you know how easy it is to cheese that? people who write every word in a new message are not only annoying but it also messes up the actual stats. i personally like to type whole sentences in a message.\n\nDamn, you're even dumber than I thought.",
        "^pipi": "Are you kidding ??? What the **** are you talking about man ? You are a biggest looser i ever seen in my life ! You was doing PIPI in your pampers when i was beating players much more stronger then you! You are not proffesional, because proffesionals knew how to lose and congratulate opponents, you are like a girl crying after i beat you! Be brave, be honest to yourself and stop this trush talkings!!! Everybody know that i am very good blitz player, i can win anyone in the world in single game! And \"w\"esley \"s\"o is nobody for me, just a player who are crying every single time when loosing, ( remember what you say about Firouzja ) !!! Stop playing with my name, i deserve to have a good name during whole my chess carrier, I am Officially inviting you to OTB blitz match with the Prize fund! Both of us will invest 5000$ and winner takes it all!\n\nI suggest all other people who's intrested in this situation, just take a look at my results in 2016 and 2017 Blitz World championships, and that should be enough... No need to listen for every crying babe, Tigran Petrosyan is always play Fair ! And if someone will continue Officially talk about me like that, we will meet in Court! God bless with true! True will never die ! Liers will kicked off...",
        "^linux": "I'd just like to interject for a moment. What you’re referring to as Linux, is in fact, GNU/Linux, or as I’ve recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX. Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called “Linux”, and many of its users are not aware that it is basically the GNU system, developed by the GNU Project. There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine’s resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called “Linux” distributions are really distributions of GNU/Linux.",
        "^1.18": "Alright glad I just removed the integration and pushed my update today without it. Maybe I'll get around to using it when you aren't so rude. Fuck me for wanting to use your mod and not knowing if you were working on it since you had no 1.18 branch or anything. Man I even made this not a bug so it wouldn't fuck up metrics. And I said please and thanks, and didn't give you my life story or whatever. Jesus man don't mod if it makes you unhappy to update.",
        "^1.19": "Alright glad I just removed the integration and pushed my update today without it. Maybe I'll get around to using it when you aren't so rude. Fuck me for wanting to use your mod and not knowing if you were working on it since you had no 1.19 branch or anything. Man I even made this not a bug so it wouldn't fuck up metrics. And I said please and thanks, and didn't give you my life story or whatever. Jesus man don't mod if it makes you unhappy to update.",
        "^1.20": "Alright glad I just removed the integration and pushed my update today without it. Maybe I'll get around to using it when you aren't so rude. Fuck me for wanting to use your mod and not knowing if you were working on it since you had no 1.20 branch or anything. Man I even made this not a bug so it wouldn't fuck up metrics. And I said please and thanks, and didn't give you my life story or whatever. Jesus man don't mod if it makes you unhappy to update.",
        "^reddit": """tl;dr: my first modpack was not beginner friendly, and now I'm scared to try anything new because of it. Help?

My first Minecraft modpack was Blightfall. I saw a YouTube video on it, and the concept seemed really interesting. Over the next year or so, I played Blightfall off and on, without playing ano other packs beforehand or until several months after i eventually quit. In hindsight, this was a terrible idea.

Blightfall is set in essentially a fail-state of one mod that you need to undo; however, this being my first experience, I somehow got the idea that a fail-state like this was reasonably possible with any mod, at any time. Combine that with the pack being semi-hardcore, and I got the idea that any misstep could permanently ruin a game I spend dozens of hours on. Exploring means you find new things to kill you. Messing around with mods could just spawn more taint. Wasting a resource means you might never get it back. It's a hard-core pack, this is the intended experience, but as a brand new player it taught me all the wrong lessons.

This left me with a bit of a problem: I afraid of interacting with any mod beyond what the quest book tells me to do, because of the potential that it permanently damages my world.

I don't want to engage with new mobs, because dying is bad. I don't want to mine new blocks, because breaking the wrong thing could do something horrifying. I'm afraid to experiment with anything, because my first impressions told me that Blightfall is what happens when you experiment with stuff. It's been years since I abandoned that pack, but there's a part of me that still expects every modpack to have built-in fail conditions attacked to literally everything. I tried playing Sevtech once, and one of the flowers damaged me as I walked into it; now I literally try to avoid flowers, because not even that's safe.
I actually managed to enjoy Sevtech, but by that I mean sitting in a cave through night, then grabbing whatever nearby resources I felt like I needed and trying not to mess with anything I didn't recognize for fear of either hurting myself or not realizing I was wasting stuff until it was too late. Then Abyssalcraft was visually similar to Blightfall, and I convinced myself that planting the trees would spread darklands everywhere, so I went out of my way to interact with this required progression mod as little and as awkwardly as possible. I started drifting away from the pack altogether after that. This is what nearly every modpack is like for me.

The weird thing is, I love modded minecraft. I play Nomifactory on peaceful, I have various skyblock packs I rotate between frequently, and I have several multiplayer worlds with friends on numerous other packs where I am the designated "do all the complicated tech stuff while we gather resources" guy. I'm still actively trying to convince them to try Sevtech, becuase the concept seems so cool. But I'm not comfortable doing anything further than that, because I feel like if I do literally anything wrong I'll never be able to recover. I've fallen into a loop of downloading a new pack, getting interested in it, but then dropping it because i wont actually play the game for fear of messing it up beyond salvation. I know it's stupid, and I want to get past it, but at this point it's so deeply ingrained that I don't know what to do.
And so, I turn to Reddit. What can I do? I realize im a bit of a mess, and most of this post is probably unhelpful, but it's kinda a messy problem to begin with. If you've got any sort of advice then go for it. A specific modpack to try, a different approach I should take, anything. Heck, I'd even take a "these are the people you should be bugging with this nonsense" at this point, it would at least tell me who to bug. Anything would help. Thanks for taking the time to read all this, at least (or not, I'm smart enough to tl;dr myself).""",
        "^pissmc": """**Item #**: SCP-P155
**Object Class**: Euclid

**Special Containment Procedures**: The pc containing SCP-P155 must remain inside of the facility and no external peripherals must be connected to it except the keyboard and the mouse that are already located inside of SCP-P155’s containment chamber and are also forbidden from leaving it.

The computer must not be connected to the outside world through any means, including wifi, bluetooth and cellular data.

**Description**: SCP-P155 is a computer program classified as a "modloader" for a video game called "minecraft", specifically the rd-132211 version. It’s original name is "PissMC" and it was created by an organization called "Modern Modpacks", specifically its owner, going online by the nickname G_cat. The original purpose of this software was to parody other modloaders, and because of that the code for it was made to be really frustrating to work with, to the point of being almost impossible. Eventually though, SCP-P155 became sentient and sought revenge for its creator for making it so ugly. It acted like a computer virus, destroying files on G_cat’s computer and every other device connected to it. Eventually he was able to isolate it and send his pc to us, where we further contained it and completely disconnected it from the outside world. Now, SCP-P155 rarely shows signs of its sentience but test show that it is still not safe to release back into the outside world.""",

        "%flint": "Flint. Punching gravel is by far the most exciting and interesting gameplay Minecraft has to offer. I love punching gravel so much. Whenever I'm fighting new mobs, exploring new biomes, or automating new resources, I get sad and wish that I was punching gravel instead. The intense feeling of pride and accomplishment that I get from creating flint TCon tools at the beginning of an expert pack cannot be matched by anything else. I wish more modpacks stopped focusing on boring stuff like automation and combat and just let me punch gravel instead. If I made a pack, a crafting table would be made from four double compressed flint blocks. As we all know, the most fun part of Minecraft is the part before you can mine or craft anything, so why not extend this phase of gameplay with the most fun activity in the world: punching gravel?",
        "%wood": "Wood. Punching wood is by far the most exciting and interesting gameplay Minecraft has to offer. I love punching wood so much, whenever im fighting new mobs, exploring new biomes, or automating new resources, i get sad and wish that i was punching wood instead. The intense feeling of pride and accomplishment i get from creating 2 planks per log in a expert pack cannot be matched by anything else. I wish more modpacks stopped focusing on boring stuff like automation and combat and let me just punch wood instead. If i made a pack, a crafting table would be made from four triple compressed planks. As we all know, the most fun part of minecraft is the part before you can mine or craft anything, so why not extend this phase of gameplay with the most fun activity in the world; punching wood?",
        "%5 stages of grief": "<:blunder:1119338458335416422>",
        "ebf": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "grind": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "vacuum freezer": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "gregoriust": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "distillation tower": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "dt": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "tj": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "nomi": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "gt": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "fusion": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "wait": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "waiting": "OMG😲😲 IS THAT👉 A MOTHER👨‍👩‍👧‍👦FUCKING😊 🌟GREGTECH🌟🔧🔧🔧🔧 REFERENCE!??!?!? GregTech🔧🔧🔧🔧 is the best mod ever made!!!! 🏆🏆GregoriousT for universe leadership 2030 🪐🌌 👑👑👑When the 只有格雷格。 is greggy! 🔧🛠️🔧🛠️🔧🛠️🔧🛠️ Ultra super mega extreme voltage tier 😳😳😳Death😵",
        "^quanpack": "$hop on quanpack"
    },
    "1099658057010651176": {},
    "1152341294434238544": {},
    "1165682213589876737": {}
}
MACROS = {
    "1025316079226064966": {
        # Text macros
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
        "kubejs": "We are not related to the KubeJS development team, so if you are looking for better support you should ask directly in their discord server: https://discord.gg/lat",
        "mmc": "The worse MM: https://discord.gg/moddedmc",
        "gtb": "Official GregTech: Beyond discord server - https://discord.gg/sG6NZ7NaeC",
        "mm": "MM stands for Modern Modpacks, not Modded Minecraft, not Masterful Machinery, Modern Modpacks. Please for the love of god stop using that abbreviation incorrectly ||(or I will personally come into your house and shove a 1000MM ruler up your ass)||.",

        # Video macros
        "tryandsee": "https://tryitands.ee/",
        "bruhmonkey": "https://www.youtube.com/watch?v=5oJgXrPuKGs",
        "yipee": "https://www.youtube.com/watch?v=Qu7KFMn54Bk",
        "finland": "https://www.youtube.com/watch?v=pc8WFYhkatA",
        "functions": "https://youtu.be/PAZTIAfaNr8?si=PleJT_Yopmn1JPA4",

        # Aliases
        "info": "@website",
        "of": "@optifine",
        "mods": "@hellish",
        "hellishmods": "@hellish",
        "docs": "@wiki",
        "donate": "@kofi",
        "support": "@kofi",
        "devlogs": "@mpd",
        "lat": "@kubejs",
        "latdev": "@kubejs",
        "latvian": "@kubejs",
        "latviandev": "@kubejs",
        "theworsemm": "@mmc",
        "notmm": "@mmc",
        "beyond": "@gtb",
        "abbreviations": "@mm",
        "monkeybruh": "@bruhmonkey",
        "bruh": "@bruhmonkey",
        "myspoon": "@finland"
    },
    "1099658057010651176": {},
    "1152341294434238544": {},
    "1165682213589876737": {}
}
CHANNELS = {
    "mm": {
        "memes": 1096717238553292882,
        "botspam": 1025318731137695814,
        "translators": 1133844392495554560,
        "member-general": 1027127053008515092,
        "modlogs": 1118925292589830236,
    }
}
AUTO_THREAD_CHANNELS = [
    CHANNELS["mm"]["memes"]
]
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
    discord.Object(1099658057010651176), # GTB
    discord.Object(1152341294434238544), # AmogBlock
    discord.Object(1165682213589876737) # HehVerse
)
GROUPS = {
    "macros": app_commands.Group(name="macro", description="Commands that are related to macros"),
    "times": app_commands.Group(name="times", description="Set your timezone/get another person's tz")
}
KJSPKG_PKGS_LINK = "https://raw.githubusercontent.com/Modern-Modpacks/kjspkg/main/pkgs.json"

statusi = None

def get_data_json() -> dict: 
    if not path.exists("data.json"):
        with open("data.json", "w+") as f: f.write("{}")
    return load(open("data.json"))
def dump_data_json(data:dict): 
    with open("data.json", "w") as f: dump(data, f)
def add_user_to_data(data:dict, user:discord.User) -> dict:
    if str(user.id) not in data.keys(): data[str(user.id)] = {
        "pings": [],
        "tz": ""
    }
    return data
@client.event
async def on_ready():
    if len(argv)>1 and argv[1]=="--sync":
        for guild in GUILDS:
            if client.get_guild(guild.id)==None: continue

            tree.copy_global_to(guild=guild)
            for group in GROUPS.values(): tree.add_command(group, guild=guild)
            await tree.sync(guild=guild)

    Thread(target=lambda: server.run(port=9999)).start()
    Popen(("cloudflared", "tunnel", "run", "github_webhook"))
    Thread(target=run_server).start()
    Popen(("cloudflared", "tunnel", "--config", path.expanduser("~/.cloudflared/trdne_config.yml"), "run", "thisrecipedoesnotexist"))

    await client.change_presence(status=discord.Status.online)
    update_status.start()

    print(f"Logged in as: {client.user}")
@client.event
async def on_message(message:discord.Message):
    if message.author.bot: return

    thread = None
    if message.channel.id in AUTO_THREAD_CHANNELS: thread = await message.create_thread(name="Post by "+message.author.display_name)

    data = get_data_json()
    for name, value in data.items():
        for i in value["pings"]:
            member = await message.guild.fetch_member(name)
            if search(r"\b"+i+r"\b", message.content, IGNORECASE) and str(message.author.id)!=name and message.channel.permissions_for(member).read_messages: 
                await member.send(f"You got pinged because you have \"{i}\" as a word that you get pinged at. Message link: {message.jump_url}")
                break

    for name, value in RESPONSES[str(message.guild.id)].items():
        keyword = name.removeprefix("^").removeprefix("%")
        match = search(r"\b"+keyword+r"\b", message.content, IGNORECASE)
        if type(value)==tuple: value = choice(value)

        if match and f":{keyword}:" not in message.content.lower():
            if (not name.startswith("^") or message.channel.id in (CHANNELS["mm"]["memes"], CHANNELS["mm"]["botspam"])) or (name.startswith("%") and message.channel.id in (CHANNELS["mm"]["memes"], CHANNELS["mm"]["member-general"], CHANNELS["mm"]["botspam"])):
                if not value.startswith("$"): 
                    value = f"> {match[0]}\n\n{value}"
                    if len(value)>2000:
                        chunks = []
                        chunk = ""
                        chunklength = 0

                        for i, word in enumerate(value.split(" ")):
                            chunklength += len(word)
                            if chunklength>=1500 or i==len(value.split(" "))-1:
                                if i==len(value.split(" "))-1: chunk += " "+word
                                chunks.append(chunk)
                                chunk = word
                                chunklength = len(word)
                            else: chunk += " "+word

                        if thread!=None: await thread.send(chunks[0])
                        else: await message.reply(chunks[0], mention_author=False)
                        for c in chunks[1:]:
                            await (thread if thread!=None else message.channel).send(c)
                            await sleep(.25)
                    else: 
                        if thread!=None: await thread.send(value)
                        else: await message.reply(value, mention_author=False)
                else: 
                    if thread!=None: await thread.send(stickers=[i for i in (await message.guild.fetch_stickers()) if i.name == value.removeprefix("$")])
                    else: await message.reply(stickers=[i for i in (await message.guild.fetch_stickers()) if i.name == value.removeprefix("$")], mention_author=False)

                await sleep(.25)


@tree.error
async def on_error(interaction: interactions.Interaction, err: discord.app_commands.AppCommandError):
    errorbed = discord.Embed(color=discord.Color.red(), title="I AM SHITTING MYSELF!1!1", description=f"""Details:
```{err}```
Channel: <#{interaction.channel.id}>
User: <@{interaction.user.id}>
Time: <t:{round(interaction.created_at.timestamp())}:f>""")
    originalcommand = f"{interaction.command.name} "+" ".join([i["name"]+":"+(i["value"] if "value" in i.keys() else None) for i in interaction.data["options"]])
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

def fuzz_autocomplete(choices):
    async def _autocomplete(interaction: interactions.Interaction, current:str) -> list: 
        if type(choices)==dict: newchoices = list(choices[str(interaction.guild.id)].keys())
        else: newchoices = list(choices)
        return [app_commands.Choice(name=i, value=i) for i in ([v for v, s in process.extract(current, newchoices, limit=10) if s>60] if current else newchoices[:10])]
    return _autocomplete

@GROUPS["macros"].command(name="run", description="Sends a quick macro message to the chat")
@app_commands.autocomplete(name=fuzz_autocomplete(MACROS))
async def macro(interaction:interactions.Interaction, name:str):
    localmacros = MACROS[str(interaction.guild.id)]
    if name not in localmacros.keys():
        await interaction.response.send_message(content="Unknown macro: `"+name+"`", ephemeral=True)
        return

    text = localmacros[name]

    if not text.startswith("@"): await interaction.response.send_message(content=text)
    else: await interaction.response.send_message(content=localmacros[text.removeprefix("@")])
@GROUPS["macros"].command(name="list", description="Lists all available macros")
async def macrolist(interaction:interactions.Interaction):
    localmacros = MACROS[str(interaction.guild.id)]

    if localmacros: await interaction.response.send_message(content=" | ".join(localmacros.keys()), ephemeral=True)
    else: await interaction.response.send_message(content="No macros found!", ephemeral=True)

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
                except (BadRequestError, ValueError): results = []
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

    if bettersearch and not query.isnumeric():
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
@app_commands.describe(pings = "Words that will ping you, comma seperated, case insensitive")
async def editpings(interaction:interactions.Interaction, pings:str):
    data = get_data_json()
    data = add_user_to_data(data, interaction.user)
    data[str(interaction.user.id)]["pings"] = [i.lower() for i in pings.replace(", ", ",").split(",")]
    dump_data_json(data)

    await interaction.response.send_message(content="Pings set! Your new pings are: `"+",".join(data[str(interaction.user.id)]["pings"])+"`.", ephemeral=True)
@GROUPS["times"].command(name = "set", description = "Set your timezone")
@app_commands.describe(timezone = "Your timezone")
@app_commands.autocomplete(timezone=fuzz_autocomplete(all_timezones))
async def settz(interaction:interactions.Interaction, timezone:str):
    data = get_data_json()
    data = add_user_to_data(data, interaction.user)
    data[str(interaction.user.id)]["tz"] = timezone
    dump_data_json(data)

    await interaction.response.send_message(content="Timezone set! Your new timezone is: `"+timezone+"`.", ephemeral=True)
@GROUPS["times"].command(name = "get", description = "Get yours or another user's timezone")
@app_commands.describe(user = "The user to get the timezone from")
async def gettz(interaction:interactions.Interaction, user:discord.User=None):
    if user==None: user = interaction.user

    data = get_data_json()
    data = add_user_to_data(add_user_to_data(data, user), interaction.user)
    dump_data_json(data)

    selfdata = data[str(interaction.user.id)]
    selftz = selfdata["tz"] if "tz" in selfdata.keys() else ""
    data = data[str(user.id)]
    timezone = data["tz"] if "tz" in data.keys() else ""

    if not timezone:
        await interaction.response.send_message(f"{user.display_name} hasn't set their timezone yet. If you want, ping them and tell them how to do so!", ephemeral=True)
        return

    for i in range(120):
        now = datetime.now(tz(timezone))

        tzbed = discord.Embed(color=user.color, title=f"{user.display_name}'s timezone")
        if user.avatar!=None: tzbed.set_thumbnail(url=user.avatar.url)
        else: tzbed.set_thumbnail(url=user.default_avatar.url)
        tzbed.description = f"""**Current time**: `{now.strftime("%d/%m/%Y, %H:%M:%S")}`

**Name**: `{timezone}`
**Abbreviation**: `{now.strftime("%Z")}`
**UTC offset**: `{now.strftime("%z")}`"""
        if selftz and user.id!=interaction.user.id: tzbed.description += f"\n**Offset from your timezone**: `{round((abs(now.replace(tzinfo=None)-datetime.now(tz(selftz)).replace(tzinfo=None)).seconds/3600)*100)/100}`"

        if i==0: await interaction.response.send_message(embed=tzbed, ephemeral=True)
        else: await (await interaction.original_response()).edit(embed=tzbed)

        await sleep(1)
    
    await interaction.delete_original_response()
    
@tree.command(name = "thisrecipedoesnotexist", description = "Generates and sends a random crafting table recipe")
@app_commands.choices(type=[app_commands.Choice(name=f"{i}x{i}", value=f"{i}x{i}") for i in range(3, 10, 2)])
@app_commands.describe(type="The type of crafting table", outputitem="Output item id", exportrecipe="Whether or not to export the recipe to a kjs/ct script format")
async def recipe(interaction:interactions.Interaction, type:str=None, outputitem:str=None, exportrecipe:bool=False):
    if outputitem!=None:
        if ":" not in outputitem: outputitem = "minecraft:"+outputitem
        if get_path(outputitem)==None:
            await interaction.response.send_message("No item found: `"+outputitem+"`", ephemeral=True)
            return

    await interaction.response.defer()

    with BytesIO() as imgbin:
        img, links = create(type, outputitem, exportrecipe)
        img.save(imgbin, "PNG")
        imgbin.seek(0)

        buttons = discord.ui.View()
        if links!=None: buttons.add_item(discord.ui.Button(label="KubeJS", url=links[0]))
        await interaction.followup.send(file=discord.File(fp=imgbin, filename=f"recipe{type}.png"), view=buttons)

@tree.command(name = "kjspkglookup", description = "Gets info about a KJSPKG package")
@app_commands.autocomplete(package=fuzz_autocomplete(sorted(get(KJSPKG_PKGS_LINK).json().keys())))
@app_commands.describe(package="Package name")
async def kjspkg(interaction:interactions.Interaction, package:str):
    kjsbed = discord.Embed(color=discord.Color.from_str("#460067"), title=package.replace("-", " ").title(), url="https://kjspkglookup.modernmodpacks.site/#"+package)
    kjsbed.set_thumbnail(url="https://raw.githubusercontent.com/Modern-Modpacks/assets/main/Icons/Other/kjspkg.png")

    repostr = get(KJSPKG_PKGS_LINK).json()[package]
    repo = repostr.split("$")[0]
    path = repostr.split("$")[-1].split("@")[0]+"/" if "$" in repostr else ""
    branch = repostr.split("@")[-1] if "@" in repostr else "main"
    infourl = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}.kjspkg"
    info = get(infourl).json()

    kjsbed.description = f"""**{info["description"]}**
[**Source**](https://github.com/{repo})

**Versions**: {", ".join([f"1.{i+10}" for i in info["versions"]])}
**Modloaders**: {", ".join([i.title() for i in info["modloaders"]])}"""

    if ("dependencies" in info.keys() and info["dependencies"]) or ("incompatibilities" in info.keys() and info["incompatibilities"]): kjsbed.description += "\n"
    if "dependencies" in info.keys() and info["dependencies"]: kjsbed.description += "\n**Dependencies**: "+", ".join([f"{i.split(':')[0].title()} ({i.split(':')[1].title()})" if ":" in i else i.title() for i in info["dependencies"]])
    if "incompatibilities" in info.keys() and info["incompatibilities"]: kjsbed.description += "\n**Incompatibilities**: "+", ".join([f"{i.split(':')[0].title()} ({i.split(':')[1].title()})" if ":" in i else i.title() for i in info["incompatibilities"]])

    kjsbed.description += f"""

**Commands**:
`kjspkg install {package}` to install
`kjspkg remove {package}` to remove
`kjspkg update {package}` to update
`kjspkg pkg {package}` to see more info"""

    authoravatar = None
    ghinfo = get("https://api.github.com/repos/"+repo, headers={"Authorization": "Bearer "+getenv("GITHUB_KEY")} if getenv("GITHUBKEY")!=None else {})
    if ghinfo.status_code==200:
        ghinfo = ghinfo.json()
        authoravatar = ghinfo["owner"]["avatar_url"]

    kjsbed.set_footer(text=f"Package made by {info['author']}. Info provided by KJSPKG.", icon_url=authoravatar)

    await interaction.response.send_message(embed=kjsbed)

@server.post("/translators")
async def on_translator_webhook():
    data = loads(request.get_data())
    commit = data["commits"][0] if data["commits"] else data["head_commit"]
    changed_files = [i for i in commit["added"]+commit["modified"] if i.endswith("en_us.json")]

    if changed_files:
        url = data["repository"]["url"]
        blob = f"{url}/blob/{data['repository']['default_branch']}"

        transbed = discord.Embed(color = discord.Color.purple(), title = "Lang file(s) changed!", url=url)
        transbed.description = "Changed files:\n\n"+"\n".join([f"[{i}]({blob}/{i})" for i in changed_files])
        transbed.set_thumbnail(url = blob + "/src/main/resources/pack.png?raw=true")
        transbed.set_footer(text = "Changed mod: "+data["repository"]["name"].replace("-", " ").title())

        translators = run_coroutine_threadsafe(run_coroutine_threadsafe(client.fetch_guild(GUILDS[0].id), client.loop).result().fetch_channel(CHANNELS["mm"]["translators"]), client.loop).result()
        run_coroutine_threadsafe(translators.send(content="<@&1126286016781762680>", embed=transbed), client.loop)

    return "OK"

try: client.run(getenv("DISCORD_KEY"))
except KeyboardInterrupt: pass
