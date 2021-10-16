#!/usr/bin/env python3

from discord.ext import commands
from dotenv import dotenv_values

import discord
import logging

class CommonFuncs():
    def __init__(self):
        pass

    #Get roles for user
    def getRoles(self, m):
        role = []
        for x in (m.roles):
            role.append(str(x.id))
        
        return role

    #Checks permissions for certain commands
    def checkPerms(self, m, roles):
        member : discord.Member=None
        if member is None:
            member = m.author
        role = self.getRoles(member)
        for i in roles:
            for j in role:
                if j == i:
                    return True
        return False


intents = discord.Intents(messages = True, members = True, guilds = True)
bot = commands.Bot(command_prefix='$', intents=intents)

funcs = CommonFuncs()

suRoles = ['']
allowed_roles = ['']

@bot.event
async def on_ready():
    print("Logged in as {0.name}{0.id}".format(bot.user))

@bot.command()
async def addRole(ctx, *, roleid=None):
    print(f"$addRole request by {ctx.author}")
    if roleid is None:
        await ctx.send("```Help: This command gives permission to role members to post Coalition Missions\nUsage: $addRole <roleID of role>```")
        return
    #checks perms with su users i.e discord admins
    if funcs.checkPerms(ctx, suRoles):
        allowed_roles.append(str(roleid))
        await ctx.send(f'RoleID {roleid} has been added')
    else:
        await ctx.send("You do not have neccesary permissions")
    #Having some issues with this code line, will deal with later
    #roleName = guild.Guild.get_role(self, role_id = roleid)

@bot.command()
async def rmRole(ctx, *, roleid=None):
    print(f"$rmRole request by {ctx.author}")
    if roleid is None:
        await ctx.send("```Help: This command removes permission for role members to post Coalition Missions\nUsage: $rmRole <roleID of role>```")
        return
    #checks perms with su users i.e discord admins
    if funcs.checkPerms(ctx, suRoles):
        allowed_roles.remove(str(roleid))
        await ctx.send(f'RoleID {roleid} has been removed')
    else:
        await ctx.send("You do not have neccesary permissions")
    #Having some issues with this code line, will deal with later
    #roleName = guild.Guild.get_role(self, role_id = roleid)

@bot.command()
async def myroles(ctx, *, member : discord.Member=None):
    print("$myroles request by:" + str(ctx.author))
    if member is None:
        member = ctx.author
    role = funcs.getRoles(member)
    await ctx.send("Your roles: " + str(role))

@bot.command()
async def missionAdd(ctx, *, arg):
    help = """```This command creates Coalition missions\nUsage: !missionCreate [title];
[description: Supports standard discord formatting.];\n
[category: "BGS"/"Research"];
[status: "recruiting"/"progress"/"success"/"failed"];
[agents: @ yourself or agent(s) in charge];\n
[personnel];
[skills beyond category];
[timeframe];
[platform];```"""

    if funcs.checkPerms(ctx, allowed_roles) is False:
        await ctx.send("You need appropriate permissions")
        return
    if (len(arg) == 0):
        await ctx.send(help)
        return
    message = str(arg)
    mission = message.split(';')
    print(mission)

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


config = dotenv_values('.env')
client.run(config['TOKEN'])
