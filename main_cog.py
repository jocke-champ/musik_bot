import discord
from discord.ext import commands

class main_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
Allmänna kommandon:
/hjälp - visar alla tillgängliga kommandon

Musikkommandon:
/spela <nyckelord> - hittar låten på youtube och spelar den
/kö - visar den aktuella musikköen
/skippa - hoppar över den aktuella låten som spelas
```
"""
        self.text_channel_list = []

    #lite felsökningsinformation så att vi vet att boten har startat 
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)

        await self.send_to_all(self.help_message)        

    @commands.command(name="hjälp", help="Visar alla kommandon")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)
