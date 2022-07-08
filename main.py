#import
import random
import discord
from discord import Guild, client
from discord.ext.commands.errors import BadArgument, MissingPermissions
from discord.ui import Button, View, view
from discord.ext import commands, tasks
import asyncio
import aiohttp
import os
import requests
from discord.ext.commands import Bot
from discord.ui.button import button
from discord_together import DiscordTogether
from dotenv import load_dotenv
import art
import pyshorteners




#client
client = commands.Bot(command_prefix=" ", case_insensitive=True)
client.remove_command("help")

@client.event
async def on_ready():
    print("Caricato configurazione da .env")
    if status == "dnd":
        await client.change_presence(activity=discord.Game(name=f"{client.user.name} | 1.0 | /invite"), status=discord.Status.dnd)
    elif status == "online":
        await client.change_presence(activity=discord.Game(name=f"{client.user.name} | 1.0 | /invite"))
    elif status == "offline":
        await client.change_presence(activity=discord.Game(name=f"{client.user.name} | 1.0 | /invite"), status=discord.Status.invisible)
    elif status == "inattivo":
        await client.change_presence(activity=discord.Game(name=f"{client.user.name} | 1.0 | /invite"), status=discord.Status.idle)
    elif status == "streaming":
        await client.change_presence(activity=discord.Streaming(name=f"{client.user.name} | 1.0 | /invite",url="https://twitch.tv/Ninja"))
    else:
        await client.change_presence(activity=discord.Game(name=f"{client.user.name} | 1.0 | /invite"))
    client.togetherControl = await DiscordTogether(token)
    art.tprint("Galbi")
    print("Online come: " + client.user.name)
    

load_dotenv()
token = os.environ['TOKEN']
clientid = os.environ['CLIENT_ID']
emcolor_r = int(os.environ['EMBED_COLOR_R'])
emcolor_g = int(os.environ['EMBED_COLOR_G'])
emcolor_b = int(os.environ['EMBED_COLOR_B'])
status= os.environ['STATUS']
caninvite= os.environ['INVITE']


#Info

@client.slash_command(description="Ottieni informazioni su questo bot")
async def info(ctx):
    embed=discord.Embed(title="**Info**", description="Informazioni su questo bot", color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
    embed.set_author(name="Galbi", icon_url="https://i.imgur.com/YeL6Nq0.png")
    embed.set_thumbnail(url="https://i.imgur.com/YeL6Nq0.png")
    embed.add_field(name="**Sviluppatore**", value="`Galbaninoh#3543`", inline=False)
    embed.add_field(name="**Versione**", value="`1.0`", inline=True)
    embed.add_field(name="**Prefisso**", value="`/`", inline=True)
    embed.add_field(name="Ping", value=f"`{client.latency*1000}`", inline=True)
    embed.set_footer(text="Fatto con ❤️ da Galbaninoh#3543")
    website=Button(label="Sito", style=discord.ButtonStyle.url, emoji="🌐",url="https://bot.galbaninoh.tech")
    view= View()
    view.add_item(website)
    await ctx.respond(f"{ctx.author.mention}",embed=embed, view=view)


#Help

@client.slash_command(description="Guarda tutti i comandi del Bot!")
async def help(ctx):
    embed=discord.Embed(title="Comandi",color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
    embed.set_author(name="Galbi", icon_url="https://i.imgur.com/YeL6Nq0.png")
    embed.add_field(name="/info", value="Ottieni informazioni su questo bot", inline=False)
    embed.add_field(name="/help", value="Guarda tutti i comandi del Bot", inline=False)
    embed.add_field(name="/youtube", value="Avvia una sessione di Youtube Watch Together", inline=False)
    embed.add_field(name="/invite", value="Invita questo bot al tuo discord!", inline=False)
    embed.add_field(name="/ban", value="Banna un membro dal server", inline=False)
    embed.add_field(name="/unban", value="Sbanna un membro dal server", inline=False)
    embed.add_field(name="/clear", value="Elimina un numero specificato di messaggi", inline=False)
    embed.add_field(name="/meme", value="Manda un Meme", inline=False)
    embed.add_field(name="/eightball", value="Fai una domanda e il bot ti dara una risposta", inline=False)
    embed.add_field(name="/shortner", value="Accorcia un url con pochi clic", inline=False)
    embed.add_field(name="/gay", value="Gay Overlay", inline=False)
    embed.add_field(name="/triggered", value="Triggered Overlay", inline=False)
    embed.add_field(name="/comunism", value="Comunism Overlay", inline=False)
    embed.add_field(name="/passed", value="Mission Passed Overlay", inline=False)
    embed.add_field(name="/wasted", value="Wasted Overlay", inline=False)
    await ctx.respond(f"{ctx.author.mention}",embed=embed)


#comandi

#Youtube Watch Together
@client.slash_command(description="Avvia una sessione di youtube")
async def youtube(ctx):
    voice_state = ctx.author.voice
    if voice_state is None:
        embed=discord.Embed(title="Errore", description="Devi essere in un canale per usare questo comando",color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
        await ctx.respond(embed=embed)
    else:
        sessione = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        embed=discord.Embed(title="Sessione Creata!", description="Clicca il bottone per entrare",color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
        tasto=Button(label="Entra nella sessione", style=discord.ButtonStyle.url, emoji="▶",url=sessione)
        view= View()
        view.add_item(tasto)
        await ctx.respond(embed=embed,view=view)

##invita
@client.slash_command(description="Invita questo bot al tuo discord!")
async def invite(ctx):
    if caninvite == True or "true":
        embed=discord.Embed(title="Invita il bot", description="Clicca il bottone qua sotto per invitare il bot al tuo discord",color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
        tasto=Button(label="Invita il bot", style=discord.ButtonStyle.url, emoji="🎫",url=f"https://discord.com/oauth2/authorize?client_id={clientid}&permissions=8&scope=applications.commands%20bot")
        view= View()
        view.add_item(tasto)
        await ctx.respond(embed=embed,view=view)
    else:
        embed=discord.Embed(title="Errore", description="Questo comando è disattivato!",color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
        await ctx.respond(embed=embed)

#Say
@client.slash_command(description="Fai dire al bot una frase a tua scelta!")
async def say(ctx, *, frase):
    await ctx.respond(frase)

#kick
@client.slash_command(description="Espelli un membro dal server")
@commands.has_permissions(kick_members = True)
async def kick(ctx,membro : discord.Member,*,motivazione= "Nessuna ragione data"):
    embed=discord.Embed(title="Kick 🔨", description=f"**{ctx.author.name}** ha espulso **{membro}**",color = discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
    embed.add_field(name="Motivazione", value=f"{motivazione}", inline=False)
    try:
        await membro.send(":hammer: Sei stato espulso dal server, Motivo:"+motivazione)
    except:
        print(f"{membro} ha i dm chiusi")
    await ctx.respond(embed = embed)
    await membro.kick(reason=motivazione)

#ban
@client.slash_command(description="Banna un membro dal server")
@commands.has_permissions(ban_members = True)
async def ban(ctx,membro : discord.Member,*,motivazione= "Nessuna ragione data"):
    embed=discord.Embed(title="Ban 🔨", description=f"**{ctx.author.name}** ha bannato **{membro}**",color = discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
    embed.add_field(name="Motivazione", value=f"{motivazione}", inline=False)
    try:
        await membro.send(":hammer: Sei stato bannato dal server, Motivo:"+motivazione)
    except:
        print(f"{membro} ha i dm chiusi")
    await ctx.respond(embed = embed)
    await membro.ban(reason=motivazione)

#unban
@client.slash_command(description="Sbanna un membro dal server")
@commands.has_permissions(ban_members=True)
async def unban(ctx,membro : discord.Member,*,motivazione= "Nessuna ragione data"):
    try:
        await ctx.guild.unban(membro,reason=motivazione)     
        embed=discord.Embed(title="Unban", description=f"**{ctx.author.name}** ha sbannato **{membro}**",color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
        embed.add_field(name="Motivazione", value=f"{motivazione}", inline=True)
        await ctx.respond(embed=embed)
    except:
        embed=discord.Embed(title="Errore", description=f"**{membro}** non è bannato!",color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
        await ctx.respond(embed=embed)

#Clear

@client.slash_command(pass_context=True, description="Elimina un numero specificato di messaggi")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, numeromessaggi: int):
    await ctx.channel.purge(limit=numeromessaggi)
    embed=discord.Embed(title="**Clear**", description=f"Ho eliminato {numeromessaggi} messaggi!" , color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
    await ctx.respond(embed=embed)



#meme
@client.slash_command(description="Manda un Meme")
async def meme(ctx):
    embed = discord.Embed(title="Ecco un meme 🤨", description="",color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/memesITA/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.respond(embed=embed)

#8ball
@client.slash_command(aliases=['8ball'], description="Fai una domanda e il bot ti dara una risposta")
async def eightball(ctx, *,domanda):
    risposte = ["È certo.",
                "È decisamente così.",
                "Senza dubbio.",
                "Sì, sicuramente.",
                "Puoi fare affidamento su di esso.",
                "Per come la vedo io, sì.",
                "Più probabilmente.",
                "Prospettive buone.",
                "Sì.",
                "I segni indicano sì.",
                "Rispondi confuso, riprova.",
                "Chiedi un'altra volta più tardi.",
                "Meglio non dirtelo ora.",
                "Non posso prevedere ora.",
                "Concentrati e chiedi di nuovo.",
                "Non ci contare.",
                "La mia risposta è no.",
                "Le mie fonti dicono di no.",
                "Prospettive non così buone.",
                "Molto dubbioso."]
    embed=discord.Embed(title="8ball",color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
    embed.add_field(name="Domanda", value=f"{domanda}", inline=False)
    embed.add_field(name="Risposta", value=f"{random.choice(risposte)}", inline=False)
    await ctx.respond(embed=embed)

#Url shortner

@client.slash_command(description="Accorcia un url con pochi clic")
async def shortner(ctx, link):
    if link.startswith('http://'):
        shortner=pyshorteners.Shortener()
        short= shortner.tinyurl.short(link)
        embed=discord.Embed(title="**Url Accorciato!**", color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
        embed.add_field(name="Url Originale", value=link, inline=False)
        embed.add_field(name="Url Accorciato", value=short, inline=False)
        await ctx.respond(embed=embed)
    elif link.startswith('https://'):
        shortner=pyshorteners.Shortener()
        short= shortner.tinyurl.short(link)
        embed=discord.Embed(title="**Url Accorciato!**", color=discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
        embed.add_field(name="Url Originale", value=link, inline=False)
        embed.add_field(name="Url Accorciato", value=short, inline=False)
        await ctx.respond(embed=embed)
    else:
        embed=discord.Embed(title="Errore", description=":red_square: **Link non valido!** Ricordati di inserire `http://` o `https://`",color= discord.Color.from_rgb(emcolor_r,emcolor_g,emcolor_b))
        await ctx.send(embed=embed)

#IMG commands

@client.slash_command(description="Gay Overlay")
async def gay(ctx,membro : discord.Member=None):
    if membro is None:
        avatarutente=ctx.author.avatar
        URL = f'https://some-random-api.ml/canvas/gay?avatar={avatarutente}'
        resp = requests.get(URL)
        if resp.status_code == 200:
            open('gay.png', 'wb').write(resp.content)
            await ctx.respond(file=discord.File('gay.png'))
            os.remove("gay.png")
        else:
            ctx.respond("**Errore API**")
    else:
        avatarutente=membro.avatar
        URL = f'https://some-random-api.ml/canvas/gay?avatar={avatarutente}'
        resp = requests.get(URL)
        if resp.status_code == 200:
            open('gay.png', 'wb').write(resp.content)
            await ctx.respond(file=discord.File('gay.png'))
            os.remove("gay.png")
        else:
            ctx.respond("**Errore API**")

@client.slash_command(description="Triggered Overlay")
async def triggered(ctx,membro : discord.Member=None):
    if membro is None:
        avatarutente=ctx.author.avatar
        URL = f'https://some-random-api.ml/canvas/triggered?avatar={avatarutente}'
        resp = requests.get(URL)
        if resp.status_code == 200:
            open('triggered.png', 'wb').write(resp.content)
            await ctx.respond(file=discord.File('triggered.png'))
            os.remove("triggered.png")
        else:
            ctx.respond("**Errore API**")
    else:
        avatarutente=membro.avatar
        URL = f'https://some-random-api.ml/canvas/triggered?avatar={avatarutente}'
        resp = requests.get(URL)
        if resp.status_code == 200:
            open('triggered.png', 'wb').write(resp.content)
            await ctx.respond(file=discord.File('triggered.png'))
            os.remove("triggered.png")
        else:
            ctx.respond("**Errore API**")

@client.slash_command(description="Comunism Overlay")
async def comunism(ctx,membro : discord.Member=None):
    if membro is None:
        avatarutente=ctx.author.avatar
        URL = f'https://some-random-api.ml/canvas/comrade?avatar={avatarutente}'
        resp = requests.get(URL)
        if resp.status_code == 200:
            open('comunism.png', 'wb').write(resp.content)
            await ctx.respond(file=discord.File('comunism.png'))
            os.remove("comunism.png")
        else:
            ctx.respond("**Errore API**")
    else:
        avatarutente=membro.avatar
        URL = f'https://some-random-api.ml/canvas/comrade?avatar={avatarutente}'
        resp = requests.get(URL)
        if resp.status_code == 200:
            open('comunism.png', 'wb').write(resp.content)
            await ctx.respond(file=discord.File('comunism.png'))
            os.remove("comunism.png")
        else:
            ctx.respond("**Errore API**")

@client.slash_command(description="Mission Passed Overlay")
async def passed(ctx,membro : discord.Member=None):
    if membro is None:
        avatarutente=ctx.author.avatar
        URL = f'https://some-random-api.ml/canvas/passed?avatar={avatarutente}'
        resp = requests.get(URL)
        if resp.status_code == 200:
            open('passed.png', 'wb').write(resp.content)
            await ctx.respond(file=discord.File('passed.png'))
            os.remove("passed.png")
        else:
            ctx.respond("**Errore API**")
    else:
        avatarutente=membro.avatar
        URL = f'https://some-random-api.ml/canvas/passed?avatar={avatarutente}'
        resp = requests.get(URL)
        if resp.status_code == 200:
            open('passed.png', 'wb').write(resp.content)
            await ctx.respond(file=discord.File('passed.png'))
            os.remove("passed.png")
        else:
            ctx.respond("**Errore API**")

@client.slash_command(description="Wasted Overlay")
async def wasted(ctx,membro : discord.Member=None):
    if membro is None:
        avatarutente=ctx.author.avatar
        URL = f'https://some-random-api.ml/canvas/wasted?avatar={avatarutente}'
        resp = requests.get(URL)
        if resp.status_code == 200:
            open('wasted.png', 'wb').write(resp.content)
            await ctx.respond(file=discord.File('wasted.png'))
            os.remove("wasted.png")
        else:
            ctx.respond("**Errore API**")
    else:
        avatarutente=membro.avatar
        URL = f'https://some-random-api.ml/canvas/wasted?avatar={avatarutente}'
        resp = requests.get(URL)
        if resp.status_code == 200:
            open('wasted.png', 'wb').write(resp.content)
            await ctx.respond(file=discord.File('wasted.png'))
            os.remove("wasted.png")
        else:
            ctx.respond("**Errore API**")

client.run(token)