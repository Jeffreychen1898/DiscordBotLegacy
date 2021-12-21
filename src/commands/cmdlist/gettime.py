import writer as writer

class GetTime:
    def __init__(self):
        pass

    async def get_time(self, message, parameters):
        await message.channel.send(embed=writer.printError("Testing", "10:00 PM"))