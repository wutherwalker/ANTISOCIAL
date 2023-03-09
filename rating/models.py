from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    num_videos = 5
    payoff = 200
    players_per_group = None
    name_in_url = 'rating'
    num_rounds = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    video_1_evaluation = models.StringField(
        label='''
                    Here are your choices:
                    ''',
        widget=widgets.RadioSelectHorizontal,
        choices=['Good', 'Not bad', 'Bad', 'Too bad'],

    )
    video_2_evaluation = models.StringField(
        label='''
                    Here are your choices:
                    ''',
        widget=widgets.RadioSelectHorizontal,
        choices=['Good', 'Not bad', 'Bad', 'Too bad'],

    )
    video_3_evaluation = models.StringField(
        label='''
                    Here are your choices:
                    ''',
        widget=widgets.RadioSelectHorizontal,
        choices=['Good', 'Not bad', 'Bad', 'Too bad'],

    )
    video_4_evaluation = models.StringField(
        label='''
                    Here are your choices:
                    ''',
        widget=widgets.RadioSelectHorizontal,
        choices=['Good', 'Not bad', 'Bad', 'Too bad'],

    )
    video_5_evaluation= models.StringField(
        label='''
                    Here are your choices:
                    ''',
        widget=widgets.RadioSelectHorizontal,
        choices=['Good', 'Not bad', 'Bad', 'Too bad'],

    )

