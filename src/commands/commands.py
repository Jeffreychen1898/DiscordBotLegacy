import discord

from exceptions import *
import commands.trigger as trigger

class Commands:
    def __init__(self, invoke_command):
        self.invoke_command = invoke_command
        self.command_trigger = trigger.CommandTrigger()

    async def on_message(self, message):
        if len(message.content) == 0:
            return

        if message.content[0] == self.invoke_command:#step 1
            try:
                command, parameters = self.parse_command(message.content[1:])
                await self.command_trigger.trigger_commands(message, command, parameters)
            except Exception as e:
                raise e

    #private
    def parse_command(self, message):
        command = ""
        parameters = {}
        #step 2
        split_message = message.split()
        for each_word in split_message:
            word = each_word.strip()
            if word == "":
                continue

            if command == "":
                if self.contain_only_letters(word):
                    command = word
                    continue
                else:
                    raise InvalidStatementException("Command Can Only Contain Letters!")
            
            #step 3
            try:
                key, value = self.parse_parameters(word)
                parameters[key] = value
            except InvalidStatementException as e:
                raise e
        
        return command, parameters
    
    def parse_parameters(self, parameter):
        key_value_split = parameter.split("=")
        if len(key_value_split) == 2:
            if not self.contain_only_letters(key_value_split[0]):
                raise InvalidStatementException("Parameter Key Can Only Contain Letters!")

            split_array = key_value_split[1].split(":")
            split_array = list(filter(lambda s:s != "", split_array))
            for value in split_array:
                if not self.containOnlyLetters(value):
                    raise InvalidStatementException("Parameter Value Can Only Contain Letters!")

            return key_value_split[0], split_array

        if not self.contain_only_letters(parameter):
            raise InvalidStatementException("Parameter Can Only Contain Letters!")

        return parameter, None

    def contain_only_letters(self, word):
        for character in word:
            ascii_code = ord(character)
            if ascii_code < 65 or ascii_code > 90: #upper case
                if ascii_code < 97 or ascii_code > 122: #lower case
                    return False

        return True