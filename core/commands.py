import logging
import pickle
from random import choice, randint, random
import spacy
import redis
import discord
from discord.ext import commands, tasks
from dateutil import parser
from datetime import datetime, timezone
from core.classifiers import naive_response
from core.output_vectors import (offended, insufficiency_recognition,
                                 propositions, indifference, opinions,
                                 positive_answers, negative_answers, bored_messages)
from core.external_requests import Query, Mutation
from core.emotions import change_humor_values, EmotionHourglass
from core.utils import (validate_text_offense, extract_sentiment, answer_intention,
                        make_hash, get_gql_client, remove_id, get_wiki,
                        get_random_blahblahblah, extract_user_id)
from luci.settings import __version__, BACKEND_URL, REDIS_HOST, REDIS_PORT


nlp = spacy.load('pt')
client = commands.Bot(command_prefix='!')
log = logging.getLogger()


class GuildTracker(commands.Cog):
    """
    Acompanha a movimentaçnao de mensagens dos servidores que Luci pertence.
    Luci recorda-se de quando foi a última mensagem enviada no server, se a
    mensagem exceder o período em horas definido na janela, ela se sentirá
    sozinha e aborrecida, enviando uma mensagem no canal geral do servidor.

    Luci também diminuirá seu valor de aptitude por ficar aborrecida.
    """
    def __init__(self):
        self.short_memory = redis.Redis(REDIS_HOST, REDIS_PORT, decode_responses=True)
        self.window = 3  # janela de tempo = 3 horas
        self.guilds = client.guilds
        self.track.start()

    @tasks.loop(seconds=60*5)
    async def track(self):
        """ Tracking task """
        log.info('tracking...')
        for guild in self.guilds:
            log.info(guild.name)
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
                    # envia mensagem no canal principal
                    log.info('Notifying channel %s', guild.system_channel.name)
                    await guild.system_channel.send(choice(bored_messages))

                    # Renova a data de última mensagem para a data atual
                    self.short_memory.set(
                        guild.id,
                        str(now.astimezone(tz=timezone.utc))
                    )
                    log.info('Renewed datetime to %s', str(now))

                    # Atualiza o humor da Luci no backend
                    server = make_hash(guild.name, guild.id).decode('utf-8')
                    gql_client = get_gql_client(BACKEND_URL)

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

    # guarda a data da mensagem como valor para o id da guilda
    short_memory = redis.Redis(REDIS_HOST, REDIS_PORT)
    short_memory.set(message.guild.id, str(message.created_at))

    text = message.content
    is_offensive = validate_text_offense(text)
    text_pol = extract_sentiment(text)
    user_name = message.author.name
    new_humor = change_humor_values(text_pol, is_offensive)
    friendshipness = -0.5 + text_pol if is_offensive else text_pol

    server = make_hash(message.guild.name, message.guild.id).decode('utf-8')
    user_id = make_hash(server, message.author.id).decode('utf-8')
    gql_client = get_gql_client(BACKEND_URL)

    # Atualiza o humor da Luci
    payload = Mutation.update_emotion(server=server, **new_humor)
    try:
        response = gql_client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')

    # Atualiza o humor status do usuario
    payload = Mutation.update_user(user_id, user_name, friendshipness, new_humor)
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
    Pinga o luci pra ver se está acordada, retornando a versão do sistema.
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
async def user_status(bot):
    """
    Verifica o relatório de afeição que Luci possui de um determinado membro.

    Uso:
        !user @Username
    """
    mentions = bot.message.mentions
    if not mentions:
        return await bot.send(
            'Não sei de quem vc está falando. Marca ele tipo @Fulano.'
        )

    # consulta os membros no backend
    server = make_hash(bot.message.guild.name, bot.message.guild.id).decode('utf-8')
    user_id = make_hash(server, mentions[0].id).decode('utf-8')

    payload = Query.get_user(user_id)
    gql_client = get_gql_client(BACKEND_URL)
    try:
        response = gql_client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')
        return

    data = response.get('users', [])
    if not data:
        return await bot.send('Acho que não c-conheço... Desculpa.')

    # monta a resposta
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    name = data[0].get('name')
    friendshipness = data[0].get('friendshipness', 0)
    emotions = data[0].get('emotion_resume', {})
    user_id = extract_user_id(data[0]['reference'])

    # url do avatar do cidadão
    user = bot.guild._members.get(user_id)
    avatar_url = f'{user.avatar_url.BASE}/avatars/{user.id}/{user.avatar}'

    if not user:
        return await bot.send('Acho que não c-conheço... Desculpa.')

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
    embed.set_thumbnail(url=avatar_url)

    return await bot.send('', embed=embed)
