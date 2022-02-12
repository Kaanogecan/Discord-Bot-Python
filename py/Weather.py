from attr import field
from Cache import Cache
import feedparser

from Embed import Embed, EmbedField

class Weather:
    def __init__(self):
        self.weatherCache = Cache("", 600)  # 600 second = 10 minutes
        
    def GetWeather(self):
        weatherCache = self.weatherCache.GetValue()
        if weatherCache == "":
            parse = feedparser.parse("http://rss.accuweather.com/rss/liveweather_rss.asp?metric=1&locCode=EUR|TR|54300|ISTANBUL|")
            parse = parse["entries"][0]["summary"]
            weatherImg = parse.split('src="')[1]
            weatherImg = weatherImg[:-4]
            parse = parse.split()
            value = parse[4] + parse[5] + " " + parse[7] + " "
            field =  EmbedField(parse[2],value)
            fields = []
            fields.append(field)
            embed = Embed("Weather"," ",weatherImg,True,fields)
            embed = embed.GetEmbed()
            self.weatherCache.SetValue(embed)
            return self.weatherCache.GetValue()
        else:
            return weatherCache 