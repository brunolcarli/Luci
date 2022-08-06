import re
from collections import Counter
import logging
from random import choice, randint, random
import spacy
import redis
import discord
from discord import ActionRow, Button, ButtonStyle
from discord.ext import commands, tasks
from dateutil import parser
from datetime import datetime, timezone
from core.classifiers import naive_response, get_intentions
from core.output_vectors import (offended, indifference, positive_answers,
                                 negative_answers, bored_messages)
from core.reinforcement import generate_answer
from core.external_requests import Query, Mutation
from core.emotions import change_humor_values, EmotionHourglass
from core.utils import (validate_text_offense, extract_sentiment,
                        make_hash, get_gql_client, remove_id, get_wiki,
                        get_random_blahblahblah, extract_user_id,
                        evaluate_math_expression, known_language_codes, translate_text,
                        get_short_memory_value, set_short_memory_value, score)
from core.gans import ResponseGenerator
from luci.settings import __version__, BACKEND_URL, REDIS_HOST, REDIS_PORT


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
            main_channel = server_config.get('main_channel')

            if not main_channel:
                continue

            channel = client.get_channel(int(main_channel))

            # data da última mensagem enviada no server
            guild_memory = self.short_memory.get(guild.id)
            if guild_memory:
                try:
                    last_message_dt = parser.parse(g)
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
                        memory = get_short_memory_value(server)
                        memory['last_message_dt'] = str(now.astimezone(tz=timezone.utc))
                        set_short_memory_value(server, memory)

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

        self.guilds = client.guilds


@client.on_click()
async def word_page_down(interaction: discord.Interaction, button):
    global page_key
    global previous_output

    key, index = page_key.split('_:_')
    server = make_hash('id', interaction.guild_id).decode('utf-8')
    memory = get_short_memory_value(server)
    page = memory.get('word_page', {})
    data = page.get(key, [])

    index = int(index) - 1
    if index < 0:
        index = len(data) - 1
    await interaction.defer()

    page_key = f'{key}_:_{index}'
    switch = {
        'token': 'Termo',
        'language': 'Idioma',
        'pos_tag': 'Etiqueta Morfossintática',
        'lemma': 'Radical',
        'polarity': 'Polaridade',
        'length': 'N˚ letras',
        'meanings': 'Significados',
        'entity': 'Entidade nomeada'
    }
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    word = data[index]
    for k, v in word.items():
        if k == 'meanings':
            value = ''
            for i in v:
                value += f'Contexto: {i["context"]}\nDefinição: {i["meaning"]}\n\n'
            v = value
        k = switch.get(k, k)
        embed.add_field(name=k, value=(v or '?'), inline=True)

    await previous_output.edit(content=f'Termo {index+1}/{len(data)}', embed=embed)


@client.on_click()
async def word_page_up(interaction: discord.Interaction, button):
    global page_key
    global previous_output

    key, index = page_key.split('_:_')
    server = make_hash('id', interaction.guild_id).decode('utf-8')
    memory = get_short_memory_value(server)
    page = memory.get('word_page', {})
    data = page.get(key, [])

    index = int(index) + 1
    if index > len(data) - 1:
        index = 0
    await interaction.defer()

    page_key = f'{key}_:_{index}'
    switch = {
        'token': 'Termo',
        'language': 'Idioma',
        'pos_tag': 'Etiqueta Morfossintática',
        'lemma': 'Radical',
        'polarity': 'Polaridade',
        'length': 'N˚ letras',
        'meanings': 'Significados',
        'entity': 'Entidade nomeada'
    }
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    word = data[index]
    for k, v in word.items():
        if k == 'meanings':
            value = ''
            for i in v:
                value += f'Contexto: {i["context"]}\nDefinição: {i["meaning"]}\n\n'
            v = value
        k = switch.get(k, k)
        embed.add_field(name=k, value=(v or '?'), inline=True)

    await previous_output.edit(content=f'Termo {index+1}/{len(data)}', embed=embed)


@client.event
async def on_member_join(member):
    """
    Greets the new member.
    """
    # Gets an hello
    message = ResponseGenerator.get_greeting_response()
    server_reference = make_hash('id', int(member.guild.id))
    query = Query.get_custom_config(server_reference)
    gql_client = get_gql_client(BACKEND_URL)
    try:
        response = gql_client.execute(query)
    except:
        log.error(f'Cant get server {server_reference} config. Skipping!')
        return None

    server_config = response.get('custom_config')
    channel = client.get_channel(int(server_config.get('main_channel')))
    if channel:
        await channel.send('https://media.discordapp.net/attachments/590678517407285251/865606198341926912/jerry.gif?width=979&height=466')
        await channel.send(f'{message} bem vinde.')


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

    text = message.content
    noises = ['\n', '"', "'"]
    for noise in noises:
        text = re.sub(noise, ' ', text).strip()
    global_intention, specific_intention = get_intentions(text)
    is_offensive = validate_text_offense(text)
    text_pol = extract_sentiment(text)
    user_name = message.author.name
    new_humor = change_humor_values(text_pol, is_offensive)
    friendshipness = (randint(-1, 1) * random()) + text_pol
    msg = {
        'global_intention': global_intention,
        'specific_intention': specific_intention,
        'text': text
    }
    gql_client = get_gql_client(BACKEND_URL)

    # não processa comandos
    for punct in '.>@,/?:;!}{[]|)(*&^%$#~':
        if text.startswith(punct):
            log.info('Skipping command text process.')
            return None

    # não processa links
    if text.startswith('http'):
        log.info('Skipping hyperlink text process.')
        return None

    server = make_hash('id', message.guild.id).decode('utf-8')
    memory = get_short_memory_value(server)

    # guarda a data da mensagem como valor para o id da guilda
    memory['last_message_dt'] = str(message.created_at)
    chat_log = memory.get('chat_log', [])
    log.info(memory)
    # caso a mensagem seja do mesmo usuario da mensagem anterior, anexa o texto
    if len(chat_log) > 1:
        if chat_log[-1]['author'] == message.author.name:
            chat_log[-1]['text'] += f' {text}'
        else:
            previous = chat_log[-1]
            chat_log.append({
                'author': message.author.name,
                'text': text
            })

            # assume a mensagem do proximo membro como resposta
            payload = Mutation.assign_response(
                text=previous['text'],
                possible_response=msg
            )
            try:
                gql_client.execute(payload)
            except Exception as err:
                log.error(f'Erro: {str(err)}\n\n')
            else:
                log.info('Saved a possible response.')

    else:
        chat_log.append({
            'author': message.author.name,
            'text': text
        })

    # mantem um maximo de 10 mensagens do chat na lembrança
    if len(chat_log) > 10:
        chat_log.pop(0)

    memory['chat_log'] = chat_log
    set_short_memory_value(server, memory)

    user_id = make_hash(server, message.author.id).decode('utf-8')

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

    # Atualiza reconhecimento de respostas, se for resposta à outra mensagem
    if message.reference:
        payload = Mutation.assign_response(
            text=message.reference.resolved.content,
            possible_response=msg
        )

        try:
            gql_client.execute(payload)
        except Exception as err:
            log.error(f'Erro: {str(err)}\n\n')

    # process @Luci mentions
    if str(channel.guild.me.id) in text:
        answer = generate_answer(text)
        if answer:
            return await channel.send(answer)

        # Caso não conheça nenhuma resposta, use o classificador inocente
        return await channel.send(
            naive_response(remove_id(text), reference=server)
        )

    if is_offensive and choice([1, 0]) and choice([1, 0]):
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

    # sorteia um quote vindo da memória de longo rpazo
    chosen_quote = choice(quotes)
    # recupera os últimos quotes ditos nesse server da memória de curto prazo
    server_memory = get_short_memory_value(server)

    # se o quote sorteado não for um quote repetido
    if chosen_quote['quote'] not in server_memory.get('last_quotes', []):
        # atualiza memória de curto prazo e retorna o quote sorteado
        server_memory['last_quotes'].append(chosen_quote['quote'])
        if len(server_memory['last_quotes']) > 10:
            server_memory['last_quotes'].pop(0)
        set_short_memory_value(server, server_memory)
        return await bot.send(f'{chosen_quote["quote"]} ~ {chosen_quote["author"]}')

    # se ela souber menos que 10 quotes nesse server pode retornar o quote repetido mesmo
    if len(quotes) < 10:
        return await bot.send(f'{chosen_quote["quote"]} ~ {chosen_quote["author"]}')

    # Se não tem que ir sorteando quotes até não ser repetido
    while chosen_quote['quote'] in server_memory['last_quotes']:
        chosen_quote = choice(quotes)

    # Atualiza a memória de curto rpazo ao selecionar o quote
    server_memory['last_quotes'].append(chosen_quote['quote'])
    if len(server_memory['last_quotes']) > 10:
        server_memory['last_quotes'].pop(0)
    set_short_memory_value(server, server_memory)

    return await bot.send(f'{chosen_quote["quote"]} ~ {chosen_quote["author"]}')


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

    server = make_hash('id', ctx.guild.id)
    payload = Mutation.create_quote(message, server.decode('utf-8'), author)
    client = get_gql_client(BACKEND_URL)

    try:
        response = client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')
        return await ctx.send('Buguei')

    quote = response['create_quote'].get('quote')
    embed = discord.Embed(color=0x1E1E1E, type="rich")
    embed.add_field(name='Entendi:', value=quote.get('quote'), inline=True)
    return await ctx.send('Ok:', embed=embed)


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
        return await ctx.send(
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


@client.command()
@commands.is_owner()
async def leave_guild(ctx, *, guild_reference=None):
    """
    Comando restrito: Faz a Luci sair de um servidor indesejado.
    """
    if not guild_reference:
        return await ctx.send(
            'Tem que me dizer o nome ou id do server né :rolling_eyes:'
        )

    guild_by_name = discord.utils.get(client.guilds, name=guild_reference)
    guild_by_id = client.get_guild(int(guild_reference))
    if guild_by_name is None and guild_by_id is None:
        return await ctx.send('Hmm não conheço esse server.')

    guild = guild_by_name or guild_by_id
    await client.get_guild(guild.id).leave()
    await ctx.send(f":ok_hand: pulei fora do server: {guild.name} ({guild.id})")


@client.command()
@commands.is_owner()
async def list_guilds(ctx):
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    for guild in client.guilds:
        embed.add_field(name=guild.name, value=guild.id, inline=True)

    await ctx.send('Lista de servers que eu estou:', embed=embed)


@client.command(aliases=['agm'])
async def anagram(ctx, word=None):
    """
    Lista anagramas para a palavra fornecida a partir da base de palavras
    conhecidas pela Luci.

    Uma palavra composta por mais de uma letra é necessária neste comando!
    Exemplo:
        !anagram pato
    """
    if not word:
        return await ctx.send('Me fale uma palavra.')

    if len(word) < 2:
        return await ctx.send('Essa palavra é muito pequena, me diz uma com mais letras.')

    word = word.lower()
    payload = Query.words_for_anagram(word)
    client = get_gql_client(BACKEND_URL)

    try:
        response = client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')
        return await ctx.send('Buguei')

    words = response.get('words')
    if not words:
        return await ctx.send('Ah, não conheço anagramas para esta palavra.')
    pattern = Counter(word)
    anagrams = [(i['token'], score(i['token'])) for i in words
                if i['token'] != word and Counter(i['token']) == pattern]

    if not anagrams:
        return await ctx.send('Ah, não conheço anagramas para esta palavra.')

    # sort by word score
    anagrams = sorted(anagrams, key=lambda k: k[1], reverse=True)
    
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    for anagram in anagrams[:10]:
        embed.add_field(name=anagram[0], value=f'Score: {anagram[1]}', inline=True)

    await ctx.send(f'Top 10 anagramas para {word}', embed=embed)


@client.command(aliases=['am'])
async def add_meaning(ctx, word=None, *args):
    if not word:
        return await ctx.send('Qual palavra?')
    if not args:
        return await ctx.send('Qual contexto e significado dessa palavra?')
    try:
        context, meaning = ' '.join(args).strip().lower().split(';;')
    except ValueError:
        return await ctx.send('Preciso que me diga um contexto e significado, separado por `;;`')

    payload = Mutation.add_meaning(word, context, meaning)
    client = get_gql_client(BACKEND_URL)

    try:
        response = client.execute(payload)
    except Exception as err:
        print(f'Erro: {str(err)}\n\n')
        return await ctx.send('Buguei')

    embed = discord.Embed(color=0x1E1E1E, type='rich')
    for option in response['add_meaning']['word']['meanings']:
        embed.add_field(name=f'Context: {option["context"]}', value=f'Meaning: {option["meaning"]}', inline=False)

    return await ctx.send(f'Legal, aprendi um significado pra palavra {word}:', embed=embed)


@client.command(aliases=['wd', 'wds'])
async def words(ctx, part=None):
    if not part:
        return await ctx.send('Mas diz uma palavra')

    global previous_output
    global page_key
    # global ctxn
    # ctxn = ctx
    page_key = f'{ctx.author.id}_:_0'
    server = make_hash('id', ctx.message.guild.id).decode('utf-8')
    memory = get_short_memory_value(server)
    page = memory.get('word_page', {})
    data = page.get(f'{ctx.author.id}', {})
    
    if not data:
        payload = Query.words(part)
        client = get_gql_client(BACKEND_URL)

        try:
            response = client.execute(payload)
        except Exception as err:
            log.error(f'Erro: {str(err)}\n\n')
            return await ctx.send('Buguei')

        words = response.get('words')
        if not words:
            return await ctx.send('Não conheço nada parecido...')

        data = words
        page[f'{ctx.author.id}'] = data
        memory['word_page'] = page
        set_short_memory_value(server, memory)
    else:
        words = data

    switch = {
        'token': 'Termo',
        'language': 'Idioma',
        'pos_tag': 'Etiqueta Morfossintática',
        'lemma': 'Radical',
        'polarity': 'Polaridade',
        'length': 'N˚ letras',
        'meanings': 'Significados',
        'entity': 'Entidade nomeada'
    }

    # Button definition
    components=[
        ActionRow(
            Button(
                style=ButtonStyle.gray,
                custom_id='word_page_up',
                label='▲'  # U+25B2
            ),
            Button(
                style=ButtonStyle.gray,
                custom_id='word_page_down',
                label='▼'  # U+25BC
            ),
        ),
    ]

    embed = discord.Embed(color=0x1E1E1E, type='rich')
    for k, v in words[0].items():
        if k == 'meanings':
            value = ''
            for i in v:
                value += f'Contexto: {i["context"]}\nDefinição: {i["meaning"]}\n\n'
            v = value
        k = switch.get(k, k)
        embed.add_field(name=k, value=(v or '?'), inline=True)
    previous_output = await ctx.send(
        f'Termo 1/{len(data)}',
        embed=embed,
        components=components
    )

