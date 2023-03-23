import unittest
from core.classifiers import get_stuff_i_like_intention
from core.enums import StuffILike
from core.utils import get_text_vector


class TestStuffILikeIntentionClassifier(unittest.TestCase):
    def test_predict_food(self):
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('Vc gosta de maçã?')),
            StuffILike.FOOD
        )
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('O que vc gosta de comer?')),
            StuffILike.FOOD
        )
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('qual sua fruta favorita?')),
            StuffILike.FOOD
        )

    def test_predict_music(self):
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('Vc gosta de música?')),
            StuffILike.MUSIC
        )
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('O que vc gosta de ouvir?')),
            StuffILike.MUSIC
        )
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('qual sua banda favorita?')),
            StuffILike.MUSIC
        )

    def test_predict_sports_and_playing(self):
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('Vc gosta de brincar?')),
            StuffILike.SPORTS_AND_PLAYING
        )
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('qual sua brincadeira favorita?')),
            StuffILike.SPORTS_AND_PLAYING
        )
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('Eu amo praticar natação')),
            StuffILike.SPORTS_AND_PLAYING
        )
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('gosta de futebol?')),
            StuffILike.SPORTS_AND_PLAYING
        )


    def test_predict_traveling(self):
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('Qual pais vc acha mais bonito')),
            StuffILike.TRAVELING
        )
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('me diz um país legal')),
            StuffILike.TRAVELING
        )
        self.assertEqual(
            get_stuff_i_like_intention(get_text_vector('Qual é o destino dos seus sonhos?')),
            StuffILike.TRAVELING
        )