# from functools import partial
import discord
from discord.ext import commands
from commands import post_job, post_services, post


class PostBot:
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix="/", intents=intents)
        self.bot.add_listener(self.on_ready, "on_ready")
        self.bot.add_command(post_job)
        self.bot.add_command(post_services)
        self.bot.add_command(post)

    def run(self, token):
        self.bot.run(token)

    async def on_ready(self):
        print(f"Bot is ready. Logged in as {self.bot.user}")
