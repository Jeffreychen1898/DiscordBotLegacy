import youtube_dl
import discord
import youtube_search

from exceptions import CommandErrorException
import bot.writer as writer

class AudioPlayer:
    def __init__(self):
        self.max_search_list = 5;
        self.ytdl = youtube_dl.YoutubeDL({})

    async def play(self, message, parameters):
        try:
            if message.author.voice is None:
                raise CommandErrorException("You Must Be In A Voice Channel To Use This Command!")

            url, index, search_query = await self.find_audio(message, parameters)
            if url == None and index == None and search_query == None:
                return

            if url != "":
                #play by url
                audio_info = self.ytdl.extract_info(url, download=False)

                voice = await self.connect_to_vc(message)
                await self.display_audio(message, audio_info["title"], url)
                voice.play(discord.FFmpegPCMAudio(audio_info["formats"][0]["url"]))

            elif len(search_query) > 0 and index < self.max_search_list and index >= 0:
                #play by title
                results = youtube_search.YoutubeSearch(search_query[0], max_results=self.max_search_list).to_dict()
                audio_url = "https://www.youtube.com" + results[index]["url_suffix"]
                audio_info = self.ytdl.extract_info(audio_url, download=False)

                voice = await self.connect_to_vc(message)
                await self.display_audio(message, audio_info["title"], audio_url)
                voice.play(discord.FFmpegPCMAudio(audio_info["formats"][0]["url"]))
            else:
                raise CommandErrorException("I Do Not Understand What You Want Me To Play!")

        except Exception as e:
            raise e
    
    #private
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

    async def connect_to_vc(self, message):
        if message.guild.voice_client is not None:
            await message.guild.voice_client.disconnect()
        
        voice = await message.author.voice.channel.connect()
        return voice