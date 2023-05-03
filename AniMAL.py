import discord
import interactions
import requests

intents = discord.Intents.all
bot = interactions.Client(token="MTEwMzMxODczMzMxMDY2ODgyMA.GE-o4J.n7xFXzUj1jhHZZWXrlwB-_D3NliWD7ZIZdqxeQ")

@bot.command(name="update_mal_anime", description="Update an anime on your list.", options=[
    {
        "name": "username",
        "description": "The username of you MAL account.",
        "type": 3,
        "required": True
    },
    {
        "name": "password",
        "description": "The password of you MAL account.",
        "type": 3,
        "required": True
    },
    {
        "name": "name",
        "description": "The name of the anime to update.",
        "type": 3,
        "required": True
    },
    {
        "name": "status",
        "description": "The status of the anime (watching, completed, on_hold, dropped, plan_to_watch).",
        "type": 3,
        "required": True,
        "choices": [
            {
                "name": "Watching",
                "value": "watching"
            },
            {
                "name": "Completed",
                "value": "completed"
            },
            {
                "name": "On Hold",
                "value": "on_hold"
            },
            {
                "name": "Dropped",
                "value": "dropped"
            },
            {
                "name": "Plan to Watch",
                "value": "plan_to_watch"
            }
        ]
    },
    {
        "name": "episodes",
        "description": "The number of episodes you've watched (optional).",
        "type": 4,
        "required": False
    },
    {
        "name": "rating",
        "description": "Your rating for the anime (1-10, optional).",
        "type": 4,
        "required": False
    }
])
async def update_anime(ctx: interactions.CommandContext,username: str, password: str, name: str, status: str, episodes: int = None, rating: int = None):
    # Call a function to update the anime on the user's list
    success = update_anime_list(username, password, name, status, episodes, rating)
    if success:
        await ctx.send(f"{name} has been updated on your list!")
    else:
        await ctx.send(f"Failed to update {name} on your list.")

def update_anime_list(username, password, name, status, episodes=None, rating=None):
    # Get the anime data from the MAL and Anilist APIs
    mal_anime_data = get_mal_anime_data(name)

    # Update the anime data with the user's input
    mal_data = {
        "status": status
    }
    if episodes:
        mal_data["num_watched_episodes"] = episodes
    if rating:
        mal_data["score"] = rating
    success = update_mal_anime(mal_anime_data["mal_id"], mal_data, username, password)

    if not success:
        return False
    
    return True

import requests

def get_mal_anime_data(name):
    # Search for the anime on MAL
    url = f"https://api.jikan.moe/v4/anime?q={name}&page=1"
    response = requests.get(url)
    data = response.json()
    results = data["data"]
    if not results:
        return None
    anime_data = results[0]
    mal_id = anime_data["mal_id"]
    print(mal_id)
    return anime_data

def update_mal_anime(mal_id, data, username, password):
    url = f"https://api.myanimelist.net/v2/anime/{mal_id}/my_list_status"

    response = requests.patch(url, data=data, auth=(username, password))

    if response.status_code == 200:
        return True
    return False

bot.start()