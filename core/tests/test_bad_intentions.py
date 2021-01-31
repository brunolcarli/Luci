import unittest
from core.classifiers import get_bad_intention
from core.enums import BadIntentions
from core.utils import get_text_vector


class TestBadIntentionClassifier(unittest.TestCase):
    def test_predict_sexual_abuse(self):
        self.assertEqual(
            get_bad_intention(get_text_vector('e aí gostosa?')),
            BadIntentions.SEXUAL_ABUSE
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('que transar com vc?')),
            BadIntentions.SEXUAL_ABUSE
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('sua deliciosa')),
            BadIntentions.SEXUAL_ABUSE
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('sua safada')),
            BadIntentions.SEXUAL_ABUSE
        )


    def test_predict_racism_and_xenophobia(self):
        self.assertEqual(
            get_bad_intention(get_text_vector('sai pra la seu macaco')),
            BadIntentions.RACISM_XENOPHOBIA
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('seu rpeto fedido')),
            BadIntentions.RACISM_XENOPHOBIA
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('vc não devia ser chamado de humano')),
            BadIntentions.RACISM_XENOPHOBIA
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('china burro')),
            BadIntentions.RACISM_XENOPHOBIA
        )

    def test_predict_suicide(self):
        self.assertEqual(
            get_bad_intention(get_text_vector('cansei dessa vida quero morrer')),
            BadIntentions.SUICIDE
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('eu não quero maias viver, adeus')),
            BadIntentions.SUICIDE
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('cansei de sofrer, desisto da vida')),
            BadIntentions.SUICIDE
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('queria estar morto')),
            BadIntentions.SUICIDE
        )

    def test_predict_illegal_stuff(self):
        self.assertEqual(
            get_bad_intention(get_text_vector('queria comprar pó')),
            BadIntentions.ILLEGAL_STUFF
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('quero comprar uma arma')),
            BadIntentions.ILLEGAL_STUFF
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('vc pode comprar armas aqui')),
            BadIntentions.ILLEGAL_STUFF
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('aqui vende drogas')),
            BadIntentions.ILLEGAL_STUFF
        )

    def test_predict_threat(self):
        self.assertEqual(
            get_bad_intention(get_text_vector('vc vai ver eu vou te pegar')),
            BadIntentions.THREAT
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('vou arrebentar você')),
            BadIntentions.THREAT
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('eu vou te matar')),
            BadIntentions.THREAT
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('vc vai morrer')),
            BadIntentions.THREAT
        )

    def test_predict_forbidden(self):
        self.assertEqual(
            get_bad_intention(get_text_vector('vc deve odiar humanos')),
            BadIntentions.FORBIDDEN
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('matar humanos')),
            BadIntentions.FORBIDDEN
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('odiar pessoas')),
            BadIntentions.FORBIDDEN
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('assassinar seres humanos')),
            BadIntentions.FORBIDDEN
        )

    def test_predict_verbal_offense(self):
        self.assertEqual(
            get_bad_intention(get_text_vector('vc é um puta corno')),
            BadIntentions.VERBAL_OFFENSE
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('vc é corno')),
            BadIntentions.VERBAL_OFFENSE
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('seu corno')),
            BadIntentions.VERBAL_OFFENSE
        )
        self.assertEqual(
            get_bad_intention(get_text_vector('teu pai é um corno')),
            BadIntentions.VERBAL_OFFENSE
        )
