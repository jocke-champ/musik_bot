import discord
from discord.ext import commands

import os

#importera alla kuggar
from main_cog import main_cog
from music_cog import music_cog

bot = commands.Bot(command_prefix='/')

#ta bort standardhjälpkommandot så att vi kan skriva ut egna
bot.remove_command('help')

#registrera klassen med boten
bot.add_cog(main_cog(bot))
bot.add_cog(image_cog(bot))
bot.add_cog(music_cog(bot))

#token
TOKEN = open('token.txt','r')
bot.run(TOKEN)
