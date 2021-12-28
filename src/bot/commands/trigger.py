import bot.commands.cmdlist.gettime as gettime
import bot.commands.cmdlist.audio_player as audio_player

from exceptions import *

class CommandTrigger:
    def __init__(self):
        self.get_time = gettime.GetTime()
        self.audio_player = audio_player.AudioPlayer()

    async def trigger_commands(self, message, command, parameter):
        try:
            if command == "time":
                await self.get_time.get_time(message, parameter)
            elif command == "play":
                await self.audio_player.play(message, parameter)
            elif command == "stopaudio":
                await self.audio_player.stop(message)
            elif command == "pauseaudio":
                await self.audio_player.pause(message)
            elif command == "resumeaudio":
                await self.audio_player.resume(message)
            else:
                raise CommandNotFoundException(f"You tried running the \"{command}\" command but this command cannot be found")
        except Exception as e:
            raise e