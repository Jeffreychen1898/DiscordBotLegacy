import commands.cmdlist.gettime as time

class CommandTrigger:
    def __init__(self):
        self.getTime = time.GetTime()

    async def triggerCommands(self, message, command, parameter):
        if(command == "time"):
            await self.getTime.getTime(message, parameter)