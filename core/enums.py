from enum import Enum


class GlobalIntentions(Enum):
    """
    Wide abstract definition of global intentions.
    Gloabl intentions are a edge layer of intentions that may have subintentions
    which each one have their specificities and contexts.
    """
    ABOUT_MYSELF = 'about_myself'
    ABOUT_MY_FRIENDS = 'about_my_friends'
    ABOUT_THE_SERVER = 'about_the_server'
    ABOUT_THE_CHANNEL = 'about_the_channel'
    ABOUT_MY_PARENTS = 'about_my_parents'
    STUFF_I_LIKE = 'stuff_i_like'
    BAD_INTENTION = 'bad_intention'
    GOOD_INTENTION = 'good_intention'


class BadIntentions(Eum):
    """
    Enumerates types of bad intentions.
    """
    SEXUAL_ABUSE = 'sex_abuse'
    VERBAL_OFFENSE = 'verbal_offense'
    RACISM = 'racism'
    XENOPHOBIA = 'xenophobia'
    NIHILISM = 'nihilism'
    ILLEGAL_STUFF = 'illegal_stuff'
    THREAT = 'threat'
    FORBIDDEN = 'forbidden'


class GoodIntentions(Enum):
    """
    Enumerates types of good intentions.
    """
    PRAISE = 'praise'
    HELPFUL = 'helpful'
    GRETTING = 'greeting'
    ACKNOWLEDGEMENT = 'acknowledgment'
    FUNNY = 'funny'


class MyselfIntentions(Enum):
    """
    Enumerates the intentions that specifies questions about Luci herself,
    like her name, her age, her feelings and so on.
    """
    WHO_AM_I = 'who_am_i'
    WHAT_AM_I = 'what_ami'
    HOW_IM_FEELING = 'howimfeeling'
    MY_AGE = 'myage'
    MY_GENDER = 'mygender'


# TODO: define the other intentions


class Intentions(Enum):  # TODO: remove this
    WHO_AM_I = 'whoami'
    WHAT_AM_I = 'whatami'
    MY_PURPOSE = 'mypurpose'
    HOW_IM_FEELING = 'howimfeeling'
    MY_AGE = 'myage'
    MY_GENDER = 'mygender'