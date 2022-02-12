import discord
import datetime
from gtts import gTTS
from Song import Song
from News import News
from Weather import Weather
from Wallpaper import Wallpaper
import youtube_dl
from youtube_search import YoutubeSearch

from Embed import Embed
# Wallpaper, Weather, News init
news = News()
weather = Weather()
wallpaper = Wallpaper()
#Dc 
client = discord.Client()
prefix = "$"

#Play Song
currentSong = Song()

def FigletLoginScr():
    print("-" * 100)
    figletRead = open("./txt/figlet.txt", "r")
    for i in figletRead:
        print(i[0:41])
    print("-" * 100)

@client.event
async def on_ready():
    FigletLoginScr()
    print("We have logged in as {0.user} ".format(client))
    await client.change_presence(
        activity=discord.Game(
            prefix + "message" + " logged in time: " + str(datetime.datetime.now())
        )
    )

@client.event
async def on_reaction_add(reaction, user): 
    reactedMessageId = reaction.message.id
    if reactedMessageId == currentSong.Id and not user.bot: # current plaing song's embed reaction
        await reaction.remove(user)
        voice = discord.utils.get(client.voice_clients, guild=reaction.message.guild)
        edittedEmbed = await currentSong.ChangeStatus(user.display_name,voice,reaction)
        await reaction.message.edit(embed=edittedEmbed)
 

@client.event
async def on_message(message):
    print(
        str(datetime.datetime.now())
        + "=> "
        + str(message.author)
        + "=> "
        + str(message.channel)
        + " channel: "
        + message.content
    )

    async def Leave():
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        try:
            await voice.disconnect()
        except:
            pass

    async def Play(music):
        await Leave()
        try:
            voiceChannel = message.author.voice.channel
            await voiceChannel.connect()
            voice = discord.utils.get(client.voice_clients, guild=message.guild)
            voice.play(discord.FFmpegPCMAudio(music))
        except:
            await message.channel.send("error")

    if message.author == client.user:
        return

    if message.content.startswith(prefix + "hi"):
        await message.channel.send(
            "hi " + (str(message.author).split("#"))[0] + " :wave: How r u ?"
        )

    if message.content.startswith(prefix + "deleteMessage"):
        count = int(message.content[len("deleteMessage"):])
        await message.channel.purge(limit=count)

    if message.content.startswith(prefix + "play") or message.channel.id == "channel id":
        link = message.content[6:]
        if "youtube.com" not in message.content.lower() or "youtu.be" not in message.content.lower():
            results = YoutubeSearch(message.content[6:], max_results=1).to_dict()
            link ="www.youtube.com"+ results[0]["url_suffix"]
        # definitely add queuing system
        await message.channel.purge()
        try:
            voiceChannel = message.author.voice.channel
        except:
            await message.channel.send("odaya gir")
        await Leave()
        await voiceChannel.connect()
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            URL = info["formats"][0]["url"]
        voice = discord.utils.get(client.voice_clients, guild=message.guild)
        songName = info["title"]
        img = info["thumbnails"][-1]["url"]
        minute = str(int(info["duration"] / 60))
        second = str(info["duration"] % 60)
        if len(minute) == 1:
            minute = "0" + minute
        if len(second) == 1:
            second = "0" + second

        global currentSong
        currentSong = Song(0,songName,img,(minute + ":" + second),(str(message.author).split("#"))[0],"","Loading...")
        messageEmbed = await message.channel.send(embed=currentSong.ConvertEmbed())
        currentSong.Id = messageEmbed.id
        currentSong.Status = Song().statusMsg[0]
        ffmpeg_options = {"options": "-vn"}
        args = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
        voice.play(discord.FFmpegPCMAudio(URL, before_options=args, **ffmpeg_options))
        await messageEmbed.edit(embed=currentSong.ConvertEmbed())
        for emoji in currentSong.emojis:
            await messageEmbed.add_reaction(emoji)

    if message.content.startswith(prefix + "help"):
        embedHelp = Embed().GetHelpEmbed(prefix)
        await message.channel.send(embed=embedHelp)

    if message.content.startswith(prefix + "leave"):
        await Leave()

    if message.content.startswith(prefix + "weather"):
        await message.channel.send(embed=weather.GetWeather())

    if message.content.startswith(prefix + "where"):
        url = (
            "https://www.google.nl/maps/place/"
            + message.content[7:].replace(" ", "+")
            + "/&amp"
        )
        await message.channel.send(url)

    if message.content.startswith(prefix + "say"):
        msg = message.content[5:]
        tts = gTTS(text=msg, lang="en")
        try:
            tts.save("audio.mp3")
            await Play("audio.mp3")
        except:
            tts.save("audio1.mp3")
            await Play("audio1.mp3")

    if message.content.startswith(prefix + "wallpaper"):
        await message.channel.send(wallpaper.GetWallpaper())

    if message.content.startswith(prefix + "hdwallpaper"):
        await message.channel.send(wallpaper.GetHdWallpaper())

    if message.content.startswith(prefix + "news"):
        await message.channel.send(embed=news.GetNews())


client.run("token")

# kuyruk mantığı