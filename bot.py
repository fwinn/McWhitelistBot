import discord
from discord.ext import commands
import os

from modules import *
import modules

import logging
logging_level = os.getenv('LOGGING_LEVEL')
level = logging.getLevelName(logging_level)
logging.basicConfig(level=level, filename='log/bot.log')

bot = commands.Bot(command_prefix='.')
bot_token = os.getenv('BOT_TOKEN')
server_ip = os.getenv('SERVER_IP')
mc_version = '1.16.5'
admin_channel = int(os.getenv('ADMIN_CHANNEL_ID'))
requests_messages = []


def take_request(message_id):
    for i in requests_messages:
        if i.admin_msg_id == message_id:
            tmp = i
            requests_messages.remove(i)
            return tmp


# Bot events:
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('Minecraft'), status=discord.Status.online)
    global requests_messages
    requests_messages = modules.filemanager.load_requests()
    logging.info('Requests loaded from last sessions: ' + str(requests_messages))
    logging.info('Ready, username: {}'.format(bot.user.name))





@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        msg = reaction.message
        if msg.author == bot.user:
            admin = bot.get_channel(admin_channel)
            current = take_request(msg.id)
            await msg.clear_reactions()
            if type(current) == request.WhitelistRequest:
                dc_user = await bot.fetch_user(current.dc_id)
                mc_name = current.mc_name
                if reaction.emoji == '✅':
                    await modules.filemanager.write_whitelist(current)
                    logging.info('Player whitelisted: {} {} {}'.format(mc_name, current.first_name, current.classs))
                    embed = discord.Embed(title='Server', color=0x22a7f0)
                    embed.add_field(name='IP', value=server_ip)
                    embed.add_field(name='Version', value=mc_version)
                    await dc_user.send(
                        'Deine Anfrage für den Account `{}` wurde angenommen. Womöglich dauert es noch kurz,'
                        ' bis du auf dem Server spielen kannst.'.format(mc_name),
                        embed=embed)
                    await admin.send('The player `{}` was whitelisted.'.format(mc_name))
                else:
                    await admin.send('The request for the player `{}` was denied.'.format(mc_name))
                    await dc_user.send('Deine Anfrage für den Spieler `{}`wurde abgelehnt. Bei Fragen kontaktiere die '
                                       'Admins im support-Channel auf dem Discord-Server.'.format(mc_name))


# Bot commands:
@bot.command()
async def whitelist(ctx, arg1, arg2, arg3):
    logging.info('Request incoming...')
    mc_name = arg1
    first_name = arg2
    classs = arg3
    member = ctx.author
    await ctx.message.delete()
    admins = bot.get_channel(admin_channel)
    logging.debug('Fetching UUID...')
    uuid = util.get_uuid(mc_name)
    if not uuid:
        await ctx.send('Der Spieler `{}` wurde nicht gefunden {}.'.format(mc_name, member.mention))
        return
    logging.debug('Checking if IDs are already in the database...')
    ids_in_db_amount = modules.filemanager.ids_in_db(uuid, member.id)
    if ids_in_db_amount[0] > 0:
        await ctx.send('Der Spieler `{}` ist bereits gewhitelistet {}.'.format(mc_name, member.mention))
        return
    embed = discord.Embed(title='Whitelist-Anfrage', color=0x22a7f0)
    embed.add_field(name='von', value=member.mention)
    embed.add_field(name='MC-Username', value=mc_name)
    embed.add_field(name='Vorname', value=first_name)
    embed.add_field(name='Klasse', value=classs)
    embed.add_field(name='Von diesem User bereits gewhitelistet', value=ids_in_db_amount[1])
    admin_msg = await admins.send(embed=embed)
    await admin_msg.add_reaction('✅')
    await admin_msg.add_reaction('❌')
    requests_messages.append(request.WhitelistRequest(member.id, admin_msg.id, mc_name, uuid, first_name, classs))
    await ctx.send('Deine Anfrage für `{}` wurde versandt {}.'.format(mc_name, member.mention))
    logging.info('Request succesful')


@bot.command()
async def shutdown(ctx):
    if ctx.channel.id == admin_channel:
        await bot.change_presence(status=discord.Status.offline)
        modules.filemanager.save_requests(requests_messages)
        await bot.logout()


# Errors:
@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        logging.error(error)
        await ctx.send('Bitte benutze `.whitelist [Minecraft username] [Vorname] [Klasse].` (keine Leerzeichen '
                       'innerhalb der Argumente)')


bot.run(bot_token)
