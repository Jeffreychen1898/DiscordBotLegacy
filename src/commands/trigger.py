#import commands.cmdlist.gettime as time
from commands.cmdlist.gettime import GetTime
from exceptions import *

class CommandTrigger:
    def __init__(self):
        self.get_time = GetTime()

    async def trigger_commands(self, message, command, parameter):
        if(command == "time"):
            await self.get_time.get_time(message, parameter)
        else:
            raise CommandNotFoundException(f"You tried running the \"{command}\" command but this command cannot be found")