import datetime
import discord
from config import TOKEN
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "oshi-no-ko-wednesday", description = "Is it Oshi No Ko Wednesday?")
async def wednesday(interaction):
    #if it is wednesday
    if datetime.datetime.today().weekday() == 2:
        await interaction.response.send_message("It is Oshi No Ko Wednesday!")
        #send another message
        await interaction.channel.send("https://tenor.com/view/oshi-no-ko-oshi-no-ko-wednesday-ai-hoshino-gif-1982692928935415089")
    else:
        await interaction.response.send_message("It is not Oshi No Ko Wednesday.")

@tree.command(name="next-episode", description="Time until the next episode?")
async def next_episode(interaction):
    # Get the current date and time in UTC
    current_datetime = datetime.datetime.now(datetime.timezone.utc)

    # Get the current day of the week
    current_weekday = current_datetime.weekday()

    # Calculate the number of days until the next Wednesday
    days_until_next_wednesday = (2 - current_weekday + 7) % 7

    # Set the target time as 2 PM
    target_time = datetime.time(14, 0, 0)

    # Create the target datetime by combining the next Wednesday and target time
    target_datetime = current_datetime + datetime.timedelta(days=days_until_next_wednesday)
    target_datetime = datetime.datetime.combine(target_datetime.date(), target_time, tzinfo=datetime.timezone.utc)

    # Calculate the time difference between the current datetime and the target datetime
    time_difference = target_datetime - current_datetime

    # Extract the remaining days, hours, and minutes from the time difference
    remaining_days = time_difference.days
    remaining_hours = time_difference.seconds // 3600
    remaining_minutes = (time_difference.seconds % 3600) // 60

    # Print the remaining time
    if remaining_days > 0:
        await interaction.response.send_message(f"Time remaining: {remaining_days} day(s), {remaining_hours} hour(s), and {remaining_minutes} minute(s)")
    else:
        await interaction.response.send_message(f"Time remaining: {remaining_hours} hour(s) and {remaining_minutes} minute(s)")

@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")


client.run(TOKEN)