#!/usr/bin/env python3

import datetime
import discord
#import logging

from discord.ext import commands
from dotenv import dotenv_values

class CommonFuncs():
    def __init__(self):
        pass

    #Get roles for user
    def getRoles(self, m, type : str):
        role = []
        if type=='id':
            for x in (m.roles):
                role.append(str(x.id))
            role.remove('828538918823657503')
        else:
            for x in (m.roles):
                role.append(str(x.name))
            role.remove('@everyone')
        return role

    #Checks permissions for certain commands
    def checkPerms(self, m, roles):
        member : discord.Member=None
        if member is None:
            member = m.author
        role = self.getRoles(member, 'id')
        for i in roles:
            for j in role:
                if j == i:
                    return True
        return False

#client = MissionBot()

def main():

    intents = discord.Intents(messages = True, members = True, guilds = True)
    bot = commands.Bot(command_prefix='$', intents=intents)

    funcs = CommonFuncs()

    suRoles = ['']
    allowed_roles = ['']

    @bot.event
    async def on_ready():
        print("[{0}]: Logged in as {1.name}{1.id}".format(datetime.datetime.now(), bot.user))

    @bot.command()
    async def ping(ctx):
        print(f'[{datetime.datetime.now()}]: {ctx.author} pinged me!!!')
        await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

    @bot.command()
    async def addRole(ctx, *, roleid=None):
        print(f"[{datetime.datetime.now()}]: $addRole request by {ctx.author}")
        #checks perms with su users i.e discord admins
        if funcs.checkPerms(ctx, suRoles) is False:
            await ctx.send("You do not have neccesary permissions")
            return
        if roleid is None:
            await ctx.send("```Help: This command gives permission to role members to post Coalition Missions\nUsage: $addRole <roleID of role>```")
            return
        allowed_roles.append(str(roleid))
        print(f'[{datetime.datetime.now()}]: RoleID {roleid} has been added to inclusion zone')
        await ctx.send(f'RoleID {roleid} has been added')
        
        #Having some issues with this code line, will deal with later
        #roleName = guild.Guild.get_role(self, role_id = roleid)

    @bot.command()
    async def rmRole(ctx, *, roleid=None):
        print(f"[{datetime.datetime.now()}]: $rmRole request by {ctx.author}")
        #checks perms with su users i.e discord admins
        if funcs.checkPerms(ctx, suRoles) is False:
            await ctx.send("You do not have neccesary permissions")
            return
        if roleid is None:
            await ctx.send("```Help: This command gives permission to role members to post Coalition Missions\nUsage: $addRole <roleID of role>```")
            return
        allowed_roles.remove(str(roleid))
        print(f'[{datetime.datetime.now()}]: RoleID {roleid} has been removed from inclusion zone')
        await ctx.send(f'RoleID {roleid} has been removed')
        #Having some issues with this code line, will deal with later
        #roleName = guild.Guild.get_role(self, role_id = roleid)

    @bot.command()
    async def myroles(ctx, *, member : discord.Member=None):
        print(f"[{datetime.datetime.now()}]: $myroles request by: {ctx.author}")
        if member is None:
            member = ctx.author
        role = funcs.getRoles(member, 'name')
        await ctx.send("Your roles: " + str(role))

    @bot.command()
    async def clear(ctx, amount: int = 2):
        await ctx.channel.purge(limit=amount)

    @bot.command()
    async def missionCreate(ctx, *args):
        help = """```This command creates Coalition missions\nUsage: $missionCreate [title];
[description: Supports standard discord formatting.];\n
[category: "BGS"/"Research"];
[status: "recruiting"/"progress"/"success"/"failed"];
[agents: @ yourself or agent(s) in charge];\n
[personnel];
[skills beyond category];
[timeframe];
[platform];```"""

        print(f"[{datetime.datetime.now()}]: $missionCreate request by: {ctx.author}")
        if funcs.checkPerms(ctx, allowed_roles) is False:
            print(f"[{datetime.datetime.now()}]: $missionCreate request by: {ctx.author} was denied")
            await ctx.send("You need appropriate permissions")
            return
        if (len(args) == 0):
            await ctx.send(help)
            return
        message = str(args[0])
        mission = message.split(';')

        #Strips the 0th and last element(8th) of " from the mission list
    
        #Title=0; Description=1; Category=2; Status=3; Agents=4; Personnel=5; Skills=6; Timeframe=7; Platform=8
        await ctx.send(f'''**{mission[0]}**

*Status: **{mission[3]}, {mission[4]}***
*Category: **{mission[2]}***

>  {mission[1]}

*Personnel: **{mission[5]}***
*Skills: **{mission[6]}***
*Timeframe: **{mission[7]}***
*Platform: **{mission[8]}***''')
        print(f"[{datetime.datetime.now()}]: $missionCreate request by: {ctx.author} granted and success")

    @bot.event
    async def on_command_error(ctx, error):
        
        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        #error = getattr(error, 'original', error)
        
        if isinstance(error, commands.CommandNotFound):
            print(f'[{datetime.datetime.now()}]: {ctx.author} tried executing {ctx.message.content}, ERROR: not found')
            await ctx.send(f'Command {ctx.message.content} not found')
            return

        if isinstance(error, commands.DisabledCommand):
            print(f'[{datetime.datetime.now()}]: {ctx.author} tried executing disabled command: {ctx.message.content}')
            await ctx.send(f'{ctx.message.content} has been disabled.')


    config = dotenv_values('.env')
    bot.run(config['TOKEN'])

if __name__=='__main__':
    main()
