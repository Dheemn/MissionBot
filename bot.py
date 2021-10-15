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
async def missionAdd(ctx, *args):
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
    if (len(args) == 0):
        await ctx.send(help)
        return


config = dotenv_values('.env')
client.run(config['TOKEN'])
