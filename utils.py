import traceback
import discord
import discord.utils
from discord.ext import commands
from settings import ALLOWED_ROLE_ID


def make_default_embed(title: str, message: str, footer: str) -> discord.Embed:
    """
    Produces an embed with the default presentation.

    Arguments:
        title (str): Title for the embed.
        message (str): Message for the main body of the embed.
        footer (str): Text for the footer of the embed.

    Returns:
        discord.Embed: An embed with the default template and the given content.
    """
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
        channel = ctx.guild.get_channel(channel_id)
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
