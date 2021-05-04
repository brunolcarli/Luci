import requests
import logging
import pickle
import requests
from random import choice, randint, random
import spacy
import redis
import discord
from discord.ext import commands, tasks
from dateutil import parser
from datetime import datetime, timezone
from core.classifiers import naive_response, get_intentions
from core.output_vectors import (offended, insufficiency_recognition,
                                 propositions, indifference, opinions,
                                 positive_answers, negative_answers, bored_messages)
from core.external_requests import Query, Mutation
from core.emotions import change_humor_values, EmotionHourglass
from core.utils import (validate_text_offense, extract_sentiment,
                        make_hash, get_gql_client, remove_id, get_wiki,
                        get_random_blahblahblah, extract_user_id,
                        evaluate_math_expression, known_language_codes, translate_text)
from core.gans import ResponseGenerator
from luci.settings import __version__, BACKEND_URL, REDIS_HOST, REDIS_PORT, MAIN_CHANNEL


nlp = spacy.load('pt')
client = commands.Bot(command_prefix='!')
log = logging.getLogger()


class GuildTracker(commands.Cog):
    """
    Acompanha a movimentação de mensagens dos servidores que Luci pertence.
    Luci recorda-se de quando foi a última mensagem enviada no server, se a
    mensagem exceder o período em horas definido na janela, ela se sentirá
    sozinha e aborrecida, enviando uma mensagem no canal geral do servidor.

    Luci também diminuirá seu valor de aptitude por ficar aborrecida.
    """
    def __init__(self):
        self.short_memory = redis.Redis(REDIS_HOST, REDIS_PORT, decode_responses=True)
        self.window = 8  # janela de tempo = 8 horas
        self.guilds = client.guilds
        self.track.start()

    @tasks.loop(seconds=60*5)
    async def track(self):
        """ Tracking task """
        log.info('tracking...')
        gql_client = get_gql_client(BACKEND_URL)

        for guild in self.guilds:
            log.info(guild.name)

            server = make_hash('id', guild.id).decode('utf-8')
            # recupera a configuração do server
            query = Query.get_custom_config(server)
            try:
                response = gql_client.execute(query)
            except:
                log.error(f'Cant get server {guild.name} config. Skipping!')
                continue

            server_config = response.get('custom_config')
            main_channel = int(server_config.get('main_channel', 0))
            channel = client.get_channel(main_channel)

            if not channel:
                continue

            # data da última mensagem enviada no server
            try:
                last_message_dt = parser.parse(self.short_memory.get(guild.id))
            except:
                last_message_dt = None

            if last_message_dt:
                now = datetime.now().astimezone(tz=timezone.utc)
                elapsed_time = now.replace(tzinfo=None) - last_message_dt.replace(tzinfo=None)

                log.info('elapsed time: ')
                log.info(elapsed_time)
                log.info('total: ')
                log.info(elapsed_time.total_seconds() / 60 / 60)

                if (elapsed_time.total_seconds() / 60 / 60) > self.window:
                    if server_config.get('allow_auto_send_messages'):
                        # envia mensagem no canal principal se autorizado
                        log.info('Notifying channel %s', channel)
                        await channel.send(choice(bored_messages))

                    # Renova a data de última mensagem para a data atual
                    self.short_memory.set(
                        guild.id,
                        str(now.astimezone(tz=timezone.utc))
                    )
                    log.info('Renewed datetime to %s', str(now))
                    payload = Mutation.update_emotion(
                        server=server,
                        aptitude=-0.1
                    )
                    try:
                        response = gql_client.execute(payload)
                        log.info('Updated aptitude')
                    except Exception as err:
                        log.error(f'Erro: {str(err)}\n\n')


@client.event
async def on_member_join(member):
    """
    Greets the new member.
    """
    # Gets an hello
    message = ResponseGenerator.get_greeting_response()
    server_reference = make_hash('id', int(member.guild.id))
    query = Query.get_custom_config(server_reference)
    try:
        response = gql_client.execute(query)
    except:
        log.error(f'Cant get server {server_reference} config. Skipping!')
        return None

    server_config = response.get('custom_config')
    channel = client.get_channel(int(server_config.get('main_channel')))
    if channel:
        await channel.send(f'{message} {member.mention}')


@client.event
async def on_ready():
    guilds = client.guilds
    client.add_cog(GuildTracker())

    log.info('Ok!')


@client.event
async def on_message(message):
    """
    Handler para mensagens do chat.
    """
    channel = message.channel
    if message.author.bot:
        return

    await client.process_commands(message)
    
    server = make_hash('id', message.guild.id).decode('utf-8')

    # guarda a data da mensagem como valor para o id da guilda
    short_memory = redis.Redis(REDIS_HOST, REDIS_PORT)
    short_memory.set(message.guild.id, str(message.created_at))

    text = message.content

    global_intention, specific_intention = get_intentions(text)
    is_offensive = validate_text_offense(text)
    text_pol = extract_sentiment(text)
    user_name = message.author.name
    new_humor = change_humor_values(text_pol, is_offensive)
    friendshipness = -0.5 + text_pol if is_offensive else text_pol
    msg = {
        'global_intention': global_intention,
        'specific_intention': specific_intention,
        'text': text
    }

    user_id = make_hash(server, message.author.id).decode('utf-8')
    gql_client = get_gql_client(BACKEND_URL)

    # Atualiza o humor da Luci
    payload = Mutation.update_emotion(server=server, **new_humor)
    try:
        gql_client.execute(payload)
    except Exception as err:
        log.error(f'Erro: {str(err)}\n\n')

    # Atualiza o humor status do usuario
    payload = Mutation.update_user(
        user_id,
        user_name,
        friendshipness,
        new_humor,
        msg
    )

    try:
        gql_client.execute(payload)
    except Exception as err:
        log.error(f'Erro: {str(err)}\n\n')

    # get server configuration
    query = Query.get_custom_config(server)
    try:
        response = gql_client.execute(query)
    except Exception as error:
        log.error(str(error))
        server_config = {}

    server_config = response.get('custom_config')

    # Atualiza reconhecimento de respostas, se for resposta à outra mensagem
    if message.reference:
        payload = Mutation.assign_response(
            text=message.reference.resolved.content,
            possible_response=msg
        )

        try:
            response = gql_client.execute(payload)
        except Exception as err:
            log.error(f'Erro: {str(err)}\n\n')

    # process @Luci mentions
    if str(channel.guild.me.id) in text:
        # busca possíveis respostas na memória de longo prazo
        payload = Query.get_possible_responses(
            text=remove_id(text)
        )

        try:
            response = gql_client.execute(payload)
        except Exception as err:
            log.error(f'Erro: {str(err)}\n\n')
            response = {'messages': []}

        if response.get('messages'):
            possible_responses = []
            for msg in response['messages']:
                for possible_response in msg.get('possible_responses'):
                    possible_responses.append(possible_response.get('text'))

            if possible_responses:
                return await channel.send(choice(possible_responses))

        # Caso não conheça nenhuma resposta, use o classificador inocente
        return await channel.send(naive_response(remove_id(text)))

    # 10% chance to not answer if is offensive and lucis not mentioned
    is_allowed = server_config.get('allow_auto_send_messages')
    if is_offensive and choice([1, 0]) and choice([1, 0]) and is_allowed:
        return await channel.send(f'{message.author.mention} {choice(offended)}')


@client.command(aliases=['v'])
async def version(discord):
    """
    Pinga o luci pra ver se está acordada, retornando a versão do sistema.
    """
    await discord.send(__version__)


@client.command(aliases=['st'])
async def status(bot):
    """
    Verifica o estado emocional da Luci.
    """
    server = make_hash('id', bot.guild.id)
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
    server = make_hash('id', bot.guild.id)
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
async def quote(ctx, *args):
    """
    Ensina um novo quote à Luci
    """
    message = ' '.join(word for word in args)
    author = ctx.author.name

    if not message:
        return await ctx.send(
            'Por favor insira uma mensagem.\nExemplo:\n'\
            '``` !quote my name is bond, vagabond ```'
        )

    if '@' in message:
        return await ctx.send(
            'Eu não posso aprender esse tipo de coisa. Vou contar pro meu pai.'
        )

    server = make_hash('id', bot.guild.id)
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
    """
    Luci responde com um pensamento filosófico aleatório.
    """
    
    return await bot.send(get_random_blahblahblah())


@client.command(aliases=['lst', 'ls'])
async def listen(bot, *args):
    """
    Conta algo à Luci para que a mesma responda com base da polaridade da
    mensagem.

    - Uso:
         !listen Fui a feira e moça da barraca me tratou super mal.
    """
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
    """
    Pergunta algo à luci. Ela buscará os substantivos da frase e consultará seu
    significado na wikipedia.

    - Uso:
          !? O que é um príncipe?
    """
    text = ' '.join(i for i in args)
    responses = get_wiki(text)

    for response in responses:
        await bot.send(response)


@client.command(aliases=['u', 'ust', 'user'])
async def user_status(ctx):
    """
    Verifica o relatório de afeição que Luci possui de um determinado membro.

    Uso:
        !user @Username
    """
    mentions = ctx.message.mentions
    if not mentions:
        return await tx.send(
            'Não sei de quem vc está falando. Marca ele tipo @Fulano.'
        )

    # consulta os membros no backend
    server = make_hash('id', ctx.message.guild.id).decode('utf-8')
    user_id = make_hash(server, mentions[0].id).decode('utf-8')
    payload = Query.get_user(user_id)
    gql_client = get_gql_client(BACKEND_URL)

    try:
        response = gql_client.execute(payload)
    except Exception as err:
        log.error(f'Erro: {str(err)}\n\n')
        return

    data = response.get('users', [])
    if not data:
        return await ctx.send('Acho que não c-conheço... Desculpa.')

    # monta a resposta
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    name = data[0].get('name')
    friendshipness = data[0].get('friendshipness', 0)
    emotions = data[0].get('emotion_resume', {})
    user_id = extract_user_id(data[0]['reference'])

    pleasantness_status = EmotionHourglass.get_pleasantness(
        emotions["pleasantness"]
    )
    pleasantness = f':heart_decoration: {emotions["pleasantness"]:.2f} '\
                    f'| status: {pleasantness_status}'

    attention_status = EmotionHourglass.get_attention(
        emotions["attention"]
    )
    attention = f':yin_yang: {emotions["attention"]:.2f} | status: {attention_status}'

    sensitivity_status = EmotionHourglass.get_sensitivity(
        emotions["sensitivity"]
    )
    sensitivity = f':place_of_worship: {emotions["sensitivity"]:.2f} | ' \
                    f'status: {sensitivity_status}'

    aptitude_status = EmotionHourglass.get_aptitude(emotions["aptitude"])
    aptitude = f':atom: {emotions["aptitude"]:.2f} | status: {aptitude_status}'

    embed.add_field(name='Username', value=name, inline=True)
    embed.add_field(name='Affection', value=friendshipness, inline=True)
    embed.add_field(name='Pleasantness', value=pleasantness, inline=False)
    embed.add_field(name='Attention', value=attention, inline=False)
    embed.add_field(name='Sensitivity', value=sensitivity, inline=False)
    embed.add_field(name='Aptitude', value=aptitude, inline=False)

    return await ctx.send('', embed=embed)


@client.command(aliases=['fs', 'friend', 'friends'])
async def friendship(ctx, opt=None):
    """
    Lista os membros com maior afinidade com a Luci.
    O parâmetro `-` solicita que sejam listados os membros com menor afinidade.

    Exemplos:

        - `!fs`
        - `!friendship -`
    """
    embed = discord.Embed(color=0x1E1E1E, type="rich")

    # consulta os membros no backend
    server = make_hash('id', ctx.message.guild.id).decode('utf-8')    
    payload = Query.get_users(server)
    gql_client = get_gql_client(BACKEND_URL)
    try:
        response = gql_client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')
        return

    members = response.get('users')

    if not members:
        return await ctx.send('Acho que ainda não gosto muito de ninguém')

    if opt and opt == '-':
        members = [m for m in members if m['friendshipness'] < 0]

        if not members:
            return await ctx.send('Acho que não tenho muitos amigos aqui ainda')

        members = sorted(members, key=lambda k: k['friendshipness'])[:10]
        
        for member in members:
            body = f'{member["name"]} | :heartpulse: : {member["friendshipness"]}'
            embed.add_field(name='Membro', value=body, inline=False)

        return await ctx.send('Membros que eu menos curto :rolling_eyes:', embed=embed)

    members = [m for m in members if m['friendshipness'] >= 0]
    if not members:
        return await ctx.send('Acho que gosto de todo mundo por aqui')

    members = sorted(members, key=lambda k: k['friendshipness'], reverse=True)[:10]
    for member in members:   
        body = f'{member["name"]} | :heartpulse: : {member["friendshipness"]}'
        embed.add_field(name='Membro', value=body, inline=False)

    return await ctx.send('Membros que eu mais curto :blush:', embed=embed)


@client.command(aliases=['g', 'who_said', 'ws'])
async def guess(ctx, *args):
    """
    Luci tenta adivinhar quem disse a frase.
    """
    text = ' '.join(char for char in args)
    query = Query.somal_guess(text)
    url = 'http://somal.brunolcarli.repl.co/graphql/'

    response = requests.post(url, json={'query': query}).json()
    target = response['data'].get('guess')

    if target:
        if target == 'bruno':
            return await ctx.send('Eu acho que quem disse isso foi o Bruno.')

        return await ctx.send(f'Acho que quem disse isso foi o tio {target.capitalize()}')

    return await ctx.send('Acho que não sei quem disse isso, sei la...')


@client.command(aliases=['wt', 'src', 'who_teached_you'])
async def source(ctx, *args):
    """
    Pergunta quem foi que ensinou a mensagem.
    """
    text = ' '.join(char for char in args)
    if not text.strip():
        return await ctx.send('Ué você não disse nada ...')

    query = Query.get_message_authors(text)
    gql_client = get_gql_client(BACKEND_URL)
    try:
        response = gql_client.execute(query)
    except Exception as err:
        log.error(f'Erro: {str(err)}\n\n')
        return

    authors = set()
    messages = response.get('messages', [])
    if not messages:
        return await ctx.send('Não conhecia essa ainda, até agora...')

    for message in messages:
        authors.add(message.get('author'))

    if len(authors) > 9:
        return await ctx.send(
            f'Ja vi tipo umas {len(authors)} pessoas dizerem isso :rolling_eyes:'
        )

    authors = ';'.join(author for author in list(authors))

    return await ctx.send(f'Aprendi isso com {authors}')


@client.command(aliases=['math', 'clc'])
async def calc(ctx, *args):
    """
    Calcula o total das expressões aritméticas básicas continas na mensagem.
    """
    text = ' '.join(char for char in args)
    if not text.strip():
        return await ctx.send('Manda a braba pra eu calcular ...')

    return await ctx.send(f'Acho que é {evaluate_math_expression(text)}')


@client.command(aliases=['tlt', 'trans'])
async def translate(ctx, code=None, *args):
    """
    Traduz um texto para uma outra linguagem.
    Necessita informar um código de linguagem:
        -Ex:
            !translate pt Hello There

    Códigos válidos:
        ['af', 'ga', 'sq', 'it', 'ar', 'ja', 'az', 'kn', 'eu',
        'ko', 'bn', 'la', 'be', 'lv','bg', 'lt', 'ca', 'mk',
        'ms', 'mt', 'hr', 'no', 'cs', 'fa', 'da', 'pl', 'nl',
        'pt', 'en', 'ro', 'eo', 'ru', 'et', 'sr', 'tl', 'sk',
        'fi', 'sl', 'fr', 'es', 'gl', 'sw', 'ka', 'sv', 'de',
        'ta', 'el', 'te', 'gu', 'th', 'ht', 'tr', 'iw', 'uk',
        'hi', 'ur', 'hu', 'vi', 'is', 'cy', 'id', 'yi']
    """
    text = ' '.join(char for char in args)
    if not text.strip():
        return await ctx.send('Escreve algo pra eu traduzir ...')

    if code not in known_language_codes():
        return await ctx.send('Não conheço esse código dessa linguagem. '\
                              'Manda um !help translate pra ver os códigos que eu sei.')

    return await ctx.send(f'Acho que se traduz como:\n > {translate_text(text, code)}')


@client.command(aliases=['speak', 'ds', 'devil_speak'])
async def satanize(ctx):
    """
    Gera um texto satânico solicitado da API Anton..
    """
    data = '{generatedText{text}}'
    url = 'https://anton.brunolcarli.repl.co/graphql/'
    response = requests.post(url, json={'query': data})
    response = response.json()

    return await ctx.send(response['data']['generatedText'].get('text', 'Não, pera...'))


@client.command(aliases=['cfg', 'config'])
async def custom_config(ctx):
    """
    Verifica as configurações customizaveis para este server.
    """
    server = make_hash('id', ctx.message.guild.id).decode('utf-8')
    payload = Query.get_custom_config(server)
    gql_client = get_gql_client(BACKEND_URL)

    try:
        response = gql_client.execute(payload)
    except Exception as err:
        log.error(f'Erro: {str(err)}\n\n')
        return await ctx.send('D-desculpa, não consegui...')

    data = response.get('custom_config')
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.add_field(name='Server', value=data.get('server_name'), inline=True)
    embed.add_field(name='Sys Channel', value=data.get('main_channel'), inline=True)
    embed.add_field(name='Allow auto send message', value=data.get('allow_auto_send_messages'), inline=False)
    embed.add_field(name='Allow chat learning', value=data.get('allow_learning_from_chat'), inline=False)
    embed.add_field(name='Filter offensive messages', value=data.get('filter_offensive_messages'), inline=False)

    return await ctx.send('Configurações do servidor:', embed=embed)
