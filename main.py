import json
import discord
from discord.ext import commands
from modules.chat_utils import *
from modules.data_initializer import *
from char import leave, list, take, status, template

def __init__():
    with open('config.json') as jsonFile:
        data = json.load(jsonFile)

        global TOKEN, client
        TOKEN = data['TOKEN']
        client = commands.Bot(command_prefix=data['prefix'])
        client.remove_command('help')

    with open('files/char_parameters.json') as jsonFile:
        global parameters
        parameters = json.load(jsonFile)


__init__()
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='>>char help'))

BR, TAB = '\n', '\t'


async def create_role(author, role_name, role_colour):
    role = await client.create_role(author.server, name=role_name, colour=role_colour)
    return role


@client.command(pass_context=True)
@commands.cooldown(1, 2, commands.BucketType.user)
async def char(ctx, *args):
    def get_help_msg():
        command = '>>char '
        message = bold('Usage:') + BR
        message += bold(command + 'list (table) [all]') + ' - List all characters from the table' + BR
        message += bold(command + 'take (character)') + ' - Assign youself to a character' + BR
        message += bold(command + 'leave') + ' - Stop being your character' + BR
        message += bold(command + '(character)') + ' - Get info about the character' + BR
        return message

    try:
        if args[0] == 'list':
            await list.run(client, ctx, args, parameters['list'])
        elif args[0] == 'take':
            await take.run(client, ctx, args, parameters['take'])
        elif args[0] == 'leave':
            await leave.run(client, ctx)
        elif args[0] == 'template':
            await template.run(client, ctx, args)
        else:
            await status.run(client, ctx, args)
    except IndexError:
        await client.say(get_help_msg())


@client.command()
async def info():
    msg = ''
    msg += 'CharacterBot v0.5' + BR
    msg += 'A bot that turns users into their favourite characters! Check `>>help` for usage.' + BR
    msg += 'Developed by Trifo Reborn#1676'
    await client.say(msg)

@client.command(pass_context=True)
async def share(ctx):
    await client.send_message(ctx.message.author, 'https://bit.ly/CharacterBotInvite')

@client.command()
async def help():
    msg = bold('>>char') + ' - For all your roleplaying needs' + BR
    msg += bold('>>info') + ' - Find out who made this bot' + BR
    msg += bold('>>share') + ' - Add this bot to YOUR server!'
    await client.say(msg)


client.run(TOKEN)