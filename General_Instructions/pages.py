from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions1(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'assign_groups': self.session.config['assign_groups'],
            'token_value': c(1).to_real_world_currency(self.session),
            'show_up_fee': self.session.config['participation_fee'],
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    Instructions1,
]
