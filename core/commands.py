from random import choice, randint

import discord
from discord.ext import commands

from core.output_vectors import (offended, insufficiency_recognition,
                                 propositions, indifference, opinions,
                                 positive_answers, negative_answers)
from core.utils import validate_text_offense, extract_sentiment
from luci.settings import __version__, SELF_ID


client = commands.Bot(command_prefix='!')


def on_mention(message, polarity):
    """
    Process messages that mention Luci on chat.
    """
    # verify if is a thanks message
    thanks = [
        'obrigado', 'obrigada', 'agradecido', 'valeu', 'vlw', 'obgd', 'obg'
    ]
    # TODO: Move to output vectors module
    thanks_response = ['disponha!', 'por nada!']

    if any(word for word in message.lower().split() if word in thanks):
        return choice(thanks_response)

    if len(message) < 25:
        # Theres no message just a mention
        got_my_attention = ['oi', 'chora', 'diga']
        return choice(got_my_attention)

    # Verify if is a question
    if '?' in message:
        # TODO implement a better handler, til there, 
        # just say dont know or some blabla based on random value
        value = randint(1, 9)
        if 1 < value <= 3:
            random_tought = ''.join(choice(i) for i in propositions)
            random_tought_2 = ''.join(choice(i) for i in propositions)

            response = f'{choice(opinions[0])}. '\
                       f'{random_tought} '\
                       f'{random_tought_2} Viajei né?'
            return response

        elif 4 < value <= 6:
            return ''.join(choice(i) for i in insufficiency_recognition)

        else:
            return ''.join(choice(i) for i in opinions)

    # Answers based on text polarity
    if polarity < 0:
        return ''.join(choice(i) for i in negative_answers)
    elif polarity > 0:
        return ''.join(choice(i) for i in positive_answers)
    else:
        return choice(indifference)


@client.event
async def on_ready():
    print('Ok!')


@client.event
async def on_message(message):
    """
    Handler para mensagens do chat.
    """
    channel = message.channel
    if message.author.bot:
        return

    await client.process_commands(message)

    text = message.content

    # Verify if message is offensive
    is_offensive = validate_text_offense(text)
    if is_offensive:
        await channel.send(f'{message.author.mention} {choice(offended)}')

    # Verify text polarity
    text_polarity = extract_sentiment(text)

    # process @Luci mentions
    if str(channel.guild.me.id) in text:
        response = on_mention(text, text_polarity)
        if response:
            return await channel.send(f'{message.author.mention} {response}')


@client.command(aliases=['v'])
async def version(discord):
    """
    Pinga o bot para teste sua execução
    """
    await discord.send(__version__)
