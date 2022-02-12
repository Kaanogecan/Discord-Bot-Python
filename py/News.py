from Cache import Cache
from GoogleNews import GoogleNews

from Embed import Embed, EmbedField

class News:
    def __init__(self):
        self.newsCache = Cache("", 600)  # 600 second = 10 minutes
        
    def GetNews(self):
        newsCache = self.newsCache.GetValue()
        if newsCache == "":
            googleNews = GoogleNews(period="2d", lang="tr")  # set lang
            googleNews.search("TR")  # search key
            result = googleNews.result(sort=True)
            fields = []
            for x in result:
                field = EmbedField(x["title"],x["desc"] + "\n" + x["date"] + "\n" + x["link"])
                fields.append(field)
            newsEmbed = Embed("News",embedFields=fields).GetEmbed()
            self.newsCache.SetValue(newsEmbed)
            return newsEmbed
        else:
            return newsCache
         
    