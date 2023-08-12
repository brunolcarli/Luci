from random import choice
from core.utils import get_text_vector
from core.intentions import Intentions
from core.enums import GlobalIntentions
from core.output_vectors import intention_responses
from core.model_loader import IntentionClassifierModels
from core.external_requests import Query


def classifiers_map():
    return {
        GlobalIntentions.ABOUT_MYSELF: get_myself_intention,
        GlobalIntentions.ABOUT_MY_PARENTS: get_my_parents_intention,
        GlobalIntentions.ABOUT_MY_FRIENDS: get_my_friends_intention,
        GlobalIntentions.STUFF_I_LIKE: get_stuff_i_like_intention,
        GlobalIntentions.GOOD_INTENTION: get_good_intention,
        GlobalIntentions.BAD_INTENTION: get_bad_intention
    }


def get_global_intention(text_vector):
    """
    Returns the intention predicted from the text vector.

    param : text_vector : <list>
    return <Enum>
    """
    recognizer = IntentionClassifierModels.GLOBAL_INTENTIONS_MODEL
    return Intentions.global_intentions.get(
        recognizer.predict([text_vector])[0]
    )


def get_myself_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = IntentionClassifierModels.MYSELF_INTENTIONS_MODEL
    return Intentions.about_myself_intentions.get(
        recognizer.predict([text_vector])[0]
    )


def get_my_parents_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = IntentionClassifierModels.PARENTS_INTENTION_MODEL
    return Intentions.about_my_parents_intentions.get(
        recognizer.predict([text_vector])[0]
    )


def get_my_friends_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = IntentionClassifierModels.FRIENDS_INTENTION_MODEL
    return Intentions.about_my_friends_intentions.get(
        recognizer.predict([text_vector])[0]
    )


def get_stuff_i_like_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = IntentionClassifierModels.STUFF_I_LIKE_INTENTIONS_MODEL
    return Intentions.stuff_i_like_intentions.get(
        recognizer.predict([text_vector])[0]
    )


def get_good_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = IntentionClassifierModels.GOOD_INTENTIONS_MODEL
    return Intentions.good_intentions.get(recognizer.predict([text_vector])[0])


def get_bad_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = IntentionClassifierModels.BAD_INTENTIONS_MODEL
    return Intentions.bad_intentions.get(recognizer.predict([text_vector])[0])


def naive_response(text, **kwargs):
    """
    Mecanismo de resposta inocente.
    Recebe um texto e responde com uma resposta aleatoria para esta intenção.

    Descrito na documentação como "Algoritmo encadeado simples"
    https://github.com/brunolcarli/Luci/wiki/Arquitetura-do-sistema#algoritmo-encadeado-simples

    param: text: <str>
    return: <Str>
    """
    # extracts the text vector
    vector = get_text_vector(text)
    # maps the possible intentions
    network = classifiers_map()

    # predict the global intention
    global_intention = get_global_intention(vector)

    # get the specific intention classifier function
    specs = network.get(global_intention)

    # predict the specifc intention
    specific_intention = specs(vector)

    # gets a random answer for the specific intention
    response = intention_responses[global_intention][specific_intention]

    return response(**kwargs)


def get_intentions(text):
    """
    Returns both global and specific intentions from a text.
    """
    # preprocess input text
    text = Query.text_preprocess(text)

    # extracts the text vector
    vector = get_text_vector(text).toarray()

    # maps the possible intentions
    network = classifiers_map()

    # predict the global intention
    global_intention = get_global_intention(vector)

    # get the specific intention classifier function
    specs = network.get(global_intention)

    # predict the specifc intention
    specific_intention = specs(vector)

    return global_intention.value, specific_intention.value
