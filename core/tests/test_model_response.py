import unittest


class TestGetIntentionResponse(unittest.TestCase):
    def test_predict_my_age_intention(self):
        """
        Verify that the classifier for the intentionspecific  predictor classify
        correctly teh questions about Luci age and return one of the possible
        answers available on the specific intention output mapping list.
        """
        # self.assertEqual(
        #     get_myself_intention(get_text_vector('quantos anos você tem?')),
        #     MyselfIntentions.MY_AGE
        # )
        pass
