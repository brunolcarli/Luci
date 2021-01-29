"""
Defines requests, queries and connections to external platforms and services.
"""
import json
import requests
from gql import gql
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

        return 0

    @staticmethod
    def get_quotes(server):
        """
        Solicita os quotes de um servidor.
        """
        query = f'''
        query {{
            quotes(reference: "{server}"){{
                quote
            }}
        }}
        '''

        return gql(query)

    @staticmethod
    def get_emotions(server):
        """
        Solicita o estado emocional em um server ao backend.
        """
        query = f'''
        query emotions{{
            emotions(reference: "{server}"){{
                reference
                pleasantness
                attention
                sensitivity
                aptitude
            }}
        }}
        '''

        return gql(query)

    @staticmethod
    def get_pos(text):
        """
        Solicita o PART OF SPEECH de um texto para LISA.
        """
        query = f'''
        query{{
            partOfSpeech(text: "{text}") {{
                token
                description
            }}
        }}
        '''
        request = requests.post(LISA_URL, json={'query': query})

        if request.status_code == 200:
            return json.loads(request.text)

        return ''

    @staticmethod
    def get_user(reference):
        """
        Consulta um usuário por id de membro da guilda.
        """
        query = f'''
        query {{
        users(reference: "{reference}") {{
            reference
            name
            friendshipness
            emotion_resume {{
                reference
                pleasantness 
                attention
                sensitivity
                aptitude
                }}
            }}
        }}
        '''

        return gql(query)


    @staticmethod
    def get_users(server_id):
        """
        Consulta membros de um server que Luci conhece.
        """
        query = f'''
        query{{
            users(server_id: "{server_id}") {{
                reference
                name
                friendshipness
            }}
        }}
        '''
        return gql(query)


class Mutation:
    """
    Operações graphql de criação e alteração de dados.
    """

    @staticmethod
    def create_quote(message, server, author):
        """
        Solicita a criação de uma mensagem para um servidor.
        """
        mutation = f'''
        mutation {{
            create_quote(input:{{
                quote:"{message}"
                reference: "{server}"
                author: "{author}"
            }}){{
                quote{{
                    id
                    quote
                    reference
                    author
                }}
            }}
        }}
        '''

        return gql(mutation)

    @staticmethod
    def update_emotion(server, pleasantness=0, aptitude=0, attention=0, sensitivity=0):
        """
        Solicita a atualização do humor da luci em um servidor ao backend.
        """
        mutation = f'''
        mutation update{{
        emotion_update(input:{{
            reference: "{server}"
            pleasantness: {pleasantness}
            aptitude: {aptitude}
            attention: {attention}
            sensitivity: {sensitivity}
        }}) {{
            emotion{{
                reference
                pleasantness
                attention
                sensitivity
                aptitude
                }}
            }}
        }}
        '''

        return gql(mutation)

    @staticmethod
    def update_user(user_id, name, friendshipness, emotions, message=None):
        """
        Solicita a atualização do estado de um membro (usuário) do server.
        """
        pleasantness = emotions.get('pleasantness', 0)
        attention = emotions.get('attention', 0)
        sensitivity = emotions.get('sensitivity', 0)
        aptitude = emotions.get('aptitude', 0)

        if message:
            message_input = f'''
            message: {{
                global_intention: "{message.get('global_intention')}"
                specific_intention: "{message.get('specific_intention')}"
                text: "{message.get('text')}"
            }}
            '''
        else:
            message_input = ''

        mutation = f'''
        mutation {{
            update_user(input:{{
                reference: "{user_id}"
                name: "{name}"
                friendshipness: {friendshipness}
                emotion_resume: {{
                    pleasantness: {pleasantness}
                    attention: {attention}
                    sensitivity: {sensitivity}
                    aptitude: {aptitude}
                }}
                {message_input}
            }}){{
                user {{
                reference
                name
                friendshipness
                    emotion_resume {{
                        reference
                        pleasantness
                        attention
                        sensitivity
                        aptitude
                    }}
                }}
            }}
        }}
        '''

        return gql(mutation)
