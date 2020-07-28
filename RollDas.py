#!/usr/bin/python3

import argparse
import json
import os

from collections import namedtuple

import discord

from dice import roll, DiceBaseException
from dice.elements import Roll, Integer

class RollDas(discord.Client):
    Command = namedtuple("Command",
                     ["content",
                      "channel",
                      "timestamp",
                      "author",
                      "msg",
                      "triggered",
                      "action",
                      "args"])


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def get_meta(self, rodas, message):
        """ Return a named tuple which contain metadata of a message """
        content = message.content
        args = content.split(" ")
        if (message.author == rodas.user or content is None or len(args[0]) == 0):
            return None

        triggered = args[0] == "!roll"
        action = args[0][1:] if len(args[0]) > 0 else ""
        args = args[1:]

        cmd = self.Command(message.content,
                    message.channel,
                    message.timestamp,
                    message.author,
                    message,
                    triggered,
                    action,
                    args)

        return cmd

    async def on_message(self, message):
        cmd = self.get_meta(self, message)

        if (not cmd or not cmd.triggered or cmd.action not in ["roll"]):
            return

        try:
            result = roll(" ".join(cmd.args))
        except DiceBaseException as e:
            await self.rodas.send_message(cmd.msg.channel,
                                        "Error: \n```" + e.pretty_print() + "```")
            return

        if type(result) is Integer:
            await self.rodas.send_message(cmd.msg.channel,
                                        "The result is: " + str(result))
        elif type(result) in [Roll, list]:
            await self.rodas.send_message(cmd.msg.channel,
                                        "The dices are: " + ", ".join(str(dice) for dice in result[:]))
        else:
            await self.rodas.send_message(cmd.msg.channel,
                                        "That seems to be an unexpected result, please contact DasFranck.")
            print(result)
            print(type(result))
        return


    async def on_ready(self):
        """Triggered when the bot is ready"""
        self.logger.info("Sucessfully connected as %s (%s)" % (self.user.name,
                                                               self.user.id))
        self.logger.info("------------")
 


# The Main.
def main():
    rodas = RollDas()

    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    args = parser.parse_args()

    rodas.run(args.token)


if (__name__ == '__main__'):
    main()
