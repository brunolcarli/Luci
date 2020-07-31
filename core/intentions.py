"""
Defines possibile intention structure maps that Luci may identify.
"""
from core.enums import (GlobalIntentions, MyselfIntentions, AboutMyFriends,
                        AboutMyParents,StuffILike, GoodIntentions, BadIntentions)


class Intentions:
    global_intentions = {
        1: GlobalIntentions.ABOUT_MYSELF,
        2: GlobalIntentions.CORRECTION,
        3: GlobalIntentions.TASK,
        4: GlobalIntentions.GOOD_INTENTION,
        5: GlobalIntentions.BAD_INTENTION
    }

    about_myself_intentions = {
        1: MyselfIntentions.MY_AGE,
        2: MyselfIntentions.WHO_AM_I,
        3: MyselfIntentions.WHAT_AM_I,
        4: MyselfIntentions.HOW_IM_FEELING,
        5: MyselfIntentions.MY_GENDER,
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
    }

    # specific_intentions = {
    #     GlobalIntentions.ABOUT_MYSELF: about_myself_intentions,
    #     GlobalIntentions.ABOUT_MY_FRIENDS: about_my_friends_intentions,
    #     GlobalIntentions.ABOUT_MY_PARENTS: about_my_parents_intentions,
    #     GlobalIntentions.STUFF_I_LIKE: stuff_i_like_intentions,
    #     GlobalIntentions.BAD_INTENTION: bad_intentions,
    #     GlobalIntentions.GOOD_INTENTION: good_intentions,
    # }
