import bot.commands.trigger as trigger

from exceptions import *

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
        split_message = self.split_command(message)
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
    
    def split_command(self, command):
        result = []
        inside_quote = False
        value = ""
        for character in command:
            if character == "\"":
                inside_quote = not inside_quote
                value += "\""
                continue
            
            if character == " " and inside_quote == False:
                if value != "":
                    result.append(value)
                    value = ""
                
                continue
            
            value += character
        
        if value != "":
            result.append(value)
        
        return result
    
    def parse_parameters(self, parameter):
        key_value_split = parameter.split("=")
        if len(key_value_split) == 2:
            if not self.contain_only_letters(key_value_split[0]):
                raise InvalidStatementException("Parameter Key Can Only Contain Letters!")

            try:
                parameter_values = self.parse_parameter_values(key_value_split[1], ":")
                return key_value_split[0], parameter_values
            except Exception as e:
                raise e

        if not self.contain_only_letters(parameter):
            raise InvalidStatementException("Parameter Can Only Contain Letters!")

        return parameter, None
    
    def parse_parameter_values(self, parameter, split_values_character):
        inside_quotes = False
        values_list = []
        value = ""
        for character in parameter:
            if character == "\"":
                inside_quotes = not inside_quotes
                continue

            if inside_quotes:
                value += character
            elif character == split_values_character:
                if value != "":
                    values_list.append(value)
                    value = ""
            elif self.is_letter(character):
                value += character
            else:
                raise InvalidStatementException("Parameter Value Can Only Contain Letters Or Strings!")
        
        if inside_quotes:
            raise InvalidStatementException("Parameter Value Is Missing A Quotation Mark!")

        if value != "":
            values_list.append(value)

        return values_list

    def is_letter(self, character):
        ascii_code = ord(character)
        if ascii_code > 64 and ascii_code < 91: #upper case
            return True
        
        if ascii_code > 96 and ascii_code < 123: #lower case
            return True
        
        return False

    def contain_only_letters(self, word):
        for character in word:
            if not self.is_letter(character):
                return False

        return True