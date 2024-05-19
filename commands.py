import discord
from discord.ext import commands
from utils import post_to_channel
from settings import JOB_CHANNEL_ID, SERVICE_CHANNEL_ID


@commands.command(name="postjob")
async def post_job(ctx, *, message: str):
    await post_to_channel(ctx, message, JOB_CHANNEL_ID, "New Job Posting")


@commands.command(name="postservices")
async def post_services(ctx, *, message: str):
    await post_to_channel(ctx, message, SERVICE_CHANNEL_ID, "New Service Offering")


@commands.command(name="post")
async def post(ctx, channel: discord.TextChannel, title: str, *, message: str):
    await post_to_channel(ctx, message, channel.id, title)
