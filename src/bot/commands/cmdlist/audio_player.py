import youtube_dl
import discord
import youtube_search

class AudioPlayer:
    def __init__(self):
        self.ytdl = youtube_dl.YoutubeDL({})
        self.connected_guilds = {}

    async def play(self, message, parameters):
        """guild_id = message.guild.id
        if self.connected_guilds.has_key(guild_id):
            pass
        else:
            voice_channel = await message.author.voice.channel.connect()
            self.connected_guilds[guild_id] = voice_channel"""
        """if not self.voice_channel:
            self.voice_channel = await message.author.voice.channel.connect()
        else:
            await self.voice_channel.disconnect()
            self.voice_channel = await message.author.voice.channel.connect()"""
        print(parameters["search"])
        results = youtube_search.YoutubeSearch(parameters["search"][0], max_results=5).to_dict()
        url = "https://www.youtube.com" + results[0]["url_suffix"]
        info = self.ytdl.extract_info(url, download=False)

        vc = await message.author.voice.channel.connect()
        vc.play(discord.FFmpegPCMAudio(info["formats"][0]["url"]))