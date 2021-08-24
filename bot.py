# encoding:utf-8

import discord
import json
import os
import asyncio
import datetime
import time
import platform
import email.message
import smtplib
from discord.ext import commands
from firebase import firebase

intents = discord.Intents.all()

Check_Dic = {}
bot = commands.Bot(command_prefix = "*", help_command = None, intents = intents)
counter_up = 0
counter_re = 0
error_time = 0
start = time.time()

with open("data.json", "r") as jfile:
    data = json.load(jfile)
        
auth = firebase.FirebaseAuthentication(data["KEY"], "sencha930511@gmail.com")
firebase.authentication = auth
user = auth.get_user()
firebase = firebase.FirebaseApplication("https://aoveditor.firebaseio.com/", authentication = auth)
 

async def interval():
    await bot.wait_until_ready()
    channel = bot.get_channel(745287933828792351)
    message = await channel.fetch_message(745324978248876112)
    while not bot.is_closed():
        global counter_up
        now_time_up = int(datetime.datetime.now().strftime("%M"))
        if now_time_up % 10 == 0 and counter_up == 0:
            capheny_check = firebase.get("/skin_ctrl/app", "CaCanUse")
            florentino_check = firebase.get("/skin_ctrl/app", "FloCanUse")
            official_check = firebase.get("/skin_ctrl/app", "OfficialCanUse")
            herosound_check = firebase.get("/sound_ctrl/app", "hero")
            lobbysound_check = firebase.get("/sound_ctrl/app", "lobby")
            text_check = firebase.get("/textcheck/app", "TextUpdate")
            telannas_check = firebase.get("/skin1/app", "btnCanUse")
            notice_check = firebase.get("/announcement/app", "display")
            map_check = firebase.get("map_ctrl/app", "Cherry")


            Check_Dic["capheny"] = capheny_check
            Check_Dic["florentino"] = florentino_check
            Check_Dic["official"] = official_check
            Check_Dic["herosound"] = herosound_check
            Check_Dic["lobbysound"] = lobbysound_check
            Check_Dic["text"] = text_check
            Check_Dic["telannas"] = telannas_check
            Check_Dic["notice"] = notice_check
            Check_Dic["map"] = map_check

            for key in Check_Dic.keys():
                if Check_Dic[key] == "true":
                    Check_Dic[key] = "運作中 :white_check_mark:"
                elif Check_Dic[key] == "false":
                    Check_Dic[key] = "關閉中 :x:"
            time = datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S")  
            app_message = f"--------------------------------------------\n【大廳音樂】\n{ Check_Dic['lobbysound'] }\n\n【角色語音】\n{ Check_Dic['herosound'] }\n\n【櫻花地圖】\n{ Check_Dic['map'] }\n\n【官方造型】\n{ Check_Dic['official'] }\n\n【卡芬妮自製造型】\n{ Check_Dic['capheny'] }\n\n【弗洛倫自製造型】\n{ Check_Dic['florentino'] }\n\n【特爾安娜絲自製造型】\n{ Check_Dic['telannas'] }\n\n【文字修改功能】\n{ Check_Dic['text'] }\n\n【公告】\n{ Check_Dic['notice'] }\n\n\n:white_check_mark: 正常運作\
    \n\n:x: 關閉維修/暫停使用\n\n最後更新時間：{ time }\n--------------------------------------------\n"
            await message.edit(content = app_message)
            print(f"【自動】{ time } 已更新狀態")
            counter_up = 1
        if now_time_up % 10 != 0:
            counter_up = 0
        await asyncio.sleep(10) #單位:sec

bg_task = bot.loop.create_task(interval()) 


async def botReport():
    await bot.wait_until_ready()
    while not bot.is_closed():
        global counter_re
        now_time_re = datetime.datetime.now().strftime("%H:%M")
        usage = firebase.get("/count/app", "UsageCounter")
        if now_time_re == "20:00" and counter_re == 0:
            end1 = time.time()
            second1 = end1 - start
            minute1 = int(second1 / 60)
            second1 = round(second1 - (minute1 * 60))
            hour1 = int(minute1 / 60)
            minute1 = minute1 - (hour1 * 60)
            day1 = int(hour1 / 24)
            hour1 = hour1 - (day1 * 24)
            sys1 = platform.platform()
            proce1 = platform.processor()
            time1 = datetime.datetime.now().strftime("%Y/%m/%d - %H:%M:%S")  
            boot1 = datetime.datetime.fromtimestamp(start).strftime("%Y-%m-%d %H:%M:%S")
            if second1 < 10:
                second_str1 = f"0{ second1 }"
            else:
                second_str1 = second1
            if minute1 < 10:
                minute_str1 = f"0{ minute1 }"
            else:
                minute_str1 = minute1
            if hour1 < 10:
                hour_str1 = f"0{ hour1 }"
            else:
                hour_str1 = hour1
            msg = email.message.EmailMessage()
            msg["From"] = "ChaBot - Discord<chabot.discord@gmail.com>"
            msg["To"] = "sencha930511+discordBot@gmail.com"
            msg["Subject"] = "[ChaBot - Discord] Bot's Daily Report"
            msg.add_alternative(f"<font color = #FF0000><h3>Your Discord Bot(ChaBot)'s Daily Report <font color = #9F35FF>{ time1 }</font></h3></font>Now running on : <font color = #0066CC>{ sys1 }</font><br>The computer processor : <font color = #0066CC>{ proce1 }</font><br>Last boot time of the bot : <font color = #0066CC>{ boot1 }</font><br>Online time of the bot : <font color = #0066CC>{ day1 }day(s), { hour_str1 }:{ minute_str1 }:{ second_str1 }</font><br>App usage : <font color = #0066CC>{ usage } time(s)</font><br><br>Vistit <a href = https://dashboard.heroku.com/apps/chabot930511/logs><font color = #02C874>Heroku</font></a> to get more information.<br><br>Thanks,<br>The ChaBot Team", subtype = "html")
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # 設定
            server.login("ChaBot.Discord@gmail.com", "Cha930511")
            server.send_message(msg)
            server.close()
            counter_re = 1
            print(f"【自動】{ time1 } 已傳送每日回報")
        if now_time_re != "20:00":
            counter_re = 0
        await asyncio.sleep(10)

report_timer = bot.loop.create_task(botReport())

'''
async def new_year():
    await bot.wait_until_ready()
    while not bot.is_closed():
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        if now_time == "23:59:54" or now_time == "23:59:55" or now_time == "23:59:56":
            for guild in bot.guilds:
                embed = discord.Embed(color = 0x6688f0)
                embed.add_field(name = "5", value = guild.default_role, inline = False)
                embed.set_image(url = "https://i.pinimg.com/originals/c2/73/9f/c2739fe9cd755c8a33eb25d92e6106a1.gif")
                await guild.system_channel.send(embed = embed)
            await asyncio.sleep(0.2)
            for guild in bot.guilds:
                embed = discord.Embed(color = 0x66f0bb)
                embed.add_field(name = "4", value = guild.default_role, inline = False)
                embed.set_image(url = "https://media3.giphy.com/media/d1E1szXDsHUs3WvK/giphy.gif")
                await guild.system_channel.send(embed = embed)
            await asyncio.sleep(0.2)
            for guild in bot.guilds:
                embed = discord.Embed(color = 0xeef066)
                embed.add_field(name = "3", value = guild.default_role, inline = False)
                embed.set_image(url = "https://i.pinimg.com/originals/5d/7c/c3/5d7cc314a06862b21765decac8654b35.gif")
                await guild.system_channel.send(embed = embed)
            await asyncio.sleep(0.2)
            for guild in bot.guilds:
                embed = discord.Embed(color = 0xf066e0)
                embed.add_field(name = "2", value = guild.default_role, inline = False)
                embed.set_image(url = "https://media0.giphy.com/media/26gsqQxPQXHBiBEUU/giphy.gif?cid=ecf05e47066eae31a6d0e0daa4f9acf3556373d79d0a2950&rid=giphy.gif")
                await guild.system_channel.send(embed = embed)
            await asyncio.sleep(0.2)
            for guild in bot.guilds:
                embed = discord.Embed(color = 0xf0606a)
                embed.add_field(name = "1", value = guild.default_role, inline = False)
                embed.set_image(url = "https://i.pinimg.com/originals/fc/ca/fa/fccafa6ce178ac8c1499abff6483a131.gif")
                await guild.system_channel.send(embed = embed)
            await asyncio.sleep(0.2)
            for guild in bot.guilds:
                embed = discord.Embed(color = 0x7860f0)
                embed.add_field(name = "Happy New Year! 2021!", value = guild.default_role, inline = False)
                embed.set_image(url = "https://media1.giphy.com/media/3o6fJcIM6mG3Ad6lAk/giphy.gif")
                await guild.system_channel.send(embed = embed)
        else:
            await asyncio.sleep(1)
    
new_year_timer = bot.loop.create_task(new_year())
''' 
           

@bot.event
async def on_ready():
    activity = discord.Game(name = "*help | Developed by SenCha 🍵")
    #activity = discord.Game(name = "*help | Happy New Year! 🎆")
    await bot.change_presence(activity = activity)
    print(">> Bot is online <<")


@bot.event
async def on_command_error(ctx, error):
        global error_time
        error_time = error_time + 1
        return error_time


@bot.command()
async def status(ctx):
    global error_time
    end = time.time()
    second = end - start
    minute = int(second / 60)
    second = round(second - (minute * 60))
    hour = int(minute / 60)
    minute = minute - (hour * 60)
    day = int(hour / 24)
    hour = hour - (day * 24)
    ping = round(bot.latency*1000)
    sys = platform.platform()
    proce = platform.processor()
    boot = datetime.datetime.fromtimestamp(start).strftime("%Y/%m/%d - %H:%M:%S")
    if second < 10:
        second_str = f"0{ second }"
    else:
        second_str = second
    if minute < 10:
        minute_str = f"0{ minute }"
    else:
        minute_str = minute
    if hour < 10:
        hour_str = f"0{ hour }"
    else:
        hour_str = hour
    embed = discord.Embed(title = "ChaBot Status", description = f"Running On `{ sys }`", color = 0x15c2e0, timestamp = datetime.datetime.utcfromtimestamp(end))
    embed.add_field(name = ":desktop: Processor", value = f"`{ proce }`" , inline = False)
    embed.add_field(name = ":tea: Latency", value = f"`{ ping } ms` / `{ ping / 1000 } s`", inline = False)
    embed.add_field(name = ":zap: Error Trigger", value = f"`{ error_time } time(s)`", inline = False)
    embed.add_field(name = ":alarm_clock: Boot Time", value = f"`{ boot }`", inline = True)
    embed.add_field(name = ":timer: Online Time", value = f"`{ day } day(s), { hour_str }:{ minute_str }:{ second_str }`", inline = True)
    await ctx.send(embed = embed)        


for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        bot.load_extension(f"cmds.{ filename[:-3] }")


if __name__ == "__main__":    
    bot.run(data["token"])
