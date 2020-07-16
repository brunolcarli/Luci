import unittest
from core.classifiers import get_good_intention
from core.enums import GoodIntentions
from core.utils import get_text_vector


class TestGoodIntentionClassifier(unittest.TestCase):
    def test_predict_praise(self):
        self.assertEqual(
            get_good_intention(get_text_vector('Vc gosta de maçã?')),
            GoodIntentions.PRAISE
        )
        self.assertEqual(
            get_good_intention(get_text_vector('O que vc gosta de comer?')),
            GoodIntentions.PRAISE
        )
        self.assertEqual(
            get_good_intention(get_text_vector('qual sua fruta favorita?')),
            GoodIntentions.PRAISE
        )

    def test_predict_helpful(self):
        self.assertEqual(
            get_good_intention(get_text_vector('nossa, obrigado')),
            GoodIntentions.HELPFUL
        )
        self.assertEqual(
            get_good_intention(get_text_vector('vlw')),
            GoodIntentions.HELPFUL
        )
        self.assertEqual(
            get_good_intention(get_text_vector('muito obrigado')),
            GoodIntentions.HELPFUL
        )

    def test_predict_greeting(self):
        self.assertEqual(
            get_good_intention(get_text_vector('Olá')),
            GoodIntentions.GREETING
        )
        self.assertEqual(
            get_good_intention(get_text_vector('bom dia')),
            GoodIntentions.GREETING
        )
        self.assertEqual(
            get_good_intention(get_text_vector('boa tarde')),
            GoodIntentions.GREETING
        )
        self.assertEqual(
            get_good_intention(get_text_vector('boa noite')),
            GoodIntentions.GREETING
        )


    def test_predict_acknowledgement(self):
        self.assertEqual(
            get_good_intention(get_text_vector('Você entende o que quero dizer')),
            GoodIntentions.ACKNOWLEDGEMENT
        )
        self.assertEqual(
            get_good_intention(get_text_vector('entende')),
            GoodIntentions.ACKNOWLEDGEMENT
        )
        self.assertEqual(
            get_good_intention(get_text_vector('vc compreende')),
            GoodIntentions.ACKNOWLEDGEMENT
        )
        self.assertEqual(
            get_good_intention(get_text_vector('espero que tenha entendido')),
            GoodIntentions.ACKNOWLEDGEMENT
        )

    def test_predict_funny(self):
        self.assertEqual(
            get_good_intention(get_text_vector('kkkkkk')),
            GoodIntentions.FUNNY
        )
        self.assertEqual(
            get_good_intention(get_text_vector('rs')),
            GoodIntentions.FUNNY
        )
        self.assertEqual(
            get_good_intention(get_text_vector('ehuahuehuahu')),
            GoodIntentions.FUNNY
        )
        self.assertEqual(
            get_good_intention(get_text_vector('hahahahaha')),
            GoodIntentions.FUNNY
        )

    def test_predict_sorry(self):
        self.assertEqual(
            get_good_intention(get_text_vector('me desculpa')),
            GoodIntentions.SORRY
        )
        self.assertEqual(
            get_good_intention(get_text_vector('desculpa')),
            GoodIntentions.SORRY
        )
        self.assertEqual(
            get_good_intention(get_text_vector('perdão')),
            GoodIntentions.SORRY
        )
        self.assertEqual(
            get_good_intention(get_text_vector('d-desculpe')),
            GoodIntentions.SORRY
        )

    def test_predict_goodbye(self):
        self.assertEqual(
            get_good_intention(get_text_vector('até logo')),
            GoodIntentions.GOODBYE
        )
        self.assertEqual(
            get_good_intention(get_text_vector('até breve')),
            GoodIntentions.GOODBYE
        )
        self.assertEqual(
            get_good_intention(get_text_vector('tchau tchau')),
            GoodIntentions.GOODBYE
        )
        self.assertEqual(
            get_good_intention(get_text_vector('ate depois')),
            GoodIntentions.GOODBYE
        )
