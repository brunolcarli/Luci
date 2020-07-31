import logging
import pickle
from random import choice, randint, random

import discord
from discord.ext import commands

from core.classifiers import naive_response, NeuralNetwork
from core.output_vectors import (offended, insufficiency_recognition,
                                 propositions, indifference, opinions,
                                 positive_answers, negative_answers)
from core.external_requests import Query, Mutation
from core.utils import (validate_text_offense, extract_sentiment, answer_intention,
                        make_hash, get_gql_client, get_text_vector)
from luci.settings import __version__, SELF_ID, API_URL
import spacy


nlp = spacy.load('pt')

client = commands.Bot(command_prefix='!')


def get_pol_response(polarity):
    # Answers based on text polarity
    if polarity < 0:
        return ''.join(choice(i) for i in negative_answers)
    elif polarity > 0:
        return ''.join(choice(i) for i in positive_answers)
    else:
        return choice(indifference)


def get_random_blablabla():
    random_tought = ''.join(choice(i) for i in propositions)
    random_tought_2 = ''.join(choice(i) for i in propositions)

    response = f'{choice(opinions[0])}. '\
               f'{random_tought} '\
               f'{random_tought_2}. Mas posso estar errada.'
    return response


def on_mention(message, polarity):
    """
    Process messages that mention Luci on chat.
    """
    logging.info(message)
    nn = NeuralNetwork()
    intention_response = naive_response(message)

    pol_response = get_pol_response(polarity)
    blablabla = get_random_blablabla()
    dunno = ''.join(choice(i) for i in insufficiency_recognition)

    input_vector = get_text_vector(message)
    response_vector = get_text_vector(intention_response)
    pol_vector = get_text_vector(pol_response)
    blablabla_vector = get_text_vector(blablabla)
    dunno_vector = get_text_vector(dunno)

    possibilities = {
        nn.execute(input_vector, response_vector): intention_response,
        nn.execute(input_vector, pol_vector): pol_response,
        nn.execute(input_vector, blablabla_vector): blablabla,
        nn.execute(input_vector, dunno_vector): dunno
    }
    print(possibilities)

    return possibilities[min(possibilities.keys())]


    # # Verify if is a question
    # if '?' in message:
    #     if value >= 9.2:
    #         random_tought = ''.join(choice(i) for i in propositions)
    #         random_tought_2 = ''.join(choice(i) for i in propositions)

    #         response = f'{choice(opinions[0])}. '\
    #                    f'{random_tought} '\
    #                    f'{random_tought_2} Viajei né?'
    #         return response

    #     elif 5 <= value < 9.2:
    #         return naive_response(message)
          
    #     elif 0 < value < 2:
    #         return ''.join(choice(i) for i in opinions)

    #     else:
    #         return ''.join(choice(i) for i in insufficiency_recognition)
    
    # if 2 <= value < 3:
    #     # Answers based on text polarity
    #     if polarity < 0:
    #         return ''.join(choice(i) for i in negative_answers)
    #     elif polarity > 0:
    #         return ''.join(choice(i) for i in positive_answers)
    #     else:
    #         return choice(indifference)
    # else:
    #     return naive_response(message)


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

    # 50% chance to not answer
    if is_offensive and choice([True, False]):
        return await channel.send(f'{message.author.mention} {choice(offended)}')

    # Verify text polarity
    text_polarity = extract_sentiment(text)

    # process @Luci mentions
    mention = str(channel.guild.me.id)
    if mention in text:
        pos = text.find(mention)
        text = (text[:pos] + text[pos+len(mention):]).strip()
        response = on_mention(text.encode('utf-8').decode('utf-8'), text_polarity)
        if response:
            return await channel.send(f'{message.author.mention} {response}')


@client.command(aliases=['v'])
async def version(discord):
    """
    Pinga o bot para teste sua execução
    """
    await discord.send(__version__)


@client.command(aliases=['rquote', 'rq'])
async def random_quote(bot):
    """
    Retorna um quote aleatório.
    """
    server = make_hash(bot.guild.name, bot.guild.id)
    payload = Query.get_quotes(server.decode('utf-8'))
    client = get_gql_client(API_URL)

    try:
        response = client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')
        return await bot.send('Erro')

    quotes = response.get('botQuotes')
    if not quotes:
        return await bot.send('Ainda não há registros de quotes neste servidor')

    chosen_quote = choice(quotes)
    embed = discord.Embed(color=0x1E1E1E, type="rich")
    embed.add_field(name='Quote:', value=chosen_quote, inline=True)
    return await bot.send('Lembra disso:', embed=embed)


@client.command(aliases=['q', 'sq', 'save_quote'])
async def quote(bot, *args):
    """
    Retorna um quote aleatório.
    """
    message = ' '.join(word for word in args)

    if not message:
        return await bot.send(
            'Por favor insira uma mensagem.\nExemplo:\n'\
            '``` --quote my name is bond, vagabond ```'
        )

    server = make_hash(bot.guild.name, bot.guild.id)
    payload = Mutation.create_quote(message, server.decode('utf-8'))
    client = get_gql_client(API_URL)

    try:
        response = client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')
        return await bot.send('Erro')

    quote = response.get('botCreateQuote')
    embed = discord.Embed(color=0x1E1E1E, type="rich")
    embed.add_field(name='Quote salvo:', value=quote.get('response'), inline=True)
    return await bot.send('Feito:', embed=embed)


# @client.command(aliases=['x'])
# async def baz(bot, *args):
#     text = ' '.join(i for i in args)
#     print(text)
#     v = nlp(text)

#     return await bot.send(myself_intention_recognizer.predict([v.vector]))
