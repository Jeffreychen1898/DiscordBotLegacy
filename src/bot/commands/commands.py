import enum

import bot.commands.trigger as trigger

from exceptions import *

class Token_Types(enum.Enum):
    WORD = 0
    SPACE = 1
    STRING = 2
    ON_STRING = 3
    COLON = 4
    EQUAL = 5

class Commands:
    def __init__(self, invoke_command):
        self.invoke_command = invoke_command
        self.command_trigger = trigger.CommandTrigger()

    async def on_message(self, message):
        if len(message.content) == 0:
            return

        if message.content[0] == self.invoke_command:
            command_message = message.content[1:]
            if len(command_message) == 0:
                return

            try:
                command, parameters = self.parse_command_message(command_message)
                await self.command_trigger.trigger_commands(message, command, parameters)
            except Exception as e:
                raise e

    #private
    def parse_command_message(self, message):
        try:
            tokens, types = self.tokenize(message)
            command, tokens, types = self.parse_command(tokens, types)

            index = self.find_index_with_token(tokens, " ")
            parameters = self.parse_parameters(tokens, types, index)
            print(parameters)

            return command, parameters
        except Exception as e:
            raise e

    def parse_parameters(self, tokens, types, splits):
        splits.append(len(tokens))

        parameters = {}

        previous_index = 0
        for i in range(len(splits)):
            front = previous_index
            back = splits[i]
            if front == back:
                continue

            key, values = self.parse_parameter(tokens[front:back], types[front:back])
            parameters[key] = values

            previous_index = splits[i] + 1
        
        return parameters
    
    def parse_parameter(self, tokens, types):
        if len(tokens) % 2 == 0:
            raise InvalidStatementException("The Parameter Cannot Be Parsed! This Is Likely Due To An Invalid Syntax!")

        key = ""
        values = []

        for i in range(len(tokens)):
            if i%2 == 0: #key and parameters
                if types[i] != Token_Types.WORD and types[i] != Token_Types.STRING:
                    raise InvalidStatementException("The Parameter Cannot Be Parsed! This Is Likely Due To An Invalid Syntax!")
                else:
                    if key == "":
                        key = tokens[i]
                    else:
                        values.append(tokens[i])
            else: #symbols
                if i == 1:
                    if types[i] != Token_Types.EQUAL:
                        raise InvalidStatementException("The Parameter Cannot Be Parsed! This Is Likely Due To An Invalid Syntax!")
                else:
                    if types[i] != Token_Types.COLON:
                        raise InvalidStatementException("The Parameter Cannot Be Parsed! This Is Likely Due To An Invalid Syntax!")
        
        return key, values
    
    def find_index_with_token(self, array, split):
        index = []
        for i in range(len(array)):
            if array[i] == split:
                index.append(i)
        
        return index
    
    def parse_command(self, tokens, types):
        if types[0] == Token_Types.WORD:
            if len(tokens) > 1:
                if types[1] == Token_Types.SPACE:
                    return tokens[0], tokens[2:], types[2:]
                else:
                    raise InvalidStatementException("A Command Must Be Followed With Spaces!")

            return tokens[0], tokens[1:], types[1:]
        else:
            raise InvalidStatementException("Command Cannot Be A String And Must Contain Only Letters!")
    
    def tokenize(self, message):
        tokens = []
        types = []

        value = ""
        current_type = ""

        for c in message:
            #handle quotes
            if c == "\"":
                if current_type == Token_Types.ON_STRING:
                    current_type = Token_Types.STRING
                else:
                    tokens.append(value)
                    types.append(current_type)
                    current_type = Token_Types.ON_STRING
                    value = ""
                continue

            #handle letters
            if current_type == Token_Types.ON_STRING:
                value += c
                continue

            if self.is_letter(c):
                if current_type != Token_Types.WORD:
                    tokens.append(value)
                    types.append(current_type)
                    value = ""

                current_type = Token_Types.WORD
                value += c
                continue

            #handle spaces
            if c == " ":
                if current_type != Token_Types.SPACE:
                    tokens.append(value)
                    types.append(current_type)
                    value = ""
                
                current_type = Token_Types.SPACE
                value = " "
                continue

            #handle symbols
            tokens.append(value)
            types.append(current_type)
            value = c
            if c == ":":
                current_type = Token_Types.COLON
            elif c == "=":
                current_type = Token_Types.EQUAL
            else:
                raise InvalidStatementException("An Invalid Character Is Detected!")
        
        if current_type == Token_Types.ON_STRING:
            raise InvalidStatementException("A Missing Closing \" Is Detected!")

        if value != "":
            tokens.append(value)
            types.append(current_type)
            
        return tokens[1:], types[1:]

    def is_letter(self, character):
        ascii_code = ord(character)
        if ascii_code > 64 and ascii_code < 91: #upper case
            return True
        
        if ascii_code > 96 and ascii_code < 123: #lower case
            return True
        
        return False