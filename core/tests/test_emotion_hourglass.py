import unittest
from core.emotions import EmotionHourglass


class TestEmotionHourglass(unittest.TestCase):
    def test_get_pleasantness(self):
        """
        Verify that the method that returns the pleasantness label
        works correcly based on the value inputed.
        """
        self.assertEqual(EmotionHourglass.get_pleasantness(-2.5), 'sadness')
        self.assertEqual(EmotionHourglass.get_pleasantness(-2), 'sadness')
        self.assertEqual(EmotionHourglass.get_pleasantness(-1.5), 'pensiveness')
        self.assertEqual(EmotionHourglass.get_pleasantness(-1), 'pensiveness')
        self.assertEqual(EmotionHourglass.get_pleasantness(-0.5), 'neutral')
        self.assertEqual(EmotionHourglass.get_pleasantness(0), 'neutral')
        self.assertEqual(EmotionHourglass.get_pleasantness(0.5), 'neutral')
        self.assertEqual(EmotionHourglass.get_pleasantness(1), 'serenity')
        self.assertEqual(EmotionHourglass.get_pleasantness(1.5), 'serenity')
        self.assertEqual(EmotionHourglass.get_pleasantness(2), 'joy')
        self.assertEqual(EmotionHourglass.get_pleasantness(2.5), 'joy')

    def test_get_attention(self):
        """
        Verify that the method that returns the attention label
        works correcly based on the value inputed.
        """
        self.assertEqual(EmotionHourglass.get_attention(-2.5), 'surprise')
        self.assertEqual(EmotionHourglass.get_attention(-2), 'surprise')
        self.assertEqual(EmotionHourglass.get_attention(-1.5), 'distraction')
        self.assertEqual(EmotionHourglass.get_attention(-1), 'distraction')
        self.assertEqual(EmotionHourglass.get_attention(-0.5), 'neutral')
        self.assertEqual(EmotionHourglass.get_attention(0), 'neutral')
        self.assertEqual(EmotionHourglass.get_attention(0.5), 'neutral')
        self.assertEqual(EmotionHourglass.get_attention(1), 'interest')
        self.assertEqual(EmotionHourglass.get_attention(1.5), 'interest')
        self.assertEqual(EmotionHourglass.get_attention(2), 'anticipation')
        self.assertEqual(EmotionHourglass.get_attention(2.5), 'anticipation')

    def test_get_sensitivity(self):
        """
        Verify that the method that returns the sensitivity label
        works correcly based on the value inputed.
        """
        self.assertEqual(EmotionHourglass.get_sensitivity(-2.5), 'fear')
        self.assertEqual(EmotionHourglass.get_sensitivity(-2), 'fear')
        self.assertEqual(EmotionHourglass.get_sensitivity(-1.5), 'aprehension')
        self.assertEqual(EmotionHourglass.get_sensitivity(-1), 'aprehension')
        self.assertEqual(EmotionHourglass.get_sensitivity(-0.5), 'neutral')
        self.assertEqual(EmotionHourglass.get_sensitivity(0), 'neutral')
        self.assertEqual(EmotionHourglass.get_sensitivity(0.5), 'neutral')
        self.assertEqual(EmotionHourglass.get_sensitivity(1), 'annoyance')
        self.assertEqual(EmotionHourglass.get_sensitivity(1.5), 'annoyance')
        self.assertEqual(EmotionHourglass.get_sensitivity(2), 'anger')
        self.assertEqual(EmotionHourglass.get_sensitivity(2.5), 'anger')

    def test_get_aptitude(self):
        """
        Verify that the method that returns the aptitude label
        works correcly based on the value inputed.
        """
        self.assertEqual(EmotionHourglass.get_aptitude(-2.5), 'disgust')
        self.assertEqual(EmotionHourglass.get_aptitude(-2), 'disgust')
        self.assertEqual(EmotionHourglass.get_aptitude(-1.5), 'boredom')
        self.assertEqual(EmotionHourglass.get_aptitude(-1), 'boredom')
        self.assertEqual(EmotionHourglass.get_aptitude(-0.5), 'neutral')
        self.assertEqual(EmotionHourglass.get_aptitude(0), 'neutral')
        self.assertEqual(EmotionHourglass.get_aptitude(0.5), 'neutral')
        self.assertEqual(EmotionHourglass.get_aptitude(1), 'acceptance')
        self.assertEqual(EmotionHourglass.get_aptitude(1.5), 'acceptance')
        self.assertEqual(EmotionHourglass.get_aptitude(2), 'trust')
        self.assertEqual(EmotionHourglass.get_aptitude(2.5), 'trust')
