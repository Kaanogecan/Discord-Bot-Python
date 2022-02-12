import random
class Wallpaper:
    def __init__(self):
        self.wallpaperRead = open("./txt/wallpaper.txt", "r")
        self.wallpaper = self.wallpaperRead.readlines()
        self.wallpaperHdRead = open("./txt/wallpaperhd.txt", "r")
        self.wallpaperHd = self.wallpaperHdRead.readlines()
    def GetHdWallpaper(self):
        return self.wallpaperHd[random.randrange(0, len(self.wallpaperHd))]
    def GetWallpaper(self):
        return self.wallpaper[random.randrange(0, len(self.wallpaper))]