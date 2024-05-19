import discord
from discord.ext import commands
import discord.utils
from dotenv import load_dotenv
import os
import traceback
from webserver import keep_alive  # Import the keep_alive function

# Load environment variables from .env file
load_dotenv()

# Use the environment variables
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
ALLOWED_ROLE_ID_str = os.getenv("ALLOWED_ROLE_ID")
JOB_CHANNEL_ID_str = os.getenv("JOB_CHANNEL_ID")  # Channel ID for job postings
SERVICE_CHANNEL_ID_str = os.getenv(
    "SERVICE_CHANNEL_ID"
)  # Channel ID for service postings

# Convert environment variables to integers
ALLOWED_ROLE_ID = int(ALLOWED_ROLE_ID_str) if ALLOWED_ROLE_ID_str else None
JOB_CHANNEL_ID = int(JOB_CHANNEL_ID_str) if JOB_CHANNEL_ID_str else None
SERVICE_CHANNEL_ID = int(SERVICE_CHANNEL_ID_str) if SERVICE_CHANNEL_ID_str else None

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


def make_default_embed(title: str, message: str, footer: str) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=message,
        color=0xFFD700,  # Gold color for the embed border
    )
    # Add a footer to the embed
    embed.set_footer(text=footer)
    return embed


async def post_to_channel(
    ctx: commands.Context, message: str, channel_id: int, title: str
):
    """
    Posts given message with given title to channel with given id.

    Arguments:
        ctx (discord.ext.commands.Context): Context under which the command was invoked.
        message (str): Message to be sent.
        channel_id (int): ID of the channel to which the message will be sent.
        title (str): Title of the embed to put in the message.
    """
    try:
        # Check if the author has the allowed role ID
        role = discord.utils.get(ctx.guild.roles, id=ALLOWED_ROLE_ID)
        if role not in ctx.author.roles:
            await ctx.send("You do not have the required role to use this command.")
            return
        # Get channel and confirm that it exists
        channel = bot.get_channel(channel_id)
        if not channel:
            await ctx.send("Target channel not found.")
        # Send embed and delete original command message
        embed = make_default_embed(title, message, f"- {ctx.author.display_name}")
        await channel.send(embed=embed)
        await ctx.message.delete()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()
        await ctx.send("An error occurred while trying to execute the command.")


# Keep the web server alive
keep_alive()

if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN environment variable is not set.")
