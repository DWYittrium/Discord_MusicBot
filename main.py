# Import necessary libraries
import discord
from discord.ext import commands
import yt_dlp
import asyncio

# Define discord bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# FFMPEG and YDL options
FFMPEG_OPTIONS = {'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}

class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
        
    @commands.command()
    async def play(self, ctx, *, search):
        """Play a song from YouTube"""
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("You are not in a voice channel!")
        if not ctx.voice_client:
            await voice_channel.connect()
        
        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                url = info['url']
                title = info['title']
                self.queue.append((url, title))
                await ctx.send(f'Added to queue: **{title}**')
        
        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

    @commands.command()
    async def skip(self, ctx):
        """Skip the currently playing song"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Song skipped...")
        else:
            await ctx.send("No song is currently playing.")
            

# Initialize the bot with a command prefix and intents
client = commands.Bot(command_prefix="!", intents=intents)

async def main():
    """Main function to start the bot"""
    await client.add_cog(MusicBot(client))
    await client.start('TOKEN_KEY')  # Replace 'TOKEN_KEY' with your own discord token key

# Run the bot
asyncio.run(main())
