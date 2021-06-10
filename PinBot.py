import discord
from discord.ext import commands
import datetime

#color values
GREEN_PRINT = '\033[92m'
ERROR_PRINT = '\033[93m'
COMMAND = '\033[96m'

client = discord.Client(client_prefix='pin.')

PinsChannel = "pinned-content"
PinContentChannel = None

FT_zip = 'https://discord.com/assets/4f27cbf7f975daa32fe7c8dec19ce2de.svg'
FT_file = 'https://discord.com/assets/66084381f55f4238d69e5cbe3b8dc42e.svg'

async def FindChannel(CTF):
    for channel in client.get_all_channels():
        if(channel.name == CTF):
            print(channel.name)
            return channel.id
    return None

@client.event
async def on_ready():
    global PinsChannel
    global PinContentChannel
    PinChannelID = await FindChannel(PinsChannel)
    if(PinChannelID == None):
        print(f'{ERROR_PRINT}Couldnt find channel: {PinsChannel}')
        quit()
    else:
        print(f'{GREEN_PRINT}Found channel: {PinsChannel}')
    PinContentChannel = await client.fetch_channel(PinChannelID)
    print("the bot is running")

@client.event
async def on_raw_reaction_add(payload):
    global PinContentChannel
    global FT_zip
    global FT_file
    if(payload.emoji.name == "📌"):
        msgchannel = await client.fetch_channel(payload.channel_id)
        origin = await msgchannel.fetch_message(payload.message_id)


        emb = discord.Embed(color=discord.Color.from_rgb(198, 120, 221))
        dc = origin.created_at.now().strftime("%Y/%m/%d %H:%M:%S")
        emb.title = f'pinned from #{origin.channel.name}'
        emb.set_author(name=origin.author.name, icon_url=origin.author.avatar_url)
        emb.add_field(name=f'sent: {dc}', value=f'[Pin Origin]({origin.jump_url})', inline=False)


        for a in origin.attachments:
            emb.add_field(name=f'msg.file: ', value=a.filename, inline=False)
            emb.add_field(name=f'msg.url', value=a.url, inline=False)
            emb.set_thumbnail(url='./FileType_Generic.png')
        #if(len(origin.attachments) == 0 and len(origin.embeds) == 0 and origin.content != ''):
        #    emb.add_field(name="message.content", value=origin.content, inline=False)
        #elif()


        #for a in origin.attachments:
        #    if(a.content_type == 'image/png'):
        #        emb.set_image(url=a.url)
        #    if('text' in a.content_type):       

        print(origin.attachments)
        print(len(origin.attachments))
        print(origin.content)
        print(origin.embeds)
        print('-------------')
        #for a in origin.attachments:
        #    emb.set_image(url=a.url)

        #print(origin.attachments[0].content_type)
        #emb.set_image(url=origin.embeds[0].image.url)

        '''
        if(len(origin.embeds) != 0):
            for current in origin.embeds:
                emb.add_field(name='embed.video', value=current.video.url, inline=True)
                emb.add_field(name='embed.desc', value=current.description, inline=True)
                emb.add_field(name='embed.title', value=current.title, inline=True)
                emb.set_thumbnail(url=current.thumbnail.url)
                emb.set_image(url=current.image.url)
        else:
            emb.add_field(name="embed.content", value=origin.content, inline=False)
        '''
        print("send file")
        await PinContentChannel.send(embed=emb)
        #await PinContentChannel.send(embed=emb)
        #msg = discord.Embed(color=discord.Colour.from_rgb(198, 120, 221))
        #dc = origin.created_at.now()
        #msg.title = f'pinned from: #{origin.channel.name}'
        #msg.set_author(name=origin.author.name, icon_url=origin.author.avatar_url)
        #msg.add_field(name=f'sent: {dc.strftime("%Y/%m/%d %H:%M:%S")}', value=f"[Pin Origin]({origin.jump_url})", inline=False)
        #for e in origin.embeds:
        #    msg.add_field(name=e.url, value=e.description, inline=False)
        #    msg.add_field(name='embed.image', value=e.image.url, inline=True)
        #    msg.add_field(name='embed.thumbnail', value=e.thumbnail.url, inline=True)
        #    msg.add_field(name='embed.video', value=e.video.url, inline=True)
        #await PinContentChannel.send(embed=msg)
        
        #await PinContentChannel.create_webhook(name="Message", avatar=origin.author.avatar)
        #print(origin)
        #await PinContentChannel.send()
        #await PinContentChannel.send(content=origin.content, embed=origin.embeds)

#region
client.run('ODE2MTAxNTA4NTQxOTcyNTMw.YD2Dwg.BB-puKouhfDtycXcV1KbDfK7dKc')
#endregion