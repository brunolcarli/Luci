import pickle
from random import choice, randint, random
import spacy
import discord
from discord.ext import commands

from core.classifiers import naive_response
from core.output_vectors import (offended, insufficiency_recognition,
                                 propositions, indifference, opinions,
                                 positive_answers, negative_answers)
from core.external_requests import Query, Mutation
from core.emotions import change_humor_values, EmotionHourglass
from core.utils import (validate_text_offense, extract_sentiment, answer_intention,
                        make_hash, get_gql_client, remove_id, get_wiki)
from luci.settings import __version__, BACKEND_URL


nlp = spacy.load('pt')
client = commands.Bot(command_prefix='!')


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
    is_offensive = validate_text_offense(text)
    text_pol = extract_sentiment(text)

    # updates luci humor based on the message content
    new_humor = change_humor_values(text_pol, is_offensive)

    server = make_hash(message.guild.name, message.guild.id)
    gql_client = get_gql_client(BACKEND_URL)

    payload = Mutation.update_emotion(server=server.decode('utf-8'), **new_humor)
    try:
        response = gql_client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')

    # process @Luci mentions
    if str(channel.guild.me.id) in text:
        return await channel.send(naive_response(remove_id(text)))

    # 50% chance to not answer if is offensive and lucis not mentioned
    if is_offensive and choice([True, False]):
        return await channel.send(f'{message.author.mention} {choice(offended)}')


@client.command(aliases=['v'])
async def version(discord):
    """
    Pinga o luci pra ver se está acordada.
    """
    await discord.send(__version__)


@client.command(aliases=['st'])
async def status(bot):
    """
    Verifica o estado emocional da Luci.
    """
    server = make_hash(bot.guild.name, bot.guild.id)
    payload = Query.get_emotions(server.decode('utf-8'))
    client = get_gql_client(BACKEND_URL)

    try:
        response = client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')
        return await bot.send('Buguei')

    humor = response.get('emotions')
    if humor:
        luci_humor = humor[0]

        embed = discord.Embed(color=0x1E1E1E, type='rich')

        pleasantness_status = EmotionHourglass.get_pleasantness(
            luci_humor["pleasantness"]
        )
        pleasantness = f':heart_decoration: {luci_humor["pleasantness"]:.2f} '\
                       f'| status: {pleasantness_status}'

        attention_status = EmotionHourglass.get_attention(
            luci_humor["attention"]
        )
        attention = f':yin_yang: {luci_humor["attention"]:.2f} | status: {attention_status}'

        sensitivity_status = EmotionHourglass.get_sensitivity(
            luci_humor["sensitivity"]
        )
        sensitivity = f':place_of_worship: {luci_humor["sensitivity"]:.2f} | ' \
                      f'status: {sensitivity_status}'

        aptitude_status = EmotionHourglass.get_aptitude(luci_humor["aptitude"])
        aptitude = f':atom: {luci_humor["aptitude"]:.2f} | status: {aptitude_status}'

        embed.add_field(name='Pleasantness', value=pleasantness, inline=False)
        embed.add_field(name='Attention', value=attention, inline=False)
        embed.add_field(name='Sensitivity', value=sensitivity, inline=False)
        embed.add_field(name='Aptitude', value=aptitude, inline=False)

        return await bot.send('', embed=embed)


@client.command(aliases=['rquote', 'rq'])
async def random_quote(bot):
    """
    Retorna um quote aleatório.
    """
    server = make_hash(bot.guild.name, bot.guild.id)
    payload = Query.get_quotes(server.decode('utf-8'))
    client = get_gql_client(BACKEND_URL)

    try:
        response = client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')
        return await bot.send('Buguei')

    quotes = response.get('quotes')
    if not quotes:
        return await bot.send('Ainda não aprendi quotes neste servidor')

    chosen_quote = choice([quote['quote'] for quote in quotes])

    return await bot.send(chosen_quote)


@client.command(aliases=['q', 'sq', 'save_quote'])
async def quote(bot, *args):
    """
    Ensina um novo quote à Luci
    """
    message = ' '.join(word for word in args)
    author = bot.author.name

    if not message:
        return await bot.send(
            'Por favor insira uma mensagem.\nExemplo:\n'\
            '``` !quote my name is bond, vagabond ```'
        )

    server = make_hash(bot.guild.name, bot.guild.id)
    payload = Mutation.create_quote(message, server.decode('utf-8'), author)
    client = get_gql_client(BACKEND_URL)

    try:
        response = client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')
        return await bot.send('Buguei')

    quote = response['create_quote'].get('quote')
    embed = discord.Embed(color=0x1E1E1E, type="rich")
    embed.add_field(name='Entendi:', value=quote.get('quote'), inline=True)
    return await bot.send('Ok:', embed=embed)


@client.command(aliases=['lero', 'lr', 'bl', 'blah', 'ps'])
async def prosa(bot):
    random_tought = ''.join(choice(i) for i in propositions)
    random_tought_2 = ''.join(choice(i) for i in propositions)

    response = f'{choice(opinions[0])}. '\
               f'{random_tought} '\
               f'{random_tought_2} Viajei né?'
    return await bot.send(response)


@client.command(aliases=['lst', 'ls'])
async def listen(bot, *args):
    text = ' '.join(token for token  in args)

    text_polarity = extract_sentiment(text)
    if text_polarity > 0:
        return await bot.send(''.join(choice(i) for i in positive_answers))
    elif text_polarity < 0:
        return await bot.send(''.join(choice(i) for i in negative_answers))
    else:
        return await bot.send(choice(indifference))


@client.command(aliases=['?', 'wiki'])
async def question(bot, *args):
    text = ' '.join(i for i in args)
    responses = get_wiki(text)

    for response in responses:
        await bot.send(response)
