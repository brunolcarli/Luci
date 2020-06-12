"""
Defines requests, queries and connections to external platforms and services.
"""
import json
import requests
from luci.settings import LISA_URL


class Query:
    """
    Groups GraphQl queries as static methods.
    """
    @staticmethod
    def get_text_offense(message):
        """
        Request LISA to verify if the text is offensive.
        """
        query = f'''
        query{{
            textOffenseLevel(text: {json.dumps(message)}) {{
                text
                average
                isOffensive
            }}
        }}
        '''
        request = requests.post(LISA_URL, json={'query': query})

        if request.status_code == 200:
            return json.loads(request.text)

        return None

    @staticmethod
    def get_text_sentiment(message):
        """
        Request LISA to extract the text sentiment polarity from message.
        """
        query = f'''
        query{{
            sentimentExtraction(text: {json.dumps(message)})
        }}
        '''
        request = requests.post(LISA_URL, json={'query': query})

        if request.status_code == 200:
            return json.loads(request.text)

        return None
