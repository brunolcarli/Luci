from core.model_loader import IntentionResponseGAN
from core.training.text_gen import sample


class ResponseGenerator:
    """
    Contain methods for generating response for specific intentions.
    """
    @staticmethod
    def get_who_am_i_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.WHO_AM_I_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_acknowledge_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.ACKNOWLEDGEMENT_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_forbidden_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.FORBIDDEN_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_funny_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.FUNNY_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_greeting_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.GREETING_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_helpful_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.HELPFUL_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_illegal_stuff_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.ILLEGAL_STUFF_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_music_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.MUSIC_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_my_age_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.MY_AGE_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)


    def get_my_gender_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.MY_GENDER_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_praise_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.PRAISE

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_racism_xenophobia_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.RACISM_XENOPHOBIA_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_sexual_abuse_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.SEXUAL_ABUSE_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_sorry_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.SORRY_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_sports_and_playing_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.SPORTS_AND_PLAYING_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_suicide_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.SUICIDE_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_threat_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.TRHEAT_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_verbal_offense_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.VERBAL_OFFENSE_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_what_am_i_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.WHAT_AM_I_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)

    @staticmethod
    def get_goodbye_response():
        model, idx_to_chars, chars_to_idx = IntentionResponseGAN.WHAT_AM_I_GAN

        return sample(model, chars_to_idx, idx_to_chars, 1000)
