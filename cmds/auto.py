import discord
import asyncio
import json
import datetime
import time
import requests
from discord.ext import commands, tasks
from core.classes import Cog_Extension

#status = ["*help | Developed by SenCha 🍵", "Made With Love :video_game:"]

class Auto(Cog_Extension):
    def __init__(self, *args, **kwargs):    
        super().__init__(*args, **kwargs)
        self.checkVideo.start()
        self.subCount.start()
        #self.changePresence.start()

    @tasks.loop(minutes = 5)
    async def checkVideo(self):
            await self.bot.wait_until_ready()
            try:
                channel = self.bot.get_channel(629623137071267844)
                requests.urllib3.disable_warnings()
                url = "https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId=UUK5dwhwK-NoJypN0SBvIZsA&key=AIzaSyCSMJWJYLxkbyD_CjPvpG76UqQlBhtPCd4"
                jFile = requests.get(url = url, verify = False).json()
                videoID = jFile["items"][0]["contentDetails"]["videoId"]
                with open("./data.json", "r") as jfile:
                    data = json.load(jfile)
                    if data["videoID"] != videoID:
                        await channel.send(f"@everyone 您的新影片已抵達，請簽收 \nhttps://youtu.be/{videoID}")
                        print("【自動】已傳送影片更新通知")
                        data["videoID"] = videoID
                        with open("./data.json", "w") as jwrite:
                            json.dump(data, jwrite)  
            except Exception as e:
                print(f"【錯誤】<auto - checkVideo> {e}")

    @tasks.loop(minutes = 5)
    async def subCount(self):
            await self.bot.wait_until_ready()
            try:
                channel = self.bot.get_channel(870178147813965864)
                requests.urllib3.disable_warnings()
                url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=UCK5dwhwK-NoJypN0SBvIZsA&key=AIzaSyCSMJWJYLxkbyD_CjPvpG76UqQlBhtPCd4"
                jFile = requests.get(url = url, verify = False).json()
                sub = jFile["items"][0]["statistics"]["subscriberCount"]
                await channel.edit(name = f"🎊煎茶訂閱：{sub}")
            except Exception as e:
                print(f"【錯誤】<auto - subCount> {e}")

'''
    @tasks.loop(seconds=5)
    async def changePresence(self):     
        global status
        activity = discord.Game(name = next(status))
        await self.bot.change_presence(activity = activity)
'''      

def setup(bot):
    bot.add_cog(Auto(bot))

