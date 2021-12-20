import discord

from exceptions import *

class Commands:
    def __init__(self, invokeCommand):
        self.invokeCommand = invokeCommand
        #self.commandTrigger = CommandTriggers()

    def onMessage(self, message):
        if len(message.content) == 0:
            return

        if message.content[0] == self.invokeCommand:#step 1
            try:
                command, parameters = self.parseCommand(message.content[1:])
                raise CommandNotFoundException("You Can Only Use A Valid Command!")
            except Exception as e:
                raise e

    #private
    def parseCommand(self, message):
        command = ""
        parameters = {}
        #step 2
        split_message = message.split()
        for each_word in split_message:
            word = each_word.strip()
            if word == "":
                continue

            if command == "":
                if self.containOnlyLetters(word):
                    command = word
                    continue
                else:
                    raise InvalidStatementException("Command Can Only Contain Letters!")
            
            #step 3
            try:
                key, value = self.parseParameters(word)
                parameters[key] = value
            except InvalidStatementException as e:
                raise e
        
        return command, parameters
    
    def parseParameters(self, parameter):
        key_value_split = parameter.split("=")
        if len(key_value_split) == 2:
            if not self.containOnlyLetters(key_value_split[0]):
                raise InvalidStatementException("Parameter Key Can Only Contain Letters!")

            split_array = key_value_split[1].split(":")
            split_array = list(filter(lambda s:s != "", split_array))
            for value in split_array:
                if not self.containOnlyLetters(value):
                    raise InvalidStatementException("Parameter Value Can Only Contain Letters!")

            return key_value_split[0], split_array

        if not self.containOnlyLetters(parameter):
            raise InvalidStatementException("Parameter Can Only Contain Letters!")

        return parameter, None

    def containOnlyLetters(self, word):
        for character in word:
            ascii_code = ord(character)
            if ascii_code < 65 or ascii_code > 90: #upper case
                if ascii_code < 97 or ascii_code > 122: #lower case
                    return False

        return True