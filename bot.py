import discord
from discord.ext import commands
import discord.utils
from utils import post_to_channel
from webserver import keep_alive
from settings import TOKEN, JOB_CHANNEL_ID, SERVICE_CHANNEL_ID

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")


@bot.command(name="postjob")
async def post_job(ctx, *, message: str):
    await post_to_channel(ctx, message, JOB_CHANNEL_ID, "New Job Posting")


@bot.command(name="postservices")
async def post_services(ctx, *, message: str):
    await post_to_channel(ctx, message, SERVICE_CHANNEL_ID, "New Service Offering")


@bot.command(name="post")
async def post(ctx, channel: discord.TextChannel, title: str, *, message: str):
    await post_to_channel(ctx, message, channel.id, title)


# Keep the web server alive
keep_alive()

if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN environment variable is not set.")
