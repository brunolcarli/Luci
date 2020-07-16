import unittest
from core.classifiers import get_my_friends_intention
from core.enums import AboutMyFriends
from core.utils import get_text_vector


class TestMyFriendsIntentionClassifier(unittest.TestCase):
    def test_predict_friends_have(self):
        self.assertEqual(
            get_my_friends_intention(get_text_vector('Nós somos amigos né?')),
            AboutMyFriends.FRIENDS_I_HAVE
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('Vc tem amigos?')),
            AboutMyFriends.FRIENDS_I_HAVE
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('vc tem mtos amigos?')),
            AboutMyFriends.FRIENDS_I_HAVE
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('vamos ser amigos')),
            AboutMyFriends.FRIENDS_I_HAVE
        )

    def test_predict_users_i_like(self):
        self.assertEqual(
            get_my_friends_intention(get_text_vector('Vc gosta do fulano?')),
            AboutMyFriends.USERS_I_LIKE
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('o que vc acha do ciclano?')),
            AboutMyFriends.USERS_I_LIKE
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('vc é amiga do toninho?')),
            AboutMyFriends.USERS_I_LIKE
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('me fala alguem que vc gosta')),
            AboutMyFriends.USERS_I_LIKE
        )

    def test_predict_users_i_dont_like(self):
        self.assertEqual(
            get_my_friends_intention(get_text_vector('Vc não gosta do fulano?')),
            AboutMyFriends.USERS_I_DONT_LIKE
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('vc nao curte ciclano?')),
            AboutMyFriends.USERS_I_DONT_LIKE
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('vc não é amiga do toninho?')),
            AboutMyFriends.USERS_I_DONT_LIKE
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('me fala alguem que vc não gosta')),
            AboutMyFriends.USERS_I_DONT_LIKE
        )

    def test_predict_my_best_friends(self):
        self.assertEqual(
            get_my_friends_intention(get_text_vector('Quem é seu melhor amigo?')),
            AboutMyFriends.BEST_FRIENDS
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('quem é sua melhor amiga?')),
            AboutMyFriends.BEST_FRIENDS
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('Vc tem um melhor amigo?')),
            AboutMyFriends.BEST_FRIENDS
        )
        self.assertEqual(
            get_my_friends_intention(get_text_vector('melhores amigos')),
            AboutMyFriends.BEST_FRIENDS
        )
