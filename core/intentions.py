"""
Defines possibile intention structure maps that Luci may identify.
"""
from core.enums import GlobalIntentions, MyselfIntentions


global_intentions = {
    1: GlobalIntentions.ABOUT_MYSELF,
    2: GlobalIntentions.ABOUT_MY_FRIENDS,
    3: GlobalIntentions.ABOUT_THE_SERVER,
    4: GlobalIntentions.ABOUT_THE_CHANNEL,
    5: GlobalIntentions.ABOUT_MY_PARENTS,
    6: GlobalIntentions.STUFF_I_LIKE,
}

specific_intentions = {
    GlobalIntentions.ABOUT_MYSELF: {
        1: MyselfIntentions.MY_AGE,
        2: MyselfIntentions.WHO_AM_I,
        3: MyselfIntentions.WHAT_AM_I,
        4: MyselfIntentions.HOW_IM_FEELING,
        5: MyselfIntentions.MY_GENDER,
    },
}
