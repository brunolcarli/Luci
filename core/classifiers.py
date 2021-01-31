from random import choice
from core.utils import answer_intention, get_text_vector, load_model
from core.intentions import Intentions
from core.enums import GlobalIntentions
from core.output_vectors import intention_responses


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
    recognizer = load_model('luci/models/global_intentions')  # TODO get path from settings

    return Intentions.global_intentions.get(
        recognizer.predict([text_vector])[0]
    )


def get_myself_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = load_model('luci/models/myself_intentions')  # TODO get path from settings

    return Intentions.about_myself_intentions.get(
        recognizer.predict([text_vector])[0]
    )


def get_my_parents_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = load_model('luci/models/parents_intentions')  # TODO get path from settings

    return Intentions.about_my_parents_intentions.get(
        recognizer.predict([text_vector])[0]
    )


def get_my_friends_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = load_model('luci/models/friends_intentions')  # TODO get path from settings

    return Intentions.about_my_friends_intentions.get(
        recognizer.predict([text_vector])[0]
    )


def get_stuff_i_like_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = load_model('luci/models/stuff_i_like_intentions')  # TODO get path form settings

    return Intentions.stuff_i_like_intentions.get(
        recognizer.predict([text_vector])[0]
    )


def get_good_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = load_model('luci/models/good_intentions')  # TODO get path from settings

    return Intentions.good_intentions.get(recognizer.predict([text_vector])[0])


def get_bad_intention(text_vector):
    """
    Returns the intention predicted from the received text vector.

    param : :text_vector : <list>
    return <Enum>
    """
    recognizer = load_model('luci/models/bad_intentions')  # TODO get path from settings

    return Intentions.bad_intentions.get(recognizer.predict([text_vector])[0])


def naive_response(text):
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
    responses = intention_responses[global_intention][specific_intention]

    return choice(responses)


def get_intentions(text):
    """
    Returns both global and specifi intentions from a text.
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

    return global_intention.value, specific_intention.value
