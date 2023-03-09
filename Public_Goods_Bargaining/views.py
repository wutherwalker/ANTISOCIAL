import random, math, itertools
from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class StartWait(WaitPage):

    wait_for_all_groups = True

    title_text = "Please Wait"
    body_text = "Please wait for the experiment to continue."


class Offer(Page):

    form_model = models.Group
    form_fields = ['High_Account_offered', 'Low_Account_offered', 'Group_Account_offered']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        self.group.set_new_floor()

        if self.player.HighLow == 1:
            return {
                    'role': "High",
                    'mandatory_treatment': self.session.config['mandatory_treatment'],
                    }
        else:
            return {
                    'role': "Low",
                    'mandatory_treatment': self.session.config['mandatory_treatment'],
                    }

    def error_message(self,values):
        if values["High_Account_offered"] + values["Low_Account_offered"] + values["Group_Account_offered"] != 100:
            return 'The sum of the three accounts must equal 100 points.'
        if values["Group_Account_offered"] < 1:
            return 'You must put at least 1 point into the group account.'

    #timeout_seconds = 5


class WaitForProposer(WaitPage):
    # template_name = 'Public_Goods_Bargaining/WaitForProposer.html'
    pass


class Accept(Page):

    form_model = models.Group
    form_fields = ['offer_accepted']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        if self.player.HighLow == 1:
            return{
                    'role': "High",
                    'mandatory_treatment': self.session.config['mandatory_treatment'],
                    }
        else:
            return {
                    'role': "Low",
                    'mandatory_treatment': self.session.config['mandatory_treatment'],
                    }

    #timeout_seconds = 5


class ResultsWaitPage(WaitPage):
    # template_name = 'Public_Goods_Bargaining/ResultsWaitPage.html'

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    #timeout_seconds = 5

    def before_next_page(self):
        self.player.set_roles()
        self.player.SetSequence()
        self.player.set_supergame_payoffs()

    def vars_for_template(self):
        if not (self.subsession.round_number == Constants.a or self.subsession.round_number == Constants.a + Constants.b or self.subsession.round_number == Constants.a + Constants.b + Constants.d or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.j):
            return {
                    'numberroll': self.subsession.randomchoice,
                    'mandatory_treatment': self.session.config['mandatory_treatment'],
                    }
        else:
            return {'numberroll': 5,
                    'mandatory_treatment': self.session.config['mandatory_treatment'],
                    }


class SupergameResults(Page):
    #timeout_seconds = 5
    def is_displayed(self):
        return self.subsession.round_number == Constants.a or self.subsession.round_number == Constants.a + Constants.b or self.subsession.round_number == Constants.a + Constants.b + Constants.d or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.j

    def vars_for_template(self):
        if self.subsession.round_number <= Constants.a:
            return {'supergamepayoff': self.participant.vars['payoff' + str(1)]}
        elif self.subsession.round_number <= Constants.a + Constants.b:
            return {'supergamepayoff': self.participant.vars['payoff' + str(2)]}
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d:
            return {'supergamepayoff': self.participant.vars['payoff' + str(3)]}
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d + Constants.e:
            return {'supergamepayoff':self.participant.vars['payoff' + str(4)]}
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f:
            return {'supergamepayoff': self.participant.vars['payoff' + str(5)]}
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g:
            return {'supergamepayoff': self.participant.vars['payoff' + str(6)]}
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h:
            return {'supergamepayoff': self.participant.vars['payoff' + str(7)]}
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i:
            return {'supergamepayoff': self.participant.vars['payoff' + str(8)]}
        else:
            return {'supergamepayoff': self.participant.vars['payoff' + str(9)]}


class EveryoneWaits(WaitPage):
    wait_for_all_groups = True


class NewSequence(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.a + 1 or self.subsession.round_number == Constants.a + Constants.b + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i + Constants.j + 1
    timeout_seconds = 10


class FinalResults(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i + Constants.j

    def vars_for_template(self):
        # This often displays None as the payoff fails to be calculated properly; a possible reason is how the
        # supergames are drawn
        self.participant.payoff = self.player.bigpayoff
        return {
                'supergame1_payoff': self.participant.vars['supergame1_payoff'],
                'supergame2_payoff': self.participant.vars['supergame2_payoff'],
                'VariablePayment': self.player.bigpayoff,
                'supergame1': self.session.vars['supergame1'],
                'supergame2': self.session.vars['supergame2']}


page_sequence = [
    StartWait,
    NewSequence,
    Offer,
    WaitForProposer,
    Accept,
    ResultsWaitPage,
    EveryoneWaits,
    Results,
    SupergameResults,
    FinalResults

]
