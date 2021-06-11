import discord
from discord.ext import commands
import datetime
import os
from os import environ

#color values
GREEN_PRINT = '\033[92m'
ERROR_PRINT = '\033[93m'
COMMAND = '\033[96m'

client = discord.Client(client_prefix='pin.')

ClientKey = environ['BOT_API_KEY']
PinsChannel = environ['TARGET_CHANNEL']
FT_zip = environ['FT_ZIP']
FT_file = environ['FT_FILE']
PinContentChannel = None
PinContentCID = None

async def FindChannel(CTF):
    print(f'Pinbot: attempting to find channel {CTF}')
    for channel in client.get_all_channels():
        if(channel.name == CTF):
            print('Pinbot: channel found')
            return channel.id
    return None

@client.event
async def on_ready():
    global PinsChannel
    global PinContentChannel
    global PinContentCID
    PinContentCID = await FindChannel(PinsChannel)
    if(PinContentCID == None):
        print(f'{ERROR_PRINT}Couldnt find channel: {PinsChannel}')
        quit()
    else:
        print(f'{GREEN_PRINT}Found channel: {PinsChannel}')
    PinContentChannel = await client.fetch_channel(PinContentCID)
    print("the bot is running")

@client.event
async def on_raw_reaction_add(payload):
    global PinContentChannel
    global PinContentCID
    global FT_zip
    global FT_file
    if(payload.emoji.name == "📌" and payload.channel_id != PinContentCID):
        msgchannel = await client.fetch_channel(payload.channel_id)
        origin = await msgchannel.fetch_message(payload.message_id)

        emb = discord.Embed(color=discord.Color.from_rgb(198, 120, 221))
        datet = str(origin.created_at)
        dc = datet[0:len(datet)-7]
        ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emb.title = f'{payload.member.name} pinned from #{origin.channel.name}'
        emb.set_author(name=payload.member.name, icon_url=payload.member.avatar_url)
        emb.add_field(name=f'sent: {dc}, pinned: {ct}', value=f'[Pin Origin]({origin.jump_url})', inline=False)
        emb.add_field(name='Author:', value=origin.author.name, inline=False)

        if(len(origin.attachments) != 0):
            for a in origin.attachments:
                emb.add_field(name=f'FileName: ', value=a.filename, inline=False)
                emb.add_field(name=f'FileURL:', value=a.url, inline=False)
                emb.set_thumbnail(url=FT_zip if('zip' in a.content_type) else FT_file)
                try: emb.set_image(url=a.url)
                except: pass
        elif(len(origin.embeds) != 0):
            for e in origin.embeds:
                emb.add_field(name=e.url, value=e.description, inline=False)
                emb.add_field(name='Image:', value=e.image.url, inline=True)
                emb.add_field(name='Thumbnail:', value=e.thumbnail.url, inline=True)
                emb.add_field(name='Video:', value=e.video.url, inline=True)
                try: emb.set_thumbnail(url=e.thumbnail.url)
                except: pass
        else:
            emb.add_field(name="Content", value=origin.content, inline=False)
        print('Pinbot: embed sent')
        await PinContentChannel.send(embed=emb)

async def GetFromPins(message, msg):
    print(f'PinBot: {msg}')
    await message.channel.send(f'Finding channel: {msg[9:len(msg)]}')
    try:
        TargetChannel = int(msg[msg.index('#')+1:len(msg)-1])
    except:
        await message.channel.send('Couldnt find channel')
        return
    Channel = client.get_channel(TargetChannel)
    ChannelPinned = await Channel.pins()
    await message.channel.send(f'Found Channel {Channel.name} with {len(ChannelPinned)} pins')
    for pins in ChannelPinned:
        await pins.add_reaction('📌')
    await message.channel.send('finished')

@client.event
async def on_message(message):
    msg = message.content.lower()
    #if('pin.from' in msg):
    #    await GetFromPins(message, msg)
    if(not message.guild and not message.author.bot):
        with open('dmreply1.mp4', 'rb') as filestream:
            await message.channel.send(file=discord.File(filestream, 'dmreply1.mp4'))

async def ReactionOnMessage(msg, reaction):
    for r in msg.reactions:
        if(r.emoji == reaction):
            return True
    return False

async def FindOriginMsg(message):
    for e in message.embeds:
        for f in e.fields:
            val = str(f.value)
            if('(' in val):
                link = val[val.index('(')+1:len(val)-1].split('/')
                return await client.get_guild(int(link[-3])).get_channel(int(link[-2])).fetch_message(int(link[-1]))
    return None

@client.event
async def on_message_delete(message):
    print('Pinbot: linking removal')
    global PinContentChannel
    if(message.channel == PinContentChannel):
        link = await FindOriginMsg(message)
        if(link != None):
            await link.clear_reaction('📌')

client.run(ClientKey)