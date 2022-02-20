# discord.py api reference: https://discordpy.readthedocs.io/en/stable/api.html

import discord
import os

botclient = discord.Client()


async def processCommand(msg):
    if msg.content.startswith("!pin"):
        if msg.reference is None:
            await msg.channel.send("Not a reply, no message to pin!")
        else:
            repl = await msg.channel.fetch_message(msg.reference.message_id)
            if repl is not None:
                await repl.pin()
    elif msg.content.startswith("!name"):
        tokens = msg.content.split(" ")
        if len(tokens) < 2:
            await msg.channel.send("No name provided")
        else:
            # get the server the message came from, and set the nick in that server
            await msg.guild.get_member(botclient.user.id).edit(nick=tokens[1])
            await msg.channel.send("Thanks for the name!")
    elif msg.content.startswith("!help"):
        await msg.channel.send("Reply to a message with !pin to pin it, and use !name [something] to set my name")
    else:
        tokens = msg.content.split(" ")
        await msg.channel.send("Unrecognized command: " + tokens[0])


#  Discord events
@botclient.event
async def on_ready():
    print('Bot connected as user {0}'.format(botclient.user))


@botclient.event
async def on_message(message):
    # Bot ignores own posts
    if message.author == botclient.user:
        return

    if message.content[0] == '!':
        try:
            await processCommand(message)
        except Exception as e:
            await message.channel.send("An error occurred:")
            await message.channel.send(str(e))


# Actual program starts execution here
token = None

if os.path.exists("token.txt"):
    with open("token.txt") as tf:
        lines = tf.readlines()
        if len(lines) > 0:
            token = lines[0].strip()
        else:
            print("Token file is empty!")
else:
    print("Token file is missing!")

if token is not None:
    botclient.run(token)
