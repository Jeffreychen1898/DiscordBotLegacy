#import commands.cmdlist.gettime as time
from commands.cmdlist.gettime import GetTime
from exceptions import *

class CommandTrigger:
    def __init__(self):
        self.getTime = GetTime()

    async def triggerCommands(self, message, command, parameter):
        if(command == "time"):
            await self.getTime.getTime(message, parameter)
        else:
            raise CommandNotFoundException(f"You tried running the \"{command}\" command but this command cannot be found")