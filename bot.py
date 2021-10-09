import discord

class CommonFuncs():
    def __init__(self):
        self._roleid = ['876015863663308821']
    
    #Get roles for user
    def getRoles(self, m):
        role = []
        for x in m.author.roles:
            role.append(str(x.id))
        return role

    #Checks permissions for certain commands
    def checkPerms(self, m):
        role = self.getRoles(m)
        for i in role:
            if self._roleid == i:
                return True
        return False


class MissionBot(discord.Client, CommonFuncs):

    #func = CommonFuncs()

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
client.run('ODk2MjY2MDI3MzgwNDA0MjM1.YWEmyA.g4y8JG3JRU7tSJOeOJ8Q1LnD90I')
