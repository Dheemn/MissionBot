#!/usr/bin/env python3

from dotenv import dotenv_values

import discord
import logging

class CommonFuncs():
    def __init__(self):
        pass
    
    #Get roles for user
    def getRoles(self, m):
        role = []
        for x in m.author.roles:
            role.append(str(x.id))
        return role

    #Checks permissions for certain commands
    def checkPerms(self, m):
        role = self.getRoles(m)
        for i in roles:
            for j in role:
                if j == i:
                    return True
        return False


class MissionBot(discord.Client, CommonFuncs):

    def __init__(self):
        self._roleid = ['876015863663308821']
        super().__init__()

    async def on_ready(self):
        print("Logged in as {0.user}".format(client))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith("$missionAdd"):
            if CommonFuncs.checkPerms(self, message):
                await message.channel.send("This is the cmd to create coalition missions!")
            else:
                await message.channel.send("You need appropriate permissions")

        if message.content.startswith('$myroles'):
            print("$myroles request by:" + str(message.author))
            role = CommonFuncs.getRoles(self, message)
            print(role)
            await message.channel.send("Your roles: {}".format(role))


client = MissionBot()
config = dotenv_values('.env')
client.run(config['TOKEN'])
