from discord import guild
import youtube_dl
import discord
import youtube_search
import asyncio

from exceptions import CommandErrorException
import bot.writer as writer

class AudioPlayer:
    def __init__(self):
        ytdl_options = {
            "format": "bestaudio/best"
        }
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        self.max_search_list = 5;
        self.ytdl = youtube_dl.YoutubeDL(ytdl_options)

        """
        guild_id: {
            queue: []
            playing: boolean
        }
        """
        self.queues = {}

    async def play(self, message, parameters):
        try:
            if message.author.voice is None:
                raise CommandErrorException("You Must Be In A Voice Channel To Use This Command!")

            await self.connect_to_vc(message)

            url, index, search_query = await self.find_audio(message, parameters)
            if url == None and index == None and search_query == None:
                return

            if url == "":
                url = self.search_youtube(search_query, index)

            if self.queues.get(message.guild.id) is None:
                self.queues[message.guild.id] = {}
                self.queues[message.guild.id]["queue"] = []
                self.queues[message.guild.id]["playing"] = False

            self.queues[message.guild.id]["queue"].append(url)

            if self.queues[message.guild.id]["playing"] == False:
                info = await self.play_audio(message)
                await self.display_audio(message, info["title"], url)
            else:
                info = self.ytdl.extract_info(url, download=False)
                await self.display_queued_song(message, info["title"], url)

        except Exception as e:
            raise e
    
    async def stop(self, message):
        if self.not_in_vc(message):
            raise CommandErrorException("I Am Not Playing Any Audio In The Voice Channel At The Moment!")

        #self.remove_queue(message)
        self.remove_queue(message)
        message.guild.voice_client.stop()
        await message.guild.voice_client.disconnect()
    
    async def skip(self, message):
        if self.not_in_vc(message):
            raise CommandErrorException("I Am Not Playing Any Audio In The Voice Channel At The Moment!")
        
        message.guild.voice_client.stop()

    async def pause(self, message):
        if self.not_in_vc(message):
            raise CommandErrorException("I Am Not Playing Any Audio In The Voice Channel At The Moment!")

        message.guild.voice_client.pause()

    async def resume(self, message):
        if self.not_in_vc(message):
            raise CommandErrorException("I Am Not Playing Any Audio In The Voice Channel At The Moment!")

        message.guild.voice_client.resume()
    
    #private
    def on_audio_end(self, message, url):
        info = self.ytdl.extract_info(url, download=False)
        message.guild.voice_client.play(discord.FFmpegPCMAudio(info["formats"][0]["url"], **self.ffmpeg_options))

    def search_youtube(self, search_query, index):
        try:
            results = youtube_search.YoutubeSearch(search_query[0], max_results=self.max_search_list).to_dict()
            return "https://www.youtube.com" + results[index]["url_suffix"]
        except:
            raise CommandErrorException("This Audio Cannot Be Found Or It May Be Restricted!")

    async def play_audio(self, message):
        try:
            if message.guild.voice_client is None:
                self.remove_queue(message)
                return
            
            if len(message.guild.voice_client.channel.members) == 1:
                await self.stop(message)
                return

            url, found = self.find_audio_in_queue(message.guild.id)
            if not found:
                self.remove_queue(message)
                await message.guild.voice_client.disconnect()
                return

            self.queues[message.guild.id]["playing"] = True

            info = self.ytdl.extract_info(url, download=False)
            audio = discord.FFmpegPCMAudio(info["formats"][0]["url"], **self.ffmpeg_options)

            on_finished = lambda e: self.on_audio_end(message)

            message.guild.voice_client.play(audio, after=on_finished)
            
            return info
        except Exception as e:
            raise CommandErrorException("The URL Appears To Be Invalid!")
    
    def on_audio_end(self, message):
        coroutine = self.play_audio(message)
        future = asyncio.run_coroutine_threadsafe(coroutine, writer.client.loop)
        try:
            future.result()
        except Exception as e:
            raise e
    
    def find_audio_in_queue(self, guild_id):
        if self.queues.get(guild_id) is not None:
            queue = self.queues[guild_id]["queue"]
            if len(queue) > 0:
                url = queue[0]

                self.queues[guild_id]["queue"].pop(0)

                return url, True
        
        return "", False
    
    def remove_queue(self, message):
        if self.queues.get(message.guild.id) is not None:
            del self.queues[message.guild.id]
 
    async def find_audio(self, message, parameters):
        url = ""
        index = 0
        search_query = []

        # search by url
        if parameters.get("url") is not None:
            if len(parameters["url"]) == 0:
                raise CommandErrorException("You Must List A URL To The Audio You Want To Play!")
            url = parameters["url"][0]

        #search by title
        elif parameters.get("search") is not None:
            search_query = parameters["search"]
            if len(search_query) == 0:
                raise CommandErrorException("You Must List A Title In The Search Parameter")
            
            #index
            if parameters.get("index") is not None:
                index_value = parameters["index"]
                if len(index_value) > 0:
                    index = int(index_value[0]) - 1
            
            #show list of videos
            if parameters.get("show") is not None:
                await self.output_titles(message, search_query[0])
                return None, None, None
        
        return url, index, search_query

    async def output_titles(self, message, search_query):
        results = youtube_search.YoutubeSearch(search_query, max_results=self.max_search_list).to_dict()

        embed = discord.Embed(title=f"What I Found For \"{search_query}\"", color=writer.COLOR_SUCCESS)

        counter = 1
        for result in results:
            url = "https://www.youtube.com" + result["url_suffix"]
            title = result["title"]

            embed.add_field(name=f"{counter} {title}", value=url, inline=False)

            counter += 1
        
        writer.polish_message(message, embed)
        await message.channel.send(embed=embed)
    
    async def display_audio(self, message, title, url):

        description = "Will Start Playing Shortly! URL: " + url

        embed = discord.Embed(title=title, description=description, color=writer.COLOR_SUCCESS)
        writer.polish_message(message, embed)
        await message.channel.send(embed=embed)
    
    async def display_queued_song(self, message, title, url):
        description = "Is Now In The Queue! URL: " + url

        embed = discord.Embed(title=title, description=description, color=writer.COLOR_SUCCESS)
        writer.polish_message(message, embed)
        await message.channel.send(embed=embed)
    
    async def display_queue(self, message):
        title = "Current Queue"
        embed = discord.Embed(title=title, color=writer.COLOR_SUCCESS)

        if self.queues.get(message.guild.id) is None:
            name = "The Queue Is Empty"
            description = "Use the $play command to add an item to the queue!"
            embed.add_field(name=name, value=description, inline=False)
        else:
            counter = 1
            for url in self.queues[message.guild.id]["queue"]:
                embed.add_field(name=counter, value=url, inline=False)

                counter += 1
        
        writer.polish_message(message, embed)
        await message.channel.send(embed=embed)
    
    def not_in_vc(self, message):
        if not message.guild.voice_client:
            return True
        
        return False

    async def connect_to_vc(self, message):
        if message.guild.voice_client is None:
            await message.author.voice.channel.connect()
        elif message.guild.voice_client.channel is not message.author.voice.channel:
            await message.guild.voice_client.disconnect()
            await message.author.voice.channel.connect()