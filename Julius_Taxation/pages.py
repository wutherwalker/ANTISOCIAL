from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import math
import random


class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'show_up_fee': c(self.session.config['participation_fee']).to_real_world_currency(self.session),
            'conversion_rate': c(1).to_real_world_currency(self.session),
        }


class WelcomeA(WaitPage):
    template_name = 'Julius_Taxation/WelcomeA.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'show_up_fee': c(self.session.config['participation_fee']).to_real_world_currency(self.session),
            'conversion_rate': c(1).to_real_world_currency(self.session),
        }

    def after_all_players_arrive(self):
        pass


class Task(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'donation_multiplier': Constants.MPCR_nonprofit * Constants.players_per_group,
        }


class TaskA(WaitPage):
    template_name = 'Julius_Taxation/TaskA.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'donation_multiplier': Constants.MPCR_nonprofit * Constants.players_per_group,
        }

    def after_all_players_arrive(self):
        pass


class Taxes(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        tax_matrix = []
        for i in range(0, int(Constants.tax_maximum/5 + 1)):
            tax_matrix.append([])
            tax_matrix[i].append(5*i)
            tax_matrix[i].append((5*i)/Constants.tax_maximum*100)
            tax_matrix[i].append(round((5*i)**2/Constants.tax_maximum, 2))
            tax_matrix[i].append(round(5*i - (5*i)**2/Constants.tax_maximum, 2))

        return {
            'examples': list(range(0, int(Constants.tax_maximum/5 + 1))),
            'tax_matrix': tax_matrix,
        }


class TaxesA(WaitPage):
    template_name = 'Julius_Taxation/TaxesA.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        tax_matrix = []
        for i in range(0, int(Constants.tax_maximum / 5 + 1)):
            tax_matrix.append([])
            tax_matrix[i].append(5 * i)
            tax_matrix[i].append((5 * i) / Constants.tax_maximum * 100)
            tax_matrix[i].append(round((5 * i) ** 2 / Constants.tax_maximum, 2))
            tax_matrix[i].append(round(5 * i - (5 * i) ** 2 / Constants.tax_maximum, 2))

        return {
            'examples': list(range(0, int(Constants.tax_maximum / 5 + 1))),
            'tax_matrix': tax_matrix,
        }

    def after_all_players_arrive(self):
        pass


class Payoffs(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'donation_multiplier': Constants.MPCR_nonprofit * Constants.players_per_group,
            'government_multiplier': Constants.MPCR_government * Constants.players_per_group,
        }


class PayoffsA(WaitPage):
    template_name = 'Julius_Taxation/PayoffsA.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'donation_multiplier': Constants.MPCR_nonprofit * Constants.players_per_group,
            'government_multiplier': Constants.MPCR_government * Constants.players_per_group,
        }

    def after_all_players_arrive(self):
        pass


class Summary(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds / 2 + 1 or self.round_number == 1

    def vars_for_template(self):
        return {
            'player': self.player,
        }


class SummaryA(WaitPage):
    template_name = 'Julius_Taxation/SummaryA.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == Constants.num_rounds / 2 + 1 or self.round_number == 1

    def vars_for_template(self):
        return {
            'player': self.player,
        }

    def after_all_players_arrive(self):
        pass


class PracticeA(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def vars_for_template(self):
        return {
            'player': self.player,
            'N': Constants.players_per_group,
            'endowment': Constants.endowment_equal,
        }

    def is_displayed(self):
        return (self.round_number == Constants.num_rounds / 2 + 1 or self.round_number == 1) and not self.player.revenue_return

    def contribution_error_message(self, value):
        print('You entered', value)
        if value < 0:
            return 'You cannot contribute a negative amount.'
        if value > self.player.gross_income:
            return 'You cannot contribute more than your gross income.'


class PracticeB(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def vars_for_template(self):
        return {
            'player': self.player,
            'N': Constants.players_per_group,
            'endowment': Constants.endowment_equal,
            'revenue_multiplier': Constants.MPCR_government * Constants.players_per_group,

        }

    def is_displayed(self):
        return (self.round_number == Constants.num_rounds / 2 + 1 or self.round_number == 1) and self.player.revenue_return

    def contribution_error_message(self, value):
        print('You entered', value)
        if value < 0:
            return 'You cannot contribute a negative amount.'
        if value > self.player.gross_income:
            return 'You cannot contribute more than your gross income.'


class DecisionA(Page):
    form_model = 'player'
    # form_fields = 'gross_income', 'contribution', 'taxable_income', 'tax_paid', 'contribution_share', 'revenue_share'
    form_fields = ['contribution']

    def is_displayed(self):
        return not self.player.revenue_return

    def vars_for_template(self):
        self.player.contribution_initial = random.randint(0, self.player.gross_income)
        return {
            'player': self.player,
            'partners': self.player.get_others_in_group(),
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'donation_multiplier': Constants.MPCR_nonprofit * Constants.players_per_group,
            'revenue_multiplier': Constants.MPCR_government * Constants.players_per_group,
            'gross_income': int(self.player.gross_income),
            'income_change': self.subsession.round_number == Constants.num_rounds / 4 + 1 or
                             self.subsession.round_number == Constants.num_rounds * 3 / 4 + 1 or
                             self.subsession.round_number == Constants.num_rounds / 2 + 1,
            # 'income_change': False,
            'condition_change': self.subsession.round_number == Constants.num_rounds / 2 + 1,
        }

    timeout_seconds = 75


class DecisionB(Page):
    form_model = 'player'
    # form_fields = 'gross_income', 'contribution', 'taxable_income', 'tax_paid', 'contribution_share', 'revenue_share'
    form_fields = ['contribution']

    def is_displayed(self):
        return self.player.revenue_return

    def vars_for_template(self):
        self.player.contribution_initial = random.randint(0, self.player.gross_income)
        return {
            'player': self.player,
            'partners': self.player.get_others_in_group(),
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'donation_multiplier': Constants.MPCR_nonprofit * Constants.players_per_group,
            'revenue_multiplier': Constants.MPCR_government * Constants.players_per_group,
            'gross_income': int(self.player.gross_income),
            'income_change': self.subsession.round_number == Constants.num_rounds / 4 + 1 or
                             self.subsession.round_number == Constants.num_rounds * 3 / 4 + 1 or
                             self.subsession.round_number == Constants.num_rounds / 2 + 1,
            # 'income_change': False,
            'condition_change': self.subsession.round_number == Constants.num_rounds / 2 + 1,
        }

    timeout_seconds = 75


class ConditionChange(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds / 2 + 1 or self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'player': self.player,
            'round_set': math.floor(Constants.num_rounds/2),
            'revenue_multiplier': Constants.MPCR_government * Constants.players_per_group,
        }


class ResultsWaitPage(WaitPage):
    template_name = 'Julius_Taxation/ResultsWaitPage.html'

    def vars_for_template(self):
        return {
            'player': self.player,
            'partners': self.player.get_others_in_group(),
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'donation_multiplier': Constants.MPCR_nonprofit * Constants.players_per_group,
            'revenue_multiplier': Constants.MPCR_government * Constants.players_per_group,
            'gross_income': int(self.player.gross_income),
        }

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    form_model = 'player'

    def vars_for_template(self):
        # Zero out payoffs each round, to recalculate later.
        # This avoids the terrifying payment screen showing $300+ payments to each.
        self.participant.payoff = 0

        return {
            'player': self.player,
            'player_in_previous_rounds': self.player.in_previous_rounds(),
        }

    timeout_seconds = 15


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'major', 'race', 'income', 'explanation']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class CharityIntro(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'player': self.player,
            'endowment': c(Constants.endowment_charity).to_real_world_currency(self.session),
        }


class CharityList(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class CharityGame(Page):
    form_model = 'player'
    form_fields = ['charity', 'donation']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'player': self.player,
            'endowment': c(Constants.endowment_charity).to_real_world_currency(self.session)
        }

    def before_next_page(self):
        # Slightly kludgy correction to adjust for the exchange rate
        if self.player.donation > 0:
            self.player.donation *= self.player.donation / c(self.player.donation).to_real_world_currency(self.session)

    def error_message(self, values):
        if values['charity'] is None and values['donation'] > 0:
            return 'If you donate a positive amount, you must select a charity to give to.'


class FinalOutcome(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        round_payoff = self.player.in_all_rounds()[self.session.vars['paying_round']-1].payoff
        variable_payment = c(round_payoff).to_real_world_currency(self.session)
        # This does not assign the correct payoff on the online display; I don't know why
        self.participant.payoff = round_payoff
        show_up_fee = self.session.config['participation_fee']
        total_earnings = variable_payment
        total_payment = total_earnings + show_up_fee
        print("Round:" + str(round_payoff))
        print("Variable:" + str(variable_payment))
        print("Earnings:" + str(total_earnings))
        print("Show-up Fee:" + str(show_up_fee))
        print("Total:" + str(total_payment))
        return {
            'paying_round': self.session.vars['paying_round'],
            'player': self.player,
            'player_in_all_rounds': self.player.in_all_rounds(),
            'round_payoff': round_payoff,
            'variable_payment': variable_payment,
            'show_up_fee': show_up_fee,
            'total_earnings': total_earnings,
            'alternative': self.participant.payoff_plus_participation_fee(),
            'total_payment': total_payment,
            'participant_ID': self.participant.code,
        }


page_sequence = [
    Welcome,
    WelcomeA,
    Task,
    TaskA,
    Payoffs,
    PayoffsA,
    Taxes,
    TaxesA,
    ConditionChange,
    Summary,
    SummaryA,
    PracticeA,
    PracticeB,
    DecisionA,
    DecisionB,
    ResultsWaitPage,
    Results,
    # CharityIntro,
    # CharityList,
    # CharityGame,
    Questionnaire,
    FinalOutcome,
]
