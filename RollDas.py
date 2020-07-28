#!/usr/bin/python3

import argparse
import json
import os

from collections import namedtuple

from discord

from dice import roll, DiceBaseException
from dice.elements import Roll, Integer

rodas = discord.Client()

Command = namedtuple("Command",
                     ["content",
                      "channel",
                      "timestamp",
                      "author",
                      "msg",
                      "triggered",
                      "action",
                      "args"])



def get_meta(message):
    """ Return a named tuple which contain metadata of a message """
    content = message.content
    args = content.split(" ")
    if (message.author == rodas.user or content is None or len(args[0]) == 0):
        return None

    cmd = {"content": message.content,
           "channel": message.channel,
           "timestamp": message.timestamp,
           "author": message.author,
           "msg": message,
           "triggered": args[0] == "!roll",
           "action": args[0][1:] if len(args[0]) > 0 else "",
           "args": args[1:]}

    return cmd

@rodas.event
async def on_message(message):
    cmd = get_meta(message)
    print(cmd)

    if (not cmd or not cmd["triggered"] or cmd["action"] not in ["roll"]):
        return

    try:
        result = roll(" ".join(cmd["args"]))
    except DiceBaseException as e:
        await rodas.send_message(cmd["msg"].channel,
                                    "Error: \n```" + e.pretty_print() + "```")
        return

    if type(result) is Integer:
        await rodas.send_message(cmd["msg"].channel,
                                    "The result is: " + str(result))
    elif type(result) in [Roll, list]:
        await rodas.send_message(cmd["msg"].channel,
                                    "The dices are: " + ", ".join(str(dice) for dice in result[:]))
    else:
        await rodas.send_message(cmd["msg"].channel,
                                    "That seems to be an unexpected result, please contact DasFranck.")
        print(result)
        print(type(result))
    return

@rodas.event
async def on_ready(self):
    """Triggered when the bot is ready"""
    self.logger.info("Sucessfully connected as %s (%s)" % (self.user.name,
                                                            self.user.id))
    self.logger.info("------------")
    print("OK")



# The Main.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    args = parser.parse_args()

    rodas.run(args.token)


if (__name__ == '__main__'):
    main()
