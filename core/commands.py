from random import choice, randint

import discord
from discord.ext import commands

from core.output_vectors import (offended, insufficiency_recognition,
                                 propositions, indifference, opinions,
                                 positive_answers, negative_answers)
from core.external_requests import Query, Mutation
from core.utils import (validate_text_offense, extract_sentiment, answer_intention,
                        make_hash, get_gql_client)
from luci.settings import __version__, SELF_ID, API_URL


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

    # if already know the intention
    intention_response = answer_intention(message)
    if intention_response:
        return intention_response

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
