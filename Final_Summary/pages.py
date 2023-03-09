from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.wait_for_all_groups = True


class FinalOutcome(Page):
    def vars_for_template(self):

        if self.session.config['assign_groups']:
            matching_money = c(self.participant.vars['matching_money'])
        else:
            matching_money = 0

        if self.session.config['WTP_task']:
            WTP_paying_round = self.session.vars['WTP_paying_round']
            WTP_payoff = self.participant.vars['WTP_payoff']
            item_purchased = self.participant.vars['item_purchased']
        else:
            WTP_paying_round = None
            WTP_payoff = 0
            item_purchased = None

        if self.session.config['dictator_game']:
            dictator_paying_round = self.session.vars['dictator_paying_round']
            dictator_payoff = self.participant.vars['dictator_payoff']
        else:
            dictator_paying_round = None
            dictator_payoff = 0

        if self.session.config['trust_game']:
            trust_paying_round = self.session.vars['trust_paying_round']
            trust_payoff = self.participant.vars['trust_payoff']
        else:
            trust_paying_round = None
            trust_payoff = 0

        if self.session.config['dictator_game'] or self.session.config['trust_game']:
            endowment = self.session.config['endowment']
        else:
            endowment = 0

        total_earnings = matching_money
        if self.session.config['WTP_task']:
            total_earnings += WTP_payoff
        if self.session.config['dictator_game']:
            total_earnings += dictator_payoff
        if self.session.config['trust_game']:
            total_earnings += trust_payoff

        self.participant.payoff = total_earnings

        return {
            'assign_groups': self.session.config['assign_groups'],
            'dictator_game': self.session.config['dictator_game'],
            'trust_game': self.session.config['trust_game'],
            'WTP_task': self.session.config['WTP_task'],
            'artist': self.participant.vars['artist'],
            'matching_money': c(matching_money),
            'matching_money_real': c(matching_money).to_real_world_currency(self.session),
            'participation_fee': self.session.config['participation_fee'],
            'endowment': c(endowment),
            'own_group': "Klee" if self.participant.vars['artist'] == "Klee" else "Kandinsky",
            'item_purchased': item_purchased is not None,
            'object_choice': item_purchased,
            'object_group': "Klee" if item_purchased == "Mug A" else "Kandinsky",
            'WTP_paying_round': WTP_paying_round,
            'WTP_payoff': WTP_payoff,
            'WTP_payoff_real': c(WTP_payoff).to_real_world_currency(self.session),
            'dictator_paying_round': dictator_paying_round,
            'dictator_payoff': dictator_payoff,
            'dictator_payoff_real': c(dictator_payoff).to_real_world_currency(self.session),
            'trust_paying_round': trust_paying_round,
            'trust_payoff': trust_payoff,
            'trust_payoff_real': c(trust_payoff).to_real_world_currency(self.session),
            'total_earnings': c(total_earnings).to_real_world_currency(self.session),
        }


page_sequence = [
    ResultsWaitPage,
    FinalOutcome,
]
