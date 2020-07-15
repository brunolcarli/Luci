import unittest
from core.classifiers import get_global_intention
from core.enums import GlobalIntentions
from core.utils import get_text_vector


class TestGlobalIntentionClassifier(unittest.TestCase):
    def test_predict_about_myself(self):
        """
        VerifY that the global intention classifier predicts correctly
        texts that refers to Luci attributes.
        """
        self.assertEqual(
            get_global_intention(get_text_vector('como é seu nome?')),
            GlobalIntentions.ABOUT_MYSELF
        )
        self.assertEqual(
            get_global_intention(get_text_vector('quantos anos vc tem?')),
            GlobalIntentions.ABOUT_MYSELF
        )
        self.assertEqual(
            get_global_intention(get_text_vector('vc é menino ou menina?')),
            GlobalIntentions.ABOUT_MYSELF
        )
        self.assertEqual(
            get_global_intention(get_text_vector('como está se sentindo?')),
            GlobalIntentions.ABOUT_MYSELF
        )

    def test_predict_about_friends(self):
        """
        Verify that the global intention classifier predicts correctly texts
        that refers to Luci's freiends.
        """
        self.assertEqual(
            get_global_intention(get_text_vector('vc tem amigos?')),
            GlobalIntentions.ABOUT_MY_FRIENDS
        )
        self.assertEqual(
            get_global_intention(get_text_vector('quem é seu melhor amigo?')),
            GlobalIntentions.ABOUT_MY_FRIENDS
        )
        self.assertEqual(
            get_global_intention(get_text_vector('nós somos amigos não somos?')),
            GlobalIntentions.ABOUT_MY_FRIENDS
        )

    def test_predict_about_my_parents(self):
        """
        Verify that the global intention classifier predicts correctly texts
        that refers to Luci's parentship.
        """
        self.assertEqual(
            get_global_intention(get_text_vector('você tem pai?')),
            GlobalIntentions.ABOUT_MY_PARENTS
        )
        self.assertEqual(
            get_global_intention(get_text_vector('você tem mãe?')),
            GlobalIntentions.ABOUT_MY_PARENTS
        )
        self.assertEqual(
            get_global_intention(get_text_vector('quem são seus pais')),
            GlobalIntentions.ABOUT_MY_PARENTS
        )

    def test_predict_about_sfuff_luci_likes(self):
        """
        Verify that the global intention classifier predicts correctly txts
        that refers to stuffs that Luci may like.
        """
        self.assertEqual(
            get_global_intention(get_text_vector('qual sua cor favorita?')),
            GlobalIntentions.STUFF_I_LIKE
        )
        self.assertEqual(
            get_global_intention(get_text_vector('você gosta de frutas?')),
            GlobalIntentions.STUFF_I_LIKE
        )
        self.assertEqual(
            get_global_intention(get_text_vector('gosta de brincadeiras')),
            GlobalIntentions.STUFF_I_LIKE
        )
        self.assertEqual(
            get_global_intention(get_text_vector('qual seu tipo de música favorito?')),
            GlobalIntentions.STUFF_I_LIKE
        )

    def test_predict_good_intentions(self):  # TODO
        pass

    def test_predict_bad_intentions(self):  # TODO
        pass
