import base64
from random import choice
from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from core.external_requests import Query
from core.output_vectors import intention_responses, intention_vectors


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
        return polarity


def answer_intention(text):
    """
    Responde de acordo com a intenção identificada, se identificada, do contrário
    retorna None.
    """
    for sample in intention_vectors:
        if sample['text'].lower() in text.lower() or text.lower() in sample['text'].lower():
            return choice(intention_responses[sample['intention']])

    return None


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
