import unittest
from core.classifiers import get_good_intention
from core.enums import GoodIntentions
from core.utils import get_text_vector


class TestGoodIntentionClassifier(unittest.TestCase):
    def test_predict_praise(self):
        self.assertEqual(
            get_good_intention(get_text_vector('ficou muito bom')),
            GoodIntentions.PRAISE
        )
        self.assertEqual(
            get_good_intention(get_text_vector('meus parabéns')),
            GoodIntentions.PRAISE
        )
        self.assertEqual(
            get_good_intention(get_text_vector('você é inteligente')),
            GoodIntentions.PRAISE
        )

    def test_predict_helpful(self):
        self.assertEqual(
            get_good_intention(get_text_vector('Veja no stack overflow')),
            GoodIntentions.HELPFUL
        )
        self.assertEqual(
            get_good_intention(get_text_vector('faz assim pra ver se funciona')),
            GoodIntentions.HELPFUL
        )
        self.assertEqual(
            get_good_intention(get_text_vector('tenta dessa forma')),
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
            get_good_intention(get_text_vector('Oi tudo bem?')),
            GoodIntentions.GREETING
        )

    def test_predict_acknowledgement(self):
        self.assertEqual(
            get_good_intention(get_text_vector('Ok obrigado')),
            GoodIntentions.ACKNOWLEDGEMENT
        )
        self.assertEqual(
            get_good_intention(get_text_vector('entende')),
            GoodIntentions.ACKNOWLEDGEMENT
        )
        self.assertEqual(
            get_good_intention(get_text_vector('blz entendi')),
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
        self.assertEqual(
            get_good_intention(get_text_vector('mds kkkk')),
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
        self.assertEqual(
            get_good_intention(get_text_vector('flw')),
            GoodIntentions.GOODBYE
        )
