

class EmotionHourglass:
    """
    Returns the emotional corresponding status based on a value
    between -2 and 2.
    """
    @staticmethod
    def get_pleasantness(value):
        """
        Returns a pleasantness emotion based on inputed value.

        param : value : <int>
        returns: <str>
        """
        if value > 0:
            if 1 <= value < 2:
                return 'serenity'
            elif value >= 2:
                return 'joy'
            else:
                return 'neutral'

        elif value < 0:
            if -2 < value <= -1:
                return 'pensiveness' 
            elif value <= -2:
                return 'sadness'
            else:
                return 'neutral'

        return 'neutral'

    @staticmethod
    def get_attention(value):
        """
        Returns a attention emotion based on inputed value.

        param : value : <int>
        returns: <str>
        """
        if value > 0:
            if 1 <= value < 2:
                return 'interest'
            elif value >= 2:
                return 'anticipation'
            else:
                return 'neutral'

        elif value < 0:
            if -2 < value <= -1:
                return 'distraction' 
            elif value <= -2:
                return 'surprise'
            else:
                return 'neutral'

        return 'neutral'

    @staticmethod
    def get_sensitivity(value):
        """
        Returns a sensitivity emotion based on inputed value.

        param : value : <int>
        returns: <str>
        """
        if value > 0:
            if 1 <= value < 2:
                return 'annoyance'
            elif value >= 2:
                return 'anger'
            else:
                return 'neutral'

        elif value < 0:
            if -2 < value <= -1:
                return 'aprehension' 
            elif value <= -2:
                return 'fear'
            else:
                return 'neutral'

        return 'neutral'

    @staticmethod
    def get_aptitude(value):
        """
        Returns a aptitude emotion based on inputed value.

        param : value : <int>
        returns: <str>
        """
        if value > 0:
            if 1 <= value < 2:
                return 'acceptance'
            elif value >= 2:
                return 'trust'
            else:
                return 'neutral'

        elif value < 0:
            if -2 < value <= -1:
                return 'boredom' 
            elif value <= -2:
                return 'disgust'
            else:
                return 'neutral'

        return 'neutral'
