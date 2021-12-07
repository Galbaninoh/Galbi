#import
from logging import log
from typing import AsyncContextManager
import random
import discord
from discord import client
from discord.ext.commands.errors import BadArgument, MissingPermissions
from discord.ui import Button, View, view
from discord.ext import commands, tasks
import asyncio
import aiohttp
import os
from discord.ext.commands import Bot
from discord.ui.button import button
import discord_together
from discord_together import DiscordTogether
from dotenv import load_dotenv


#.env
load_dotenv()
token = os.environ['TOKEN']
#client
client = commands.Bot(command_prefix=" ", case_insensitive=True)
client.remove_command("help")

###Info

@client.slash_command(description="Vedi diverse informazioni sul bot!")
async def info(ctx):
    embed=discord.Embed(title="**Informazioni sul Bot**", color=ctx.author.color)
    embed.set_author(name="Galbi Bot V2.0 By Galbaninoh", url="https://github.com/Galbaninoh/GalbiBot", icon_url="https://cdn.discordapp.com/avatars/532264302300889088/2de1cf0d3e414f574cd78ba92e8884d7.webp?size=24")
    embed.add_field(name="Versione", value="2.0", inline=False)
    embed.add_field(name="Autore", value="Galbaninoh", inline=True)
    embed.add_field(name="Prefix", value=f"`/`", inline=False)
    latenza=client.latency*1000
    embed.add_field(name="Ping", value=f"`{latenza}ms`", inline=True)
    tasto=Button(label="Github", style=discord.ButtonStyle.url, emoji="💻",url="https://github.com/Galbaninoh/GalbiBot")
    view= View()
    view.add_item(tasto)
    await ctx.respond(embed=embed, view=view)


###Help

@client.slash_command(description="Guarda tutti i comandi del Bot!")
async def help(ctx):
    embed=discord.Embed(title="**Help**", color=0xff0040)
    embed.add_field(name="`/Help <Comando>`", value="Da informazioni su un comando", inline=False)
    embed.add_field(name="`/ban <membro> <motivo>`", value="Banna un membro dal server", inline=False)
    embed.add_field(name="`/unban <membro> <motivo>`", value="Sbanna un membro dal server", inline=False)
    embed.add_field(name="`/clear <NumeroDiMessaggi>`", value="Elimina un numero specificato di messaggi", inline=False)
    embed.add_field(name="`/youtube`", value="Avvia una sessione di Youtube Watch Together", inline=False)
    embed.add_field(name="`/meme`", value="Invia un meme", inline=False)
    embed.add_field(name="`/say`", value="Fai dire una frase a tua scelta al bot", inline=False)
    embed.add_field(name="`/eightball`", value="Fai una domanda e il bot darà la risposta", inline=False)
    embed.add_field(name="`/invite`", value="Invia il link per invitare il bot al tuo discord", inline=False)
    embed.add_field(name="`/info`", value="Ricevi diverse informazioni riguardanti al bot", inline=False)
    await ctx.respond(embed=embed)


##comandi

#Youtube Watch Together
@client.slash_command(description="Avvia una sessione di youtube, preparati dei 🍿 e goditi la serata!")
async def youtube(ctx):
    voice_state = ctx.author.voice
    if voice_state is None:
        return await ctx.respond('Devi essere in un canale vocale per eseguire questo comando')
    sessione = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    tasto=Button(label="Entra nella sessione", style=discord.ButtonStyle.url, emoji="▶",url=sessione)
    view= View()
    view.add_item(tasto)
    await ctx.respond('**Sessione creata!**',view=view)

##invita

@client.slash_command(description="Invita questo fantastico bot al tuo discord!")
async def invite(ctx):
    tasto=Button(label="INVITA IL BOT!", style=discord.ButtonStyle.url, emoji="🎫",url="https://discord.com/oauth2/authorize?client_id=856409675129815050&permissions=8&scope=applications.commands%20bot")
    view= View()
    view.add_item(tasto)
    await ctx.respond('**Ecco qua il tasto per invitare il bot!**',view=view)

#Say

@client.slash_command(description="Fai dire al bot una frase a tua scelta!")
async def say(ctx, *, frase):
    await ctx.respond(frase)

#kick
@client.slash_command(description="Espelli un membro dal server")
@commands.has_permissions(kick_members = True)
async def kick(ctx,utente : discord.Member,*,motivazione= "Nessuna ragione data"):
    embed = discord.Embed(title = "**Kick**", description = " ",color = ctx.author.color )
    embed.add_field(name = "", value = (f":green_square: {utente} è stato kickato dal server!,Motivazione: " +motivazione))
    try:
        await utente.respond(":confused: Sei stato kickato dal server, Motivo:"+motivazione)
    except:
        await ctx.respond("Il membro ha i dm chiusi,lo Espello senza inviare un messaggio in Dm")
    await ctx.respond(embed = embed)
    await utente.kick(reason=motivazione)

#ban
@client.slash_command(description="Banna un membro dal server")
@commands.has_permissions(ban_members = True)
async def ban(ctx,membro : discord.Member,*,motivazione= "Nessuna ragione data"):
    bane = discord.Embed(title = "Ban", description = " ",color = ctx.author.color )
    bane.add_field(name = "**Informazioni**", value = (f":green_square: {membro} è stato bannato dal server!,Motivazione: " +motivazione))
    try:
        await membro.respond(":hammer: Sei stato bannato dal server, Motivo:"+motivazione)
    except:
        await ctx.respond("Il membro ha i dm chiusi, proverò comunque a bannarlo")
    await ctx.respond(embed = bane)
    await membro.ban(reason=motivazione)

#unban
@client.slash_command(description="Sbanna un membro dal server")
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,membro):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = membro.split('#')
    for banned_entry in banned_users:
        user = banned_entry.user
        if(user.name, user.discriminator)==(member_name,member_disc):
            await ctx.guild.unban(user)
            await ctx.respond(member_name + " **è stato sbannato!**")
            return
    await ctx.respond(membro+" **non è stato trovato**")

#Clear

@client.slash_command(pass_context=True, description="Elimina un numero specificato di messaggi")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, numeromessaggi: int):
    await ctx.channel.purge(limit=numeromessaggi)
    embed=discord.Embed(title="**Clear**", description=f"Ho ripulito la chat da {numeromessaggi} messaggi!" , color=0x00ff2a)
    await ctx.respond(embed=embed)



#meme
@client.slash_command(description="Manda un Meme")
async def meme(ctx):
    embed = discord.Embed(title="Ecco un bel meme 🤨", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/memesITA/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.respond(embed=embed)

#8ball
@client.slash_command(aliases=['8ball'], description="Fai una domanda e il bot ti dara una risposta! Magik vero?")
async def eightball(ctx, *,domanda):
    responses = ["È certo.",
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
    await ctx.respond(f':8ball: Domanda: {domanda}\n:8ball: Risposta: {random.choice(responses)}')

#On command error

@client.event
async def on_error(ctx, error):
    if isinstance(error, BadArgument):
        embed=discord.Embed(title="**Errore!**", description="**Non hai il permesso di eseguire questo comando!** 🛑", color=0xf00000)
        await ctx.send(embed=embed)
    elif isinstance(error, MissingPermissions):
        embed=discord.Embed(title="**Errore!**", description="**La sintassi non è corretta!** 🛑", color=0xf00000)
        await ctx.send(embed=embed)
    else:
        raise error


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"GalbiBot | Test"))
    print('GalbiBot by Galbaninoh')
    print('------------')
    print('Bot pronto come')
    print(client.user.name)
    print('------------')
    client.togetherControl = await DiscordTogether(token)

client.run(token)