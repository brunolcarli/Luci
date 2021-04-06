"""
Contains the trained models loaded and encapsulated in a class.
"""
import pickle


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
    WHO_AM_I_GAN = load_model('luci/models/who_am_i_gan')
    ACKNOWLEDGEMENT_GAN = load_model('luci/models/acknowledgement')
    FORBIDDEN_GAN = load_model('luci/models/forbidden')
    FUNNY_GAN = load_model('luci/models/funny')
    GREETING_GAN = load_model('luci/models/greeting')
    HELPFUL_GAN = load_model('luci/models/helpful')
    ILLEGAL_STUFF_GAN = load_model('luci/models/illegal_stuff')
    MUSIC_GAN = load_model('luci/models/music')
    MY_AGE_GAN = load_model('luci/models/my_age')
    MY_GENDER_GAN = load_model('luci/models/my_gender')
    PRAISE_GAN = load_model('luci/models/praise')
    RACISM_XENOPHOBIA_GAN = load_model('luci/models/racism_xenophobia')
    SEXUAL_ABUSE_GAN = load_model('luci/models/sexual_abuse')
    SORRY_GAN = load_model('luci/models/sorry')
    SPORTS_AND_PLAYING_GAN = load_model('luci/models/sports_and_playing')
    SUICIDE_GAN = load_model('luci/models/suicide')
    TRHEAT_GAN = load_model('luci/models/threat')
    VERBAL_OFFENSE_GAN = load_model('luci/models/verbal_offense')
    WHAT_AM_I_GAN = load_model('luci/models/what_am_i')
    GOODBYE_GAN = load_model('luci/models/goodbye')
