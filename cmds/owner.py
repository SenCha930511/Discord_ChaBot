import discord
import asyncio
import os
from discord.ext import commands
from core.classes import Cog_Extension

class Owner(Cog_Extension):

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.bot.load_extension(f"cmds.{ extension }")
        await ctx.send(f"{ extension } 讀取完畢")
        print(f"【指令】{ extension } 讀取完畢")


    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        if extension == "owner":
            await ctx.send(f"無法退出 {extension}")
            print(f"【錯誤】無法退出 {extension}")
        else:
            self.bot.unload_extension(f"cmds.{ extension }")
            await ctx.send(f"{ extension } 退出完畢")
            print(f"【指令】{ extension } 退出完畢")


    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        if extension == "*":
            for filename in os.listdir('./cmds'):
                if filename.endswith('.py'):
                    self.bot.reload_extension(f'cmds.{filename[:-3]}')
                    await ctx.send(f"{filename[:-3]} 重新載入完畢")
            await ctx.send(f"已重新載入所有cogs")
            print(f"【指令】已重新載入所有cogs")
        else:
            self.bot.reload_extension(f"cmds.{ extension }")
            await ctx.send(f"{ extension } 重新載入完畢")
            print(f"【指令】{ extension } 重新載入完畢")
            
  
    @commands.command()
    @commands.is_owner()
    async def say(self, ctx, message):
        await ctx.send(message)
        await ctx.message.delete()
       
 
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down...")
        await asyncio.sleep(1)
        await self.bot.logout()
 

'''
    @commands.command()
    @commands.is_owner()
    async def meow(self, ctx):
        try:
            guild = self.bot.get_guild(786388384352174110)
            role = guild.get_role(826113736002895912)
            await ctx.author.add_roles(role)
            await ctx.send("done")
        except Exception as e:
            print(e)
'''       


def setup(bot):
    bot.add_cog(Owner(bot))

