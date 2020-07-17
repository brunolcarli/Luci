import unittest
from core.classifiers import get_myself_intention
from core.enums import MyselfIntentions
from core.utils import get_text_vector


class TestMyselfIntentionClassifier(unittest.TestCase):
    def test_predict_my_age(self):
        """
        Verify that the classifier preedicts correctly text inputs that
        refers to Luci's age.
        """
        self.assertEqual(
            get_myself_intention(get_text_vector('quantos anos você tem?')),
            MyselfIntentions.MY_AGE
        )
        self.assertEqual(
            get_myself_intention(get_text_vector('qual é a sua idade?')),
            MyselfIntentions.MY_AGE
        )
        self.assertEqual(
            get_myself_intention(get_text_vector('quantos anos tem mesmo?')),
            MyselfIntentions.MY_AGE
        )

    def test_predict_who_am_i(self):
        """
        Verify that the classifier predicts correctly texts that refers to
        Luci's personality.
        """
        self.assertEqual(
            get_myself_intention(get_text_vector('qual é o seu nome?')),
            MyselfIntentions.WHO_AM_I
        )
        self.assertEqual(
            get_myself_intention(get_text_vector('como vc se chama?')),
            MyselfIntentions.WHO_AM_I
        )
        self.assertEqual(
            get_myself_intention(get_text_vector('quem é você?')),
            MyselfIntentions.WHO_AM_I
        )

    def test_predict_how_im_feeling(self):
        """
        Verify that the classifier predicts correctly texts that refers to
        Luci's feelings.
        """
        self.assertEqual(
            get_myself_intention(get_text_vector('tudo bem com vc?')),
            MyselfIntentions.HOW_IM_FEELING
        )
        self.assertEqual(
            get_myself_intention(get_text_vector('como você está?')),
            MyselfIntentions.HOW_IM_FEELING
        )
        self.assertEqual(
            get_myself_intention(get_text_vector('como está se sentindo?')),
            MyselfIntentions.HOW_IM_FEELING
        )

    def test_predict_gender(self):
        """
        Verify that the classifier predicts correctly texts that refers to
        Luci's feelings.
        """
        self.assertEqual(
            get_myself_intention(get_text_vector('vc é menino ou menina?')),
            MyselfIntentions.MY_GENDER
        )
        self.assertEqual(
            get_myself_intention(get_text_vector('vc é menino?')),
            MyselfIntentions.MY_GENDER
        )
        self.assertEqual(
            get_myself_intention(get_text_vector('vc é ele ou ela?')),
            MyselfIntentions.MY_GENDER
        )

    def test_predict_what_am_i(self):
        """
        Verify that the classifier predicts correctly texts that refers to
        Luci being.
        """
        self.assertEqual(
            get_myself_intention(get_text_vector('vc é uma criança?')),
            MyselfIntentions.WHAT_AM_I
        )
        self.assertEqual(
            get_myself_intention(get_text_vector('vc é uma pessoa?')),
            MyselfIntentions.WHAT_AM_I
        )
        self.assertEqual(
            get_myself_intention(get_text_vector('vc é um bot?')),
            MyselfIntentions.WHAT_AM_I
        )