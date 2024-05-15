import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import traceback
from webserver import keep_alive  # Import the keep_alive function

# Load environment variables from .env file
load_dotenv()

# Use the environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
ALLOWED_ROLE_ID_str = os.getenv('ALLOWED_ROLE_ID')
TARGET_CHANNEL_ID_str = os.getenv('TARGET_CHANNEL_ID')

if TARGET_CHANNEL_ID_str is not None:
    TARGET_CHANNEL_ID = int(TARGET_CHANNEL_ID_str)
else:
    print("Error: TARGET_CHANNEL_ID environment variable is not set.")
    exit()

if ALLOWED_ROLE_ID_str is not None:
    ALLOWED_ROLE_ID = int(ALLOWED_ROLE_ID_str)
else:
    print("Error: ALLOWED_ROLE_ID environment variable is not set.")
    exit()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')


@bot.command(name='post')
async def post(ctx, *, message: str):
    try:
        # Check if the author has the allowed role ID
        role = discord.utils.get(ctx.guild.roles, id=ALLOWED_ROLE_ID)
        if role in ctx.author.roles:
            channel = bot.get_channel(TARGET_CHANNEL_ID)
            if channel:
                await channel.send(message)
                await ctx.send(f'Message sent to {channel.mention}')
            else:
                await ctx.send('Target channel not found.')
        else:
            await ctx.send('You do not have the required role to use this command.')
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        await ctx.send('An error occurred while trying to execute the command.')


# Keep the web server alive
keep_alive()

if TOKEN is not None:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN environment variable is not set.")
