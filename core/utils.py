from core.external_requests import Query


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
