from email.policy import default
from time import time
from Embed import Embed,EmbedField
import youtube_dl
from youtube_search import YoutubeSearch
import discord

class Song:
    def __init__(self, id=0, songName="",img="", time="",addedBy="",statusChangedby="", status=""):
        self.AddedBy =addedBy
        self.Id = id
        self.SongName = songName
        self.Time = time
        self.Status = status
        self.Image = img
        self.StatusChangedby = statusChangedby
        self.statusMsg = ["Playing", "Paused", "Stoped"]
        self.emojis = ["▶️", "⏸️", "⏹️", "⏭️"]

    def ConvertEmbed(self):
        embedField = EmbedField(self.Time,self.Status+(" \nstatus changed by: "+self.StatusChangedby if self.StatusChangedby!= "" else ""))
        embed = Embed(self.SongName,"Added by: "+self.AddedBy,self.Image,False,[embedField])
        embed = embed.GetEmbed()
        return embed

    #0 => play 1 => resume 2=> stop
    async def ChangeStatus(self,user,voice,reaction):
        status = -1
        try:
            status = self.emojis.index(reaction.emoji)
        except:
            pass
        if status != -1:
            if voice.is_playing:
                if status == self.statusMsg.index("Playing"):
                    voice.resume()
                    self.Status = self.statusMsg[0]
                    self.StatusChangedby = user
                    editEmbed = self.ConvertEmbed()
                    editEmbed.color = 0x71368A
                    return editEmbed
                if status == self.statusMsg.index("Paused"):
                    voice.pause()
                    self.Status = self.statusMsg[1]
                    self.StatusChangedby = user
                    editEmbed = self.ConvertEmbed()
                    editEmbed.color = 0xE74C3C
                    return editEmbed
            if status == self.statusMsg.index("Stoped"):
                try:
                    self.Status = self.statusMsg[2]
                    self.StatusChangedby = user
                    editEmbed = self.ConvertEmbed()
                    editEmbed.color = 0x95A5A6
                    await voice.disconnect()
                    return editEmbed
                except:
                    pass
        else:
            return self.ConvertEmbed()
    
    async def Play(self,message,client):
        link = message.content[6:]
        if "youtube.com" not in message.content.lower() or "youtu.be" not in message.content.lower():
            results = YoutubeSearch(message.content[6:], max_results=1).to_dict()
            link ="youtube.com"+ results[0]["url_suffix"]
        # definitely add queuing system
        await message.channel.purge()
        try:
            voiceChannel = message.author.voice.channel
        except:
            await message.channel.send("odaya gir")
        await self.Leave()
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
        for emoji in self.emojis:
            await messageEmbed.add_reaction(emoji)
    
    async def Leave():
        pass
