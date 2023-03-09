from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1



class VideoEvaluation(Page):
    form_model = 'player'
    form_fields = ['video_1_evaluation']



    def is_displayed(self):
        return self.subsession.round_number == 1



class VideoEvaluation2(Page):
    form_model = 'player'
    form_fields = ['video_2_evaluation']

    def is_displayed(self):
        return self.subsession.round_number == 1

class VideoEvaluation3(Page):
    form_model = 'player'
    form_fields = ['video_3_evaluation']

    def is_displayed(self):
        return self.subsession.round_number == 1

class VideoEvaluation4(Page):
    form_model = 'player'
    form_fields = ['video_4_evaluation']

    def is_displayed(self):
        return self.subsession.round_number == 1

class VideoEvaluation5(Page):
    form_model = 'player'
    form_fields = ['video_5_evaluation']

    def is_displayed(self):
        return self.subsession.round_number == 1

class Results(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'payoff': Constants.payoff}

page_sequence = [
    Introduction,
    VideoEvaluation,
    VideoEvaluation2,
    VideoEvaluation3,
    VideoEvaluation4,
    VideoEvaluation5,
    Results,
]
