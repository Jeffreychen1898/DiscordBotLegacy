from exceptions import CommandErrorException
import youtube_dl
import discord
import youtube_search

class AudioPlayer:
    def __init__(self):
        self.max_search_list = 5;
        self.ytdl = youtube_dl.YoutubeDL({})

    async def play(self, message, parameters):
        try:
            if message.author.voice is None:
                raise CommandErrorException("You Must Be In A Voice Channel To Use This Command!")

            url, index, search_query = self.find_audio(parameters)
            if not url and not index and not search_query:
                return

            if url != "":
                #play by url
                audio_info = self.ytdl.extract_info(url, download=False)

                voice = await self.connect_to_vc(message)
                voice.play(discord.FFmpegPCMAudio(audio_info["formats"][0]["url"]))

            elif len(search_query) > 0 and index <= self.max_search_list:
                #play by title
                results = youtube_search.YoutubeSearch(search_query[0], max_results=self.max_search_list).to_dict()
                audio_url = "https://www.youtube.com" + results[index]["url_suffix"]
                audio_info = self.ytdl.extract_info(audio_url, download=False)

                voice = await self.connect_to_vc(message)
                voice.play(discord.FFmpegPCMAudio(audio_info["formats"][0]["url"]))
            else:
                raise CommandErrorException("I Do Not Understand What You Want Me To Play!")

        except Exception as e:
            raise e
    
    #private
    def find_audio(self, parameters):
        url = ""
        index = 0
        search_query = []

        if parameters.get("url") is not None:
            if len(parameters["url"]) == 0:
                raise CommandErrorException("You Must List A URL To The Audio You Want To Play!")
            url = parameters["url"][0]

        elif parameters.get("search") is not None:
            search_query = parameters["search"]
            if len(search_query) == 0:
                raise CommandErrorException("You Must List A Title In The Search Parameter")
            
            if parameters.get("index") is not None:
                index_value = parameters["index"]
                if len(index_value > 0):
                    index = index_value[0]
            
            if parameters.get("show") is not None:
                self.output_titles()
                return None, None, None
        
        return url, index, search_query

    def output_titles(self):
        pass

    async def connect_to_vc(self, message):
        if message.guild.voice_client is not None:
            await message.guild.voice_client.disconnect()
        
        voice = await message.author.voice.channel.connect()
        return voice