"""
Contains the trained models loaded and encapsulated in a class.
"""
import pickle
from core.training.text_gen import GenerativeModel, ddic, ddic_aux


def load_model(fpath):
    """
    Loads a trained machine learning model.

    param : fpath: <str> : file path to the model
    """
    with open(fpath, 'rb') as trained_model:
        model = pickle.load(trained_model)

    return model


class IntentionClassifierModels:
    """
    Models for intention classification.
    """
    GLOBAL_INTENTIONS_MODEL = load_model('luci/models/global_intentions')  # TODO get path from settings
    MYSELF_INTENTIONS_MODEL = load_model('luci/models/myself_intentions')  # TODO get path from settings
    PARENTS_INTENTION_MODEL = load_model('luci/models/parents_intentions')  # TODO get path from settings
    FRIENDS_INTENTION_MODEL = load_model('luci/models/friends_intentions')  # TODO get path from settings
    STUFF_I_LIKE_INTENTIONS_MODEL = load_model('luci/models/stuff_i_like_intentions')  # TODO get path form settings
    GOOD_INTENTIONS_MODEL = load_model('luci/models/good_intentions')  # TODO get path from settings
    BAD_INTENTIONS_MODEL = load_model('luci/models/bad_intentions')  # TODO get path from settings


class IntentionResponseGAN:
    """
    Models for text response generation.
    """
    WHO_AM_I_GAN = load_model('luci/models/who_am_i_response.model')
    ACKNOWLEDGEMENT_GAN = load_model('luci/models/acknowledgement_response.model')
    FORBIDDEN_GAN = load_model('luci/models/forbidden_response.model')
    FUNNY_GAN = load_model('luci/models/funny_response.model')
    GREETING_GAN = load_model('luci/models/greeting_response.model')
    HELPFUL_GAN = load_model('luci/models/helpful_response.model')
    ILLEGAL_STUFF_GAN = load_model('luci/models/illegal_stuff_response.model')
    MUSIC_GAN = load_model('luci/models/music_response.model')
    MY_AGE_GAN = load_model('luci/models/my_age_response.model')
    MY_GENDER_GAN = load_model('luci/models/my_gender_response.model')
    PRAISE_GAN = load_model('luci/models/praise_response.model')
    RACISM_XENOPHOBIA_GAN = load_model('luci/models/racism_xenophobia_response.model')
    SEXUAL_ABUSE_GAN = load_model('luci/models/sexual_abuse_response.model')
    SORRY_GAN = load_model('luci/models/sorry_response.model')
    SPORTS_AND_PLAYING_GAN = load_model('luci/models/sports_and_playing_response.model')
    SUICIDE_GAN = load_model('luci/models/suicide_response.model')
    TRHEAT_GAN = load_model('luci/models/threat_response.model')
    VERBAL_OFFENSE_GAN = load_model('luci/models/verbal_offense_response.model')
    WHAT_AM_I_GAN = load_model('luci/models/what_am_i_response.model')
    GOODBYE_GAN = load_model('luci/models/goodbye_response.model')


class LearnedResponses:
    def __init__(self):
        self.model = load_model('luci/models/learned_responses.model')

    def get_response(self, text):
        return self.model.predict_sentence(text)
