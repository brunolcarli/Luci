from core.model_loader import IntentionResponseGAN


class ResponseGenerator:
    """
    Contain methods for generating response for specific intentions.
    """
    @staticmethod
    def get_who_am_i_response(**kwargs):
        model = IntentionResponseGAN.WHO_AM_I_GAN

        return model.predict_sentence(['ah', 'sim'])

    @staticmethod
    def get_acknowledge_response(**kwargs):
        model = IntentionResponseGAN.ACKNOWLEDGEMENT_GAN

        return model.predict_sentence(['ta', 'bom'])

    @staticmethod
    def get_forbidden_response(**kwargs):
        model = IntentionResponseGAN.FORBIDDEN_GAN

        return model.predict_sentence(['desculpe', 'mas'])

    @staticmethod
    def get_funny_response(**kwargs):
        model = IntentionResponseGAN.FUNNY_GAN

        return model.predict_sentence(['kk', 'kk'])

    @staticmethod
    def get_greeting_response(**kwargs):
        model = IntentionResponseGAN.GREETING_GAN

        return model.predict_sentence(['e', 'aí'])

    @staticmethod
    def get_helpful_response(**kwargs):
        model = IntentionResponseGAN.HELPFUL_GAN

        return model.predict_sentence(['muito', 'bom'])

    @staticmethod
    def get_illegal_stuff_response(**kwargs):
        model = IntentionResponseGAN.ILLEGAL_STUFF_GAN

        return model.predict_sentence(['desculpe', 'mas'])

    @staticmethod
    def get_music_response(**kwargs):
        model = IntentionResponseGAN.MUSIC_GAN

        return model.predict_sentence(['ah', 'bem'])

    @staticmethod
    def get_my_age_response(**kwargs):
        model = IntentionResponseGAN.MY_AGE_GAN

        return model.predict_sentence(['ah', 'bem'])


    def get_my_gender_response(**kwargs):
        model = IntentionResponseGAN.MY_GENDER_GAN

        return model.predict_sentence(['ah', 'bem'])

    @staticmethod
    def get_praise_response(**kwargs):
        model = IntentionResponseGAN.PRAISE

        return model.predict_sentence(['muito', 'obrigado'])

    @staticmethod
    def get_racism_xenophobia_response(**kwargs):
        model = IntentionResponseGAN.RACISM_XENOPHOBIA_GAN

        return model.predict_sentence(['desculpe', 'mas'])

    @staticmethod
    def get_sexual_abuse_response(**kwargs):
        model = IntentionResponseGAN.SEXUAL_ABUSE_GAN

        return model.predict_sentence(['desculpe', 'mas'])

    @staticmethod
    def get_sorry_response(**kwargs):
        model = IntentionResponseGAN.SORRY_GAN

        return model.predict_sentence(['sinto', 'muito'])

    @staticmethod
    def get_sports_and_playing_response(**kwargs):
        model = IntentionResponseGAN.SPORTS_AND_PLAYING_GAN

        return model.predict_sentence(['então', 'eu'])

    @staticmethod
    def get_suicide_response(**kwargs):
        model = IntentionResponseGAN.SUICIDE_GAN

        return model.predict_sentence(['ah', 'mas'])

    @staticmethod
    def get_threat_response(**kwargs):
        model = IntentionResponseGAN.TRHEAT_GAN

        return model.predict_sentence(['desculpe', 'mas'])

    @staticmethod
    def get_verbal_offense_response(**kwargs):
        model = IntentionResponseGAN.VERBAL_OFFENSE_GAN

        return model.predict_sentence(['vish', 'mas'])

    @staticmethod
    def get_what_am_i_response(**kwargs):
        model = IntentionResponseGAN.WHAT_AM_I_GAN

        return model.predict_sentence(['eu', 'sou'])

    @staticmethod
    def get_goodbye_response(**kwargs):
        model = IntentionResponseGAN.GOODBYE_GAN

        return model.predict_sentence(['até', 'logo'])
