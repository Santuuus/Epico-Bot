import datetime
import discord
import schedule
from config import TOKEN
from discord import app_commands
from discord.ext import tasks

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

#Is it Oshi No Ko Wednesday?
@tree.command(name = "oshi-no-ko-wednesday", description = "Is it Oshi No Ko Wednesday?")
async def wednesday(interaction):
    #if it is wednesday
    if datetime.datetime.today().weekday() == 2:
        await interaction.response.send_message("It is Oshi No Ko Wednesday!")
        #send another message
        await interaction.channel.send("https://tenor.com/view/oshi-no-ko-oshi-no-ko-wednesday-ai-hoshino-gif-1982692928935415089")
    else:
        await interaction.response.send_message("It is not Oshi No Ko Wednesday.")

#Time until next Oshi No Ko episode
@tree.command(name="next-episode", description="Time until the next episode?")
async def next_episode(interaction):
    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Get the current day of the week (Monday is 0 and Sunday is 6)
    current_weekday = current_datetime.weekday()

    # Calculate the number of days until the next Wednesday
    days_until_next_wednesday = (2 - current_weekday + 7) % 7

    # Set the target time as 3 PM
    target_time = datetime.time(15, 0, 0)

    # Check if the current day is Wednesday and it's already past 3 PM
    if current_weekday == 2 and current_datetime.time() > target_time:
        # Add 7 days to find the next Wednesday
        days_until_next_wednesday += 7

    # Create the target datetime by combining the next Wednesday and target time
    next_wednesday = current_datetime + datetime.timedelta(days=days_until_next_wednesday)
    target_datetime = datetime.datetime.combine(next_wednesday.date(), target_time)

    # Calculate the time difference between the current datetime and the target datetime
    time_difference = target_datetime - current_datetime

    # Extract the remaining days, hours, and minutes from the time difference
    remaining_days = time_difference.days
    remaining_seconds = time_difference.seconds
    remaining_hours = remaining_seconds // 3600
    remaining_minutes = (remaining_seconds % 3600) // 60

    # Print the remaining time
    if remaining_days > 0:
        await interaction.response.send_message(f"Time remaining: {remaining_days} day(s), {remaining_hours} hour(s), and {remaining_minutes} minute(s)")
    else:
        await interaction.responde.send_message(f"Time remaining: {remaining_hours} hour(s) and {remaining_minutes} minute(s)")

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


client.run(TOKEN)