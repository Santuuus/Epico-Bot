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

#Commands
#Is it Jujutsu Kaisen?
@tree.command(name = "jjk-thursday", description = "Is it Jujutsu Kaisen Thursday??")
async def wednesday(interaction):
    #if it is wednesday
    if datetime.datetime.today().weekday() == 2:
        await interaction.response.send_message("It is JJK Thursday!")
        #send another message
        await interaction.channel.send("https://tenor.com/view/jujutsu-thursday-jujutsu-jujutsu-kaisen-jujutsu-kaisen-thursday-gojo-gif-13734841367417869316")
    else:
        await interaction.response.send_message("It is not JJK Thursday.")
       # await interaction.channel.send("https://tenor.com/view/ruby-hoshino-oshi-no-ko-anime-tears-crying-gif-16026934856871427303")

#Time until next Jujutsu Kaisen episode
@tree.command(name="next-episode", description="Time until the next episode?")
async def next_episode(interaction):
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Get the current day of the week (Monday is 0 and Sunday is 6)
    current_weekday = current_datetime.weekday()

    # Calculate the number of days until the next Thursday
    days_until_next_thursday = (3 - current_weekday + 7) % 7

    # Set the target time as 3 PM
    target_time = datetime.time(15, 56, 0)
    
    #Get Unix timestamp for next wednesday at 3 PM
    target_timestamp = datetime.datetime.combine(current_datetime.date() + datetime.timedelta(days=days_until_next_thursday), target_time).timestamp()

    #if it is wednesday and past 3 PM
    if current_weekday == 3 and current_datetime.time() >= target_time:
        # Add 7 days to the timestamp
        target_timestamp += 7 * 24 * 60 * 60
    
    #if it is wednesday between 3 PM and 4 PM
    if current_weekday == 3 and current_datetime.time() >= datetime.time(15, 56, 0) and current_datetime.time() < datetime.time(18, 56, 0):
        await interaction.response.send_message("# Episode out now!")
    else:
        # Print the remaining time
        await interaction.response.send_message(f"Next Jujutsu Kaisen episode: <t:{int(target_timestamp)}:R>")

#Live ROY reaction
@tree.command(name="roy", description="Live ROY reaction")
async def roy(interaction):
    await interaction.response.send_message(file=discord.File("assets/royreaction.png"))

#Quaso
@tree.command(name="quaso", description="QUASO")
async def roy(interaction):
    await interaction.response.send_message(file=discord.File("assets/quaso.png"))

#Bot uptime
@tree.command(name="uptime", description="Bot uptime")
async def uptime(interaction):
    if interaction.user.id == 282662959241756683:
        await interaction.response.send_message("Uptime: maior que o do <@1099352698572243007>")
    else:
        #calculate uptime
        uptime = datetime.datetime.now() - start_time
        #send message
        if uptime.days < 1:
            await interaction.response.send_message(f"Uptime: {uptime.seconds // 3600} hour(s), {uptime.seconds % 3600 // 60} minute(s) and {uptime.seconds % 3600 % 60} second(s)")
        else:
            await interaction.response.send_message(f"Uptime: {uptime.days} day(s), {uptime.seconds // 3600} hour(s), {uptime.seconds % 3600 // 60} minute(s) and {uptime.seconds % 3600 % 60} second(s)")

#Get Real
@tree.command(name="get-real", description="Get Real")
async def getReal(interaction):
    await interaction.response.send_message("https://tenor.com/view/oshi-no-ko-anime-ai-hoshino-idol-gif-8712266706126317077")

#Error handling
@tree.error
async def on_error(interaction, error):
    if isinstance(error, app_commands.errors.CommandOnCooldown):
        await interaction.response.send_message(f"Command on cooldown. Try again in {error.retry_after:.2f} seconds.", ephemeral=True)
    else:
        raise error


#Start the bot
@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Ryo playing Bass"))
    global start_time 
    start_time = datetime.datetime.now()
    print("Ready!")

#Responds to mentions
@client.event
async def on_message(message):
    if client.user.mentioned_in(message) and message.author.id != 1099352698572243007:
        if message.mention_everyone:
            return
        await message.reply("Oshi No Ko Reference")
    elif message.author.id == 1099352698572243007:
        #if message contains "precisas de ajuda"
        if "precisas de ajuda" in message.content.lower():
            await message.reply("Preciso que te cales <a:peperonimo:1101073938039177350>", mention_author=False)
        if "stay malding bozo" in message.content.lower():
            await message.reply("Mald deez nuts.", mention_author=False)
     

#Run
client.run(TOKEN)