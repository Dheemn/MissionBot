#!/usr/bin/env python3

import discord
#import logging

from discord.ext import commands
from dotenv import dotenv_values

class CommonFuncs():
    def __init__(self):
        pass

    #Get roles for user
    def getRoles(self, m):
        #role = []
        #for x in (m.message.author).roles:
        #    role.append(str(x.name))
        user = m.message.author
        role = discord.utils.get(user.roles)
        return role

    #Checks permissions for certain commands
    def checkPerms(self, m, roles):
        role = self.getRoles(m)
        for i in roles:
            for j in role:
                if j == i:
                    return True
        return False


""" class MissionBot(discord.Client, CommonFuncs):
    
    def __init__(self):
        self._roleid = ['876015863663308821']

        super().__init__()

    async def on_ready(self):
        print("Logged in as {0.user}".format(client))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith("$missionAdd"):
            if CommonFuncs.checkPerms(self, message, self._roleid):
                await message.channel.send("This is the cmd to create coalition missions!")
            else:
                await message.channel.send("You need appropriate permissions")

        if message.content.startswith('$myroles'):
            print("$myroles request by:" + str(message.author))
            role = CommonFuncs.getRoles(self, message)
            print(role)
            await message.channel.send("Your roles: {}".format(role)) """


#client = MissionBot()

intents = discord.Intents(messages = True, members = True)
bot = commands.Bot(command_prefix='$', intents=intents)

funcs = CommonFuncs()

@bot.event
async def on_ready():
    print("Logged in as {0.name}{0.id}".format(bot.user))

@bot.command(pass_context = True)
async def myroles(ctx):
    print("$myroles request by:" + str(ctx.author))
    role = funcs.getRoles(ctx)
    print(type(role))
    await ctx.send("Your roles: " + str(role))

config = dotenv_values('.env')
bot.run(config['TOKEN'])
