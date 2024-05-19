from webserver import keep_alive
from settings import TOKEN
from post_bot import PostBot

# Keep the web server alive
keep_alive()

if TOKEN:
    bot = PostBot()
    bot.run(TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN environment variable is not set.")
