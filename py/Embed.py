import discord
class Embed:
    def __init__(self,title="",description="",imageUrl="",imgIsThumb= False,embedFields="",color = 0x71368A):
        self.Title =title
        self.Description = description
        self.Image = imageUrl
        self.EmbedFiels = embedFields
        self.Color = color
        self.ImgIsThumb=imgIsThumb
        
    def GetEmbed(self):
        embedVar = discord.Embed(title=self.Title, description=self.Description, color=self.Color)
        if self.Image != "":
            if self.ImgIsThumb:
                embedVar.set_thumbnail(url=self.Image)
            else:
                embedVar.set_image(url=self.Image)
        for field in self.EmbedFiels:
            embedVar.add_field(name=field.Name, value=field.Value,inline=field.Inline)
        return embedVar

    def GetHelpEmbed(self,prefix):
        helpEmbed = discord.Embed(title="Commands", description="", color=0x71368A)
        helpEmbed.add_field(name=prefix + "hi", value="Say Hi", inline=False)
        helpEmbed.add_field(
            name=prefix + "weather", value="Weather info for Istanbul", inline=False
        )
        helpEmbed.add_field(
            name=prefix + "where", value="Show on google maps", inline=False
        )
        helpEmbed.add_field(
            name=prefix + "wallpaper", value="Random Wallpaper", inline=False
        )
        helpEmbed.add_field(
            name=prefix + "hdwallpaper", value="Random HD Wallpaper", inline=False
        )
        helpEmbed.add_field(
            name=prefix + "deleteMessage",
            value=prefix + "deleteMessage [number]",
            inline=False,
        )
        helpEmbed.add_field(name=prefix + "say", value="say [your text]", inline=False)
        helpEmbed.add_field(name=prefix + "play", value="play music", inline=False)
        helpEmbed.add_field(
            name=prefix + "leave", value="Kosmarobot leave channel", inline=False
        )

class EmbedField:
    def __init__(self,name="",value="",inline=False):
        self.Name = name
        self.Value = value
        self.Inline = inline