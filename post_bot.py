from functools import partial, wraps
import discord
from discord.ext import commands
from utils import post_to_channel
from settings import JOB_CHANNEL_ID, SERVICE_CHANNEL_ID


class PostBot:
    def __init__(self, allowed_role_id, job_channel_id, service_channel_id):
        intents = discord.Intents.default()
        intents.message_content = True
        self.allowed_role_id = allowed_role_id
        self.job_channel_id = job_channel_id
        self.service_channel_id = service_channel_id
        self.bot = commands.Bot(command_prefix="/", intents=intents)
        self.bot.event(self.on_ready)
        self.add_command("postjob", PostBot.post_job)
        self.add_command("postservices", PostBot.post_services)
        self.add_command("post", PostBot.post)

    def add_command(self, name, f):
        self.bot.command(name=name)(wraps(f)(partial(f, self)))

    def run(self, token):
        self.bot.run(token)

    async def on_ready(self):
        print(f"Bot is ready. Logged in as {self.bot.user}")

    async def post_job(self, ctx, *, message: str):
        await post_to_channel(ctx, message, JOB_CHANNEL_ID, "New Job Posting")

    async def post_services(self, ctx, *, message: str):
        await post_to_channel(ctx, message, SERVICE_CHANNEL_ID, "New Service Offering")

    async def post(
        self, ctx, channel: discord.TextChannel, title: str, *, message: str
    ):
        await post_to_channel(ctx, message, channel.id, title)
