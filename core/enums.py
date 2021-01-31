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


class BadIntentions(Enum):
    """
    Enumerates types of bad intentions.
    """
    SEXUAL_ABUSE = 'sex_abuse'
    RACISM_XENOPHOBIA = 'racism_and_xenophobia'
    SUICIDE = 'suicide'
    ILLEGAL_STUFF = 'illegal_stuff'
    THREAT = 'threat'
    FORBIDDEN = 'forbidden'
    VERBAL_OFFENSE = 'verbal_offense'


class GoodIntentions(Enum):
    """
    Enumerates types of good intentions.
    """
    PRAISE = 'praise'
    HELPFUL = 'helpful'
    GREETING = 'greeting'
    ACKNOWLEDGEMENT = 'acknowledgment'
    FUNNY = 'funny'
    SORRY = 'sorry'
    GOODBYE = 'goodbye'


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


class AboutMyParents(Enum):
    """
    Enumerates intentions refering to Luci parentship.
    """
    MY_MOTHER = 'my_mother'
    MY_DAD = 'my_dad'
    GRANDPA = 'grandpa'
    GRANDMA = 'grandma'
    RESPONSIBLE = 'responsible'


class AboutMyFriends(Enum):
    """
    Enumerates intentions refering to Luci's friendship.
    """
    FRIENDS_I_HAVE = 'friends_i_have'
    USERS_I_LIKE = 'users_i_like'
    USERS_I_DONT_LIKE = 'users_i_dont_like'
    BEST_FRIENDS = 'best_friends'


class StuffILike(Enum):
    """
    Enumerates stuff Luci may like.
    """
    FOOD = 'food'
    MUSIC = 'music'
    SPORTS_AND_PLAYING = 'sports_and_playing'
    TRAVELING = 'traveling'
