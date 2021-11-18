#!/usr/bin/env python3

import datetime
import discord
import logging
import sys

from discord.ext import commands
from dotenv import dotenv_values

class CommonFuncs():
    def __init__(self):
        pass

    #Get roles for user
    def getRoles(self, m, t : str):
        role = []
        if t=='id':
            for x in (m.roles):
                role.append(str(x.id))
            role.remove('<@everyone roleID>')
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

    async def createEmbed(self, title='', author=None, reason=None, channel=None):
        embed = discord.Embed(title=title, color=0x1bc704)
        embed.set_author(name=author[0], icon_url=author[1])
        embed.set_thumbnail(url=author[1])
        embed.add_field(name=reason[0], value=reason[1], inline=False)
        embed.set_footer(text=f'UserID {author[2]}')
        await channel.send(embed=embed)

    #Creates embeds for mission
    async def mEmbed(self, reason=None, channel=None, edit=False):
        #Title=0; Description=1; Category=2; Status=3; Agents=4; Personnel=5; Skills=6; Timeframe=7; Platform=8
        embed = discord.Embed(title=reason[0])
        embed.color=0xeb4034
        #This checks if there are any Agents assigned to the mission
        if (reason[4] == ''): embed.add_field(name='***Status***', value=reason[3], inline=False)
        else: embed.add_field(name='***Status***', value=f'{reason[3]}, {reason[4]}', inline=False)
        embed.add_field(name='Description: ', value=f'>>> {reason[1]}', inline=False)
        embed.add_field(name='Required Personnel: ', value=reason[5], inline=False)
        embed.add_field(name='Skill Required: ', value=reason[6], inline=False)
        embed.add_field(name='Timeframe: ', value=reason[7], inline=False)
        embed.add_field(name='Platform: ', value=reason[8], inline=False)
        if edit != False:
            return embed
        msg = await channel.send(embed=embed)
        return msg.id


def main():

    intents = discord.Intents(messages = True, members = True, guilds = True)
    bot = commands.Bot(command_prefix='$', intents=intents)

    logging.basicConfig(filename='bot.log', format='%(levelname)s:%(message)s', level=logging.INFO)

    funcs = CommonFuncs()

    ANNOUNCMENT_CHANNEL = <announcement_channel>
    ADMIN_CHANNEL = <admin_channel>

    suRoles = []
    allowed_roles = []

    @bot.event
    async def on_ready():
        logging.info(f'[{datetime.datetime.now()}]: Logged in as {bot.user.name}{bot.user.id}')
        #print(f'[{datetime.datetime.now()}]: Logged in as {bot.user.name}{bot.user.id}')

    @bot.command()
    async def ping(ctx):
        #print(f'[{datetime.datetime.now()}]: {ctx.author} pinged me!!!')
        logging.info(f'[{datetime.datetime.now()}]: {ctx.author} pinged me!!!')
        await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

    @bot.command()
    #@commands.has_any_role(suRoles)
    async def addRole(ctx, *, roleid=None):
        logging.info(f"[{datetime.datetime.now()}]: $addRole request by {ctx.author}")
        #checks perms with su users i.e discord admins
        if funcs.checkPerms(ctx, suRoles) is False:
            await ctx.reply("You do not have neccesary permissions")
            logging.info(f'[{datetime.datetime.now()}]: {ctx.author} tried using $addRole command. Denied!')
            return
        if roleid is None:
            await ctx.reply("```Help: This command gives permission to role members to post Coalition Missions\nUsage: $addRole <roleID of role>```")
            return
        allowed_roles.append(str(roleid))
        logging.info(f'[{datetime.datetime.now()}]: RoleID {roleid} has been added to inclusion zone by {ctx.author}')
        await ctx.reply(f'RoleID {roleid} has been added')
        
    @bot.command()
    #@commands.has_any_role(su)
    async def rmRole(ctx, *, roleid=None):
        logging.info(f"[{datetime.datetime.now()}]: $rmRole request by {ctx.author}")
        #checks perms with su users i.e discord admins
        if funcs.checkPerms(ctx, suRoles) is False:
            await ctx.reply("You do not have neccesary permissions to perform action!")
            logging.info(f'[{datetime.datetime.now()}]: {ctx.author} tried using $rmRole command. Denied!')
            return
        if roleid is None:
            await ctx.reply("```Help: This command gives permission to role members to post Coalition Missions\nUsage: $addRole <roleID of role>```")
            return
        allowed_roles.remove(str(roleid))
        logging.info(f'[{datetime.datetime.now()}]: RoleID {roleid} has been removed from inclusion zone by {ctx.author}')
        await ctx.reply(f'RoleID {roleid} has been removed')

    @bot.command()
    async def myroles(ctx, *, member : discord.Member=None):
        logging.info(f'[{datetime.datetime.now()}]: $myroles request by: {ctx.author}')
        if member is None:
            member = ctx.author
        role = funcs.getRoles(member, 'name')
        logging.info(msg=f'[{datetime.datetime.now()}]: $myroles request by: {ctx.author}')
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

        logging.info(f"[{datetime.datetime.now()}]: $missionCreate request by: {ctx.author}")
        if funcs.checkPerms(ctx, allowed_roles) is False:
            logging.info(f"[{datetime.datetime.now()}]: $missionCreate request by: {ctx.author} was denied")
            await ctx.send("You need appropriate permissions")
            return
        if (len(args) == 0):
            await ctx.send(help)
            return
        message = str(args[0])
        mission = message.split(';')
    
        #Title=0; Description=1; Category=2; Status=3; Agents=4; Personnel=5; Skills=6; Timeframe=7; Platform=8
        msg_ID = await funcs.mEmbed(reason=mission, channel=bot.get_channel(ANNOUNCMENT_CHANNEL))
        reason = (':white_check_mark: Created mission', f'@{ctx.author.mention} has created a mission with MsgID: {msg_ID}')
        author = (ctx.author.display_name, ctx.author.avatar_url, ctx.author.id)
        await ctx.send(f':white_check_mark: Mission created with messageID {msg_ID}')
        await funcs.createEmbed(title='Mission Created',author=author, reason=reason, channel=bot.get_channel(ADMIN_CHANNEL))
        logging.info(f"[{datetime.datetime.now()}]: $missionCreate request by: {ctx.author} granted and success with msgID: {msg_ID}")

    @bot.command()
    async def missionEdit(ctx, message: commands.MessageConverter, arg):
        logging.info(f"[{datetime.datetime.now()}]: $missionEdit request by: {ctx.author}")
        if funcs.checkPerms(ctx, allowed_roles) is False:
            logging.info(f"[{datetime.datetime.now()}]: $missionCreate request by: {ctx.author} was denied")
            await ctx.send("You need appropriate permissions")
            return
        mission = arg.split(';')

        await message.edit(embed=await funcs.mEmbed(reason=mission, channel=bot.get_channel(ANNOUNCMENT_CHANNEL), edit=True))
        await ctx.reply(f':white_check_mark: Message has been edited with msgID:{message.id}')
        #Title=0; Description=1; Category=2; Status=3; Agents=4; Personnel=5; Skills=6; Timeframe=7; Platform=8
        reason = (':white_check_mark: Edited mission', f'{ctx.author.mention} has edited a mission with MsgID: {message.id}')
        author = (ctx.author.display_name, ctx.author.avatar_url, ctx.author.id)

        await funcs.createEmbed(author=author, reason=reason, channel=bot.get_channel(ADMIN_CHANNEL))
        logging.info(f"[{datetime.datetime.now()}]: $missionCreate request by: {ctx.author} granted and success with msgID: {message.id}")

    @missionEdit.error
    async def missionEdit_error(ctx, error):
        help = """```This command edits Coalition missions\nUsage: $missionEdit [MessageID of Mission] "[title];
[description: Supports standard discord formatting.];\n
[category: "BGS"/"Research"];
[status: "recruiting"/"progress"/"success"/"failed"];
[agents: @ yourself or agent(s) in charge];\n
[personnel];
[skills beyond category];
[timeframe];
[platform];"```"""
        print(f"[{datetime.datetime.now()}]: $missionEdit error by: {ctx.author}")
        if isinstance(error, commands.MissingRequiredArgument):
            logging.error(f'[{datetime.datetime.now()}]: $missionEdit Error: {error}')
            await ctx.send(f'Missing Arguments \n{help}')
            return
        if isinstance(error, commands.MessageNotFound):
            logging.error(f'[{datetime.datetime.now()}]: $missionEdit Error: {error}')
            await ctx.send('Oops! Something went wrong. Please provide valid message ID with channelID. Eg: <channelID-messageID> or its URL')
            return

    @bot.command()
    async def missionRM(ctx, message: commands.MessageConverter):
        logging.info(f"[{datetime.datetime.now()}]: $missionRM request by: {ctx.author}")
        if funcs.checkPerms(ctx, allowed_roles) is False:
            logging.info(f"[{datetime.datetime.now()}]: $missionRM request by: {ctx.author} was denied")
            await ctx.send("You need appropriate permissions")
            return
        if message.channel.id != ANNOUNCMENT_CHANNEL:
            logging.info(f'[{datetime.datetime.now()}]: User {ctx.author} tried deleting message outside of announcement channel')
            await ctx.send('You cannot delete messages outside the Coalition Mission channel')
            return

        msg_id = message.id
        await message.delete()

        reason = (':white_check_mark: Deleted mission', f'{ctx.author.mention} has deleted a mission with MsgID: {msg_id}')
        author = (ctx.author.display_name, ctx.author.avatar_url, ctx.author.id)

        await ctx.send(f':white_check_mark: Mission with messageID:{msg_id} successfully deleted')
        await funcs.createEmbed(title='Message Deleted', author=author, reason=reason, channel=bot.get_channel(ADMIN_CHANNEL))
        logging.info(f'[{datetime.datetime.now()}]: User {ctx.author} deleted mission with msgID {msg_id} successfully')

    @missionRM.error
    async def missionRM_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            logging.error(f'[{datetime.datetime.now()}]: $missionRM Error: {error}')
            await ctx.send('```Missing argument\nThis command deletes the coalition mission\n Usage: $missionRM [messageID/URL of the mission]```')
            return
        if isinstance(error, commands.MessageNotFound):
            logging.error(f'[{datetime.datetime.now()}]: $missionRM Error: {error}')
            await ctx.send('Oops! Something went wrong. Please provide valid message ID with channelID. Eg: <channelID-messageID> or its URL')
            return
    
    @bot.event
    async def on_command_error(ctx, error):
        
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        #error = getattr(error, 'original', error)
        
        if isinstance(error, commands.CommandNotFound):
            logging.error(f'[{datetime.datetime.now()}]: {ctx.author} tried executing {ctx.message.content}, ERROR: not found')
            await ctx.send(f'Command {ctx.message.content} not found')
            return
        if isinstance(error, commands.DisabledCommand):
            logging.error(f'[{datetime.datetime.now()}]: {ctx.author} tried executing disabled command: {ctx.message.content}')
            await ctx.send(f'{ctx.message.content} has been disabled.')
            return
        if isinstance(error, discord.DiscordException):
            logging.error(f'[{datetime.datetime.now()}]: Error: {error}')
            await ctx.send('Error has occured!! Please contact bot maintainer')
            return

    config = dotenv_values('.env')
    bot.run(config['TOKEN'])

if __name__=='__main__':
    try:
        main()
    except KeyboardInterrupt or SystemExit:
        print('Exiting.....')
        sys.exit(0)
