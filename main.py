import discord
import datetime
import random
import requests
from discord import app_commands
from discord.ext import tasks
from config import TOKEN
from keep_alive import keep_alive

keep_alive()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#admin commands
#purge
@tree.command(name="purge", description="Purge messages from a channel")
@app_commands.describe(amount="The ammount of messages to purge (max 100))")
async def purge(ctx, amount: int):
    if ctx.user.guild_permissions.administrator:
        if amount > 100:
            await ctx.response.send_message("Calma lá pá! Só 100 mensagens de cada vez!", ephemeral=True)
        else:
            await ctx.channel.purge(limit=amount)
            await ctx.response.send_message(f"Purged {amount} messages!", delete_after=10)
    else:
        await ctx.response.send_message("Não és épico o suficiente para utilizar este comando!", ephemeral=True)

#kick
@tree.command(name="kick", description="Kick a user from the server")
@app_commands.describe(user="The user to kick")
async def kick(ctx, user: discord.User):
    if ctx.user.guild_permissions.administrator:
        if user.guild_permissions.administrator:
            await ctx.response.send_message("Esse utilizador é demasiado épico para ser kickado")
        else:
            await ctx.guild.kick(user)
            await ctx.response.send_message(f"{user.mention} foi kickado do servidor! Nada épico bro...")
    else:
        await ctx.response.send_message("Não és épico o suficiente para utilizar este comando!", ephemeral=True)

#ban
@tree.command(name="ban", description="Ban a user from the server")
@app_commands.describe(user="The user to ban")
async def ban(ctx, user: discord.User):
    if ctx.user.guild_permissions.administrator:
        if user.guild_permissions.administrator:
            await ctx.response.send_message("Esse utilizador é demasiado épico para ser banido")
        else:
            await ctx.guild.ban(user)
            await ctx.response.send_message(f"{user.mention} foi banido do servidor! Vai e não voltes!")
    else:
        await ctx.response.send_message("Não és épico o suficiente para utilizar este comando!", ephemeral=True)

#other commands
@tree.command(name="epic-meter", description="Quão épico és tu?")
async def epic_meter(ctx):
    value = random.randint(0,100)
    if value < 50:
        await ctx.response.send_message(f"{ctx.user.mention} és {value}% épico! Fraquinho pá, fraquinho...")
    elif value < 75:
        await ctx.response.send_message(f"{ctx.user.mention} és {value}% épico! Nada mau!")
    elif value < 90:
        await ctx.response.send_message(f"{ctx.user.mention} és {value}% épico! És mesmo épico!")
    else:
        await ctx.response.send_message(f"{ctx.user.mention} és {value}% épico! Épico demais para este mundo!")


#on user join send message to channel in a specific server
@client.event
async def on_member_join(member):
    if member.guild.id == 1149658744469340250:
        #give role
        role = discord.utils.get(member.guild.roles, name="Gente Épica")
        await member.add_roles(role)
        channel = client.get_channel(1149671217322786857)
        info_channel = client.get_channel(1149710829676134421)
        await channel.send(f"{member.mention} és Épico! Vai ao {info_channel.mention} para mais informações.", file=discord.File('assets/epico.jpeg'))

# @client.event
# async def on_ready():
#     Channel = client.get_channel(1149710829676134421)
#     embed = discord.Embed(title="Tu és Épico",
#                       description="Bem vindo ao Epicamente Épico. Tu, sim tu, tu és épico.\n\n*Para mais informações acerca do teu nível de épico consulta o nosso bot de serviço.*",
#                       colour=0x80ff00,
#                       timestamp=datetime.now())

#     embed.add_field(name="Roles",
#                 value="As seguintes roles existem:\n\n**Deus Épico** - O Deus, que é épico.\n**Super Épico** - Pessoas super épicas, que têm poderes super épicos.\n**Gente Épica** - Pessoas que são épicas.",
#                 inline=False)
#     embed.add_field(name="Game Roles",
#                 value="Gostas de jogar jogos épicos? Queres ser chateado por pessoas que também gostam de jogar jogos épicos? Reage a esta mensagem com o emoji respetivo para receberes a role do jogo épico.\n\n⚽ - Rocket League\n🔫 - Valorant\n🦸 - Overwatch 2\n\n*Não nos responsabilizamos por quantidades exorbitantes de pings que possam receber.*",
#                 inline=True)

#     embed.set_image(url="https://files.catbox.moe/bi7tvm.jpeg")

#     embed.set_footer(text="O vosso bot de serviço, Épico Bot",
#                  icon_url="https://files.catbox.moe/v63f1c.jpeg")

#     Moji = await Channel.send(embed=embed)
#     await Moji.add_reaction("⚽")
#     await Moji.add_reaction("🔫")
#     await Moji.add_reaction("🦸")

#reaction roles on specific message
@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 1149715252238364723:
        if payload.emoji.name == "⚽":
            role = discord.utils.get(payload.member.guild.roles, name="Rocket League")
            await payload.member.add_roles(role)
        elif payload.emoji.name == "🔫":
            role = discord.utils.get(payload.member.guild.roles, name="Valorant")
            await payload.member.add_roles(role)
        elif payload.emoji.name == "🦸":
            role = discord.utils.get(payload.member.guild.roles, name="Overwatch")
            await payload.member.add_roles(role)

#Start the bot
@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="música épica"))
    print("Ready!")


#Run
client.run(TOKEN)