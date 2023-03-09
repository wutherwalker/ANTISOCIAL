from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

import random


class Introduction(Page):
    def is_displayed(self):
        self.session.vars['continue'] = True
        return self.round_number == 1


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    timeout_seconds = 20
    timeout_submission = {'decision': "A"}

    def is_displayed(self):
        return self.session.vars['continue']

    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
        }


class ResultsWaitPage(WaitPage):
    template_name = 'HW2_Julius_StagHunt/ResultsWaitPage.html'

    def after_all_players_arrive(self):
        self.group.set_payoffs()

        if self.round_number >= 6 and self.session.vars['continue'] is True:
            # Starting at round 6, the game can end randomly
            p = random.random()
            if p > Constants.prob_continue or self.round_number >= 10:
                self.session.vars['continue'] = False
                self.session.vars['paying_round'] = random.randint(1, self.round_number)
                for person in self.subsession.get_players():
                    print("@@@@@@@@@@@@@ DEBUG @@@@@@@@@@@")
                    print("Paying round:")
                    print(self.session.vars['paying_round'])
                    person.participant.payoff = person.in_all_rounds()[self.session.vars['paying_round']-1].payoff
                    print(person.participant.payoff)
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


class Results(Page):
    def is_displayed(self):
        return self.session.vars['continue']

    form_model = 'player'

    def vars_for_template(self):
        return {
            'player_in_previous_rounds': self.player.in_previous_rounds(),
        }


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'major', 'race', 'income']

    def is_displayed(self):
        return not self.session.vars['continue']


class FinalOutcome(Page):
    def is_displayed(self):
        return not self.session.vars['continue']

    form_model = 'player'

    def vars_for_template(self):
        print("***********DEBUG***********")
        print(self.player.in_all_rounds()[self.session.vars['paying_round']-1].payoff)
        print(self.player.in_all_rounds()[self.session.vars['paying_round']-1].round_number)
        print("***************************")
        return {
            'player_in_all_rounds': self.player.in_all_rounds(),
            'paying_round': self.player.in_all_rounds()[self.session.vars['paying_round']-1].round_number,
            'player_in_paying_round': self.player.in_all_rounds()[self.session.vars['paying_round']-1]
        }



page_sequence = [
    Introduction,
    Decision,
    ResultsWaitPage,
    Results,
    Questionnaire,
    FinalOutcome
]
