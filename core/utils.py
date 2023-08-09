from string import ascii_letters
from typing import Optional
import re
import base64
import pickle
from random import choice
import spacy
import wikipedia
from redis import Redis
from gql import Client
from deep_translator import GoogleTranslator
from gql.transport.requests import RequestsHTTPTransport
from core.external_requests import Query
from core.output_vectors import (intention_responses, opinions,
                                 propositions)
from core.types import CompressedDict
from luci.settings import REDIS_HOST, REDIS_PORT
from core.training.text_gen import GenerativeModel, ddic, ddic_aux

nlp = spacy.load('pt_core_news_sm')


def known_language_codes():
    """
    Returns a list of know language codes for translation.
    """
    return ['af', 'ga', 'sq', 'it', 'ar', 'ja', 'az', 'kn', 'eu',
            'ko', 'bn', 'la', 'be', 'lv','bg', 'lt', 'ca', 'mk',
            'ms', 'mt', 'hr', 'no', 'cs', 'fa', 'da', 'pl', 'nl',
            'pt', 'en', 'ro', 'eo', 'ru', 'et', 'sr', 'tl', 'sk',
            'fi', 'sl', 'fr', 'es', 'gl', 'sw', 'ka', 'sv', 'de',
            'ta', 'el', 'te', 'gu', 'th', 'ht', 'tr', 'iw', 'uk',
            'hi', 'ur', 'hu', 'vi', 'is', 'cy', 'id', 'yi']


def validate_text_offense(text):
    """
    Verify if an text message is offensive or not. Returns Tru if it is
    offensive text. Returns False if its not offensive.

    param : text : <str> : Text input;
    return: : <bool>
    """
    request_offenssivnes = Query.get_text_offense(text)
    if not request_offenssivnes:
        return False

    try:
        is_offensive = request_offenssivnes['data']['textOffenseLevel']['isOffensive']
    except KeyError:
        # In case of failure, like an naive child, take as False
        return False
    else:
        # Otherwise return the value calculated by LISA
        return is_offensive


def extract_sentiment(text):
    """
    Extracts sentiment polarity from text, returning a integer value
    between -1 and 1. In any failure case, consider it neutral (0).

    param : text : <str>
    return : <int>
    """
    request_sentiment = Query.get_text_sentiment(text)

    if not request_sentiment:
        return 0

    try:
        polarity = request_sentiment['data']['sentimentExtraction']
    except KeyError:
        return 0
    else:
        return polarity if polarity else 0

    return 0


def make_hash(descriptor, _id):
    """
    Criptografa um descritor e um id em uma hash base64
    args:
        descriptor : <str>
        id: <int> || <str>
    return: <str>
    """
    return base64.b64encode(b'%s' % f'{descriptor}:{_id}'.encode('utf-8'))


def get_gql_client(url, auth=None):
    """
    Retorna um client de execução de requisições graphql.
    param : auth : <str> : hash de autorização.
    """
    if not auth:
        transport = RequestsHTTPTransport(url=url, use_json=True)
    else:
        headers = {
            'content-type': 'application/json',
            'auth': '{}'.format(auth)
        }
        transport = RequestsHTTPTransport(
            url=url,
            use_json=True,
            headers=headers
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)
    return client


def get_text_vector(text):
    """
    Receives a string text input and returns its vector.
    """
    return nlp(text).vector


def remove_id(string):
    """
    Remove characteres between the delimiters "<" and ">"
    """
    string = re.sub(r'<(?<=\<)(.*?)(?=\>)>', '', string).lstrip()
    # lstrip() to remove leading whitespaces
                    
    return string


def get_wiki(text):
    """
    Return a list of explanations for a each term inputed.
    """
    error_response = ['N-não..', 'Não sei...']
    data = Query.get_pos(text)

    wiki = wikipedia
    wiki.set_lang('pt')

    if not data:
        return error_response

    tokens = [token['token'] for token in data['data']['partOfSpeech']
              if token['description'] == 'substantivo'
              or token['description'] == 'nome próprio']

    if len(tokens) > 3:
        return [get_random_blahblahblah()]

    try:
        response = [wiki.summary(token, sentences=2) for token in tokens]
    except (wiki.exceptions.DisambiguationError, wiki.exceptions.PageError):
        response = error_response

    return response


def extract_user_id(hash_id):
    """
    Extrai o id de membro da hash 'reference' do usuario.
    A hash é uma string base64.
    A hash contém dois dados (server_id, user_id), retorna-se apenas o user_id.

    param : hash_id : <str>
    return : <int>
    """
    _, uid = base64.b64decode(hash_id.encode('utf-8')).decode('utf-8').split(':')

    return int(uid)


def get_random_blahblahblah():
    """
    Retorna um papo filosófico aleatório.

    return: <str>
    """
    random_tought = ''.join(choice(i) for i in propositions)
    random_tought_2 = ''.join(choice(i) for i in propositions)

    response = f'{choice(opinions[0])}. '\
               f'{random_tought} '\
               f'{random_tought_2} Viajei né?'

    return response


def evaluate_math_expression(expression):
    """
    Retorna o resultado matemático de cálculos contidos na string.
    retorna 0 se não houver qualquer expressão matemática.
    param : expression : <str>
    return : <int>
    """
    valid_operators = (
        '+', '-', '*', '/', '>', '<', '=', '!', '(', ')', '.', '&'
    )
    word_switchs = {
        'maior': '>',
        'menor': '<',
        'igual': "=",
        'ou': 'or',
        'não': 'not',
        'diferente': '!=',
        'mais': '+',
        'menos': '-',
        'vezes': '*',
        'dividido': '/',
    }
    for word, switch in word_switchs.items():
        expression = expression.replace(word, switch)

    # calculates the probability of an "overcalculation"
    if (len(expression) + 1) / (len(expression) + 2) > 0.9:
        responses = [
            'bem, acho que não sei calcular tanta coisa assim',
            'sei lá, só tenho oito anos não sei fazer isso.'
        ]
        return choice(responses)

    filtered = ''.join(i for i in expression if i.isdigit() or i in valid_operators)

    try:
        result = eval(filtered)
    except SyntaxError:
        result = 0

    return result


def translate_text(text, lang):
    """
    Traduz um texto para uma outroa linguagem
    """
    return GoogleTranslator(target=lang).translate(text)


def get_short_memory_value(key: str) -> dict:
    """
    Recupera um valor da memória de curto prazo.
    Caso o valor não exista, retorna uma estrutura default
    """
    short_memory = Redis(REDIS_HOST, REDIS_PORT)
    memory = short_memory.get(key)

    if memory:
        return CompressedDict.decompress_bytes(memory)

    # Se não houver memórias vamos instanciar uma nova memória
    memory = {
        'last_message_dt': None,
        'last_quotes': [],
        'chat_log': [],
        'word_page': {}
    }
    short_memory.set(key, CompressedDict(memory).bit_string)

    return memory


def set_short_memory_value(key: str, value: Optional) -> bool:
    """
    Atualiza um valor da memória de curto prazo.
    """
    short_memory = Redis(REDIS_HOST, REDIS_PORT)
    result = short_memory.set(key, CompressedDict(value).bit_string)

    return result


def dist(a, b):
    """ Verifica a distancia entre duas letras do alfabeto """
    b_value = ascii_letters.index(b) + 1
    a_value = ascii_letters.index(a) + 1

    return abs(a_value - b_value)


def score(word):
    distances = 0
    if len(word) < 2:
        return 0

    for i in range(1, len(word)):
        distances += dist(word[i-1], word[i])

    return distances
