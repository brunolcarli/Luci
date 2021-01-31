"""
Defines possibile intention structure maps that Luci may identify.
"""
from core.enums import (GlobalIntentions, MyselfIntentions, AboutMyFriends,
                        AboutMyParents,StuffILike, GoodIntentions, BadIntentions)


class Intentions:
    global_intentions = {
        1: GlobalIntentions.ABOUT_MYSELF,
        2: GlobalIntentions.ABOUT_MY_FRIENDS,
        3: GlobalIntentions.ABOUT_MY_PARENTS,
        4: GlobalIntentions.STUFF_I_LIKE,
        5: GlobalIntentions.GOOD_INTENTION,
        6: GlobalIntentions.BAD_INTENTION
    }

    about_myself_intentions = {
        1: MyselfIntentions.MY_AGE,
        2: MyselfIntentions.WHO_AM_I,
        3: MyselfIntentions.WHAT_AM_I,
        4: MyselfIntentions.HOW_IM_FEELING,
        5: MyselfIntentions.MY_GENDER,
    }

    about_my_parents_intentions = {
        1: AboutMyParents.MY_MOTHER,
        2: AboutMyParents.MY_DAD,
        3: AboutMyParents.GRANDPA,
        4: AboutMyParents.GRANDMA,
        5: AboutMyParents.RESPONSIBLE
    }

    about_my_friends_intentions = {
        1: AboutMyFriends.FRIENDS_I_HAVE,
        2: AboutMyFriends.USERS_I_LIKE,
        3: AboutMyFriends.USERS_I_DONT_LIKE,
        4: AboutMyFriends.BEST_FRIENDS
    }

    stuff_i_like_intentions = {
        1: StuffILike.FOOD,
        2: StuffILike.MUSIC,
        3: StuffILike.SPORTS_AND_PLAYING, 
        4: StuffILike.TRAVELING,
    }

    good_intentions = {
        1: GoodIntentions.PRAISE,
        2: GoodIntentions.HELPFUL,
        3: GoodIntentions.GREETING,
        4: GoodIntentions.ACKNOWLEDGEMENT,
        5: GoodIntentions.FUNNY,
        6: GoodIntentions.SORRY,
        7: GoodIntentions.GOODBYE
    }

    bad_intentions = {
        1: BadIntentions.SEXUAL_ABUSE,
        2: BadIntentions.RACISM_XENOPHOBIA,
        3: BadIntentions.SUICIDE,
        4: BadIntentions.ILLEGAL_STUFF,
        5: BadIntentions.THREAT,
        6: BadIntentions.FORBIDDEN,
        7: BadIntentions.VERBAL_OFFENSE
    }

    specific_intentions = {
        GlobalIntentions.ABOUT_MYSELF: about_myself_intentions,
        GlobalIntentions.ABOUT_MY_FRIENDS: about_my_friends_intentions,
        GlobalIntentions.ABOUT_MY_PARENTS: about_my_parents_intentions,
        GlobalIntentions.STUFF_I_LIKE: stuff_i_like_intentions,
        GlobalIntentions.BAD_INTENTION: bad_intentions,
        GlobalIntentions.GOOD_INTENTION: good_intentions,
    }
