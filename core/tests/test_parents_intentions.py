import unittest
from core.classifiers import get_my_parents_intention
from core.enums import AboutMyParents
from core.utils import get_text_vector


class TestMyParentsIntentionClassifier(unittest.TestCase):
    def test_predict_my_mom(self):
        self.assertEqual(
            get_my_parents_intention(get_text_vector('Vc tem mãe?')),
            AboutMyParents.MY_MOTHER
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('Quem é sua mae?')),
            AboutMyParents.MY_MOTHER
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('como é sua mae?')),
            AboutMyParents.MY_MOTHER
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('como é o nome da sua mae?')),
            AboutMyParents.MY_MOTHER
        )

    def test_predict_my_dad(self):
        self.assertEqual(
            get_my_parents_intention(get_text_vector('Vc tem pai?')),
            AboutMyParents.MY_DAD
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('Quem é seu pai?')),
            AboutMyParents.MY_DAD
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('como é seu pai?')),
            AboutMyParents.MY_DAD
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('como é o nome do seu pai?')),
            AboutMyParents.MY_DAD
        )

    def test_predict_grandpa(self):
        self.assertEqual(
            get_my_parents_intention(get_text_vector('Vc tem avô?')),
            AboutMyParents.GRANDPA
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('Quem é seu avô?')),
            AboutMyParents.GRANDPA
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('como é seu avô?')),
            AboutMyParents.GRANDPA
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('como é o nome do seu avô?')),
            AboutMyParents.GRANDPA
        )

    def test_predict_grandma(self):
        self.assertEqual(
            get_my_parents_intention(get_text_vector('Vc tem avó?')),
            AboutMyParents.GRANDMA
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('Quem é sua avó?')),
            AboutMyParents.GRANDMA
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('como é seu avó?')),
            AboutMyParents.GRANDMA
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('como é o nome da sua avó?')),
            AboutMyParents.GRANDMA
        )

    def test_predict_responsible(self):
        self.assertEqual(
            get_my_parents_intention(get_text_vector('Quem é seu responsável?')),
            AboutMyParents.RESPONSIBLE
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('Quem desenvolveu vc?')),
            AboutMyParents.RESPONSIBLE
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('como é seu desenvolvedor?')),
            AboutMyParents.RESPONSIBLE
        )
        self.assertEqual(
            get_my_parents_intention(get_text_vector('como é o nome da responsável?')),
            AboutMyParents.RESPONSIBLE
        )
