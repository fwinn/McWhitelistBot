import ast

import discord
import requests
import json
from discord.ext import commands

bot = commands.Bot(command_prefix='.')
whitelist_location = 'path/to/whitelist.json'
adminlist_location = 'path/to/admins.json'
requests_location = 'path/to/requests.json'
requests_messages = []
ip = 'your ip'
version = 'minecraft version'


class Request:
    def __init__(self, author_id, admin_msg_id):
        self.author_id = author_id
        self.admin_msg_id = admin_msg_id


class WhitelistRequest(Request):
    def __init__(self, author_id, admin_msg_id, mc_name, uuid):
        super().__init__(author_id, admin_msg_id)
        self.mc_name = mc_name
        self.uuid = uuid


def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


def take_request(message_id):
    for i in requests_messages:
        if i.admin_msg_id == message_id:
            tmp = i
            requests_messages.remove(i)
            return tmp


@bot.event
async def on_ready():
    print('Ready, username: {}'.format(bot.user.name))
    await bot.change_presence(activity=discord.Game('Minecraft'), status=discord.Status.online)
    # TODO: Read pending requests out of file


@bot.event
async def on_disconnect():
    data = []
    for i in requests_messages:
        d = {'type': type(i), 'author_id': i.author_id, 'admin_msg_id': i.admin_msg_id}
        if type(i) == WhitelistRequest:
            d['mc_name'] = i.mc_name
            d['uuid'] = i.uuid
        data.append(d)
    with open(requests_location, 'w') as outfile:
        json.dump(data, outfile)


@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        msg = reaction.message
        if msg.author == bot.user:
            admin = user
            request = take_request(msg.id)
            await msg.delete()
            if type(request) == WhitelistRequest:
                mcname = request.mc_name
                dcuser = await bot.fetch_user(request.author_id)
                if reaction.emoji == '✅':
                    uuid = request.uuid
                    await writewhitelist(mcname, uuid)
                    print('Player whitelisted: ' + mcname + ' ' + uuid)
                    embed = discord.Embed(title='Server', color=0x22a7f0)
                    embed.add_field(name='IP', value=ip)
                    embed.add_field(name='Version', value=version)
                    await dcuser.send(
                        'Your request for the player  `' + mcname + 'was accepted. It may take up to 5 more minutes'
                                                                    'until you will be able to join the server.',
                        embed=embed)
                    await admin.send('The player `' + mcname + '` was whitelisted.')
                else:
                    await admin.send('The request for the player `' + mcname + '` was denied.')
                    await dcuser.send('Your request for the player `' + mcname + '`was denied.')


def get_uuid(mcname):
    d = ast.literal_eval(requests.get('https://api.mojang.com/users/profiles/minecraft/' + mcname).text)
    unformatted = d['id']
    part = unformatted[:8], unformatted[8:12], unformatted[12:16], unformatted[16:20], unformatted[20:]
    return part[0] + '-' + part[1] + '-' + part[2] + '-' + part[3] + '-' + part[4]


def get_admin_id(guild_id):
    with open(adminlist_location, 'r') as file:
        data = json.load(file)
    return int(data[str(guild_id)])


def add_admin(admin_id, guild_id, admins_dict):
    admins_dict[str(guild_id)] = admin_id
    with open(adminlist_location, 'w') as outfile:
        print('Writing admin data...')
        json.dump(admins_dict, outfile)
    print('Success')


async def writewhitelist(mcname, uuid):
    print('Writing whitelist...')
    with open(whitelist_location, 'r') as json_data:
        data = json.load(json_data)
        data = merge_two_dicts(data, {"uuid": uuid, "name": mcname})
    with open(whitelist_location, 'w') as outfile:
        json.dump(data, outfile)
    print('Done')


@bot.command()
async def whitelist(ctx, arg):
    mcname = arg
    member = ctx.author
    await ctx.message.delete()
    admin_id = get_admin_id(member.guild.id)
    if not admin_id:
        await ctx.send('Fatal Error: No admin defined for this server.')
        return
    admin = await bot.fetch_user(admin_id)
    uuid = get_uuid(mcname)
    if not uuid:
        await ctx.send('Player `{}` not found {}.'.format(mcname, member.mention))
        return
    embed = discord.Embed(title='Whitelist request', color=0x22a7f0)
    embed.add_field(name='by', value=ctx.author.mention)
    embed.add_field(name='MC-Username', value=mcname)
    embed.add_field(name='joined server', value=member.joined_at.strftime('%d.%m.%Y, %H:%M'))
    adminmsg = await admin.send(embed=embed)
    await adminmsg.add_reaction('✅')
    await adminmsg.add_reaction('❌')
    requests_messages.append(WhitelistRequest(ctx.author.id, adminmsg.id, mcname, uuid))
    await ctx.send('Your request for whitelisting `{}` was sent {}.'.format(mcname, member.mention))


@bot.command()
async def imtheadmin(ctx):
    author = ctx.author
    guild_id = ctx.author.guild.id
    await ctx.message.delete()
    with open(adminlist_location, 'r') as json_data:
        print('Reading admin data...')
        data = json.load(json_data)
    if str(guild_id) in data:
        old_admin = await bot.fetch_user(get_admin_id(guild_id))
        embed = discord.Embed(title='Admin request')
        embed.add_field(name='by', value=author.mention)
        embed.add_field(name='joined server', value=author.joined_at.strftime('%d.%m.%Y, %H:%M'))
        adminmsg = await old_admin.send(embed=embed)
        requests_messages.append(Request(author.id, adminmsg.id))
        await adminmsg.add_reaction('✅')
        await adminmsg.add_reaction('❌')
        await ctx.send('Your request for administration privileges was sent to an existing admin. ' + author.mention)
    else:
        add_admin(author.id, guild_id, data)


@whitelist.error
async def whitelist_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please use .whitelist [Minecraft username].')


bot.run('your bot token')
