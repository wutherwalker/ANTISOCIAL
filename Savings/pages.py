from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random, time

class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass

class WaitForInstructions(Page):
    def is_displayed(self):
        return self.round_number == int(Constants.num_rounds/2) or self.round_number == Constants.num_rounds

class Practice(Page):
    form_model = 'player'
    form_fields = ['consumption0']

    def is_displayed(self):
        return self.round_number == 1 or self.round_number == int(Constants.num_rounds/2)+1

    def vars_for_template(self):
        max_borrow = self.session.config['income_min'] - 1
        return {
            'constrained': self.player.borrowing_constrained,
            'max_consumption': int(self.player.income1 + max_borrow),
            'max_borrow': c(max_borrow),
            'multiplier': self.session.config['utility_multiplier'],
            'income': self.player.income1,
            'round_number': self.round_number,
            'income_min': self.session.config['income_min'],
            'income_max': self.session.config['income_max'],
            'max_savings': int(self.player.income1 - 1),
        }

class Wait(WaitPage):
    def after_all_players_arrive(self):
        pass

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class Choice1(Page):
    form_model = 'player'
    form_fields = ['consumption1']

    def vars_for_template(self):
        max_borrow = self.session.config['income_min'] - 1
        return {
            'constrained': self.player.borrowing_constrained,
            'max_consumption': int(self.player.income1 + max_borrow),
            'max_borrow': c(max_borrow),
            'multiplier': self.session.config['utility_multiplier'],
            'income': self.player.income1,
            'round_number': self.round_number,
            'income_min': self.session.config['income_min'],
            'income_max': self.session.config['income_max'],
            'max_savings': int(self.player.income1 - 1),
        }

    def before_next_page(self):
        player = self.player
        player.savings1 = player.income1 - player.consumption1
        player.payoff += player.get_payoff(player.consumption1)


class TreatmentChange(Page):
    pass


class Choice2(Page):
    form_model = 'player'
    form_fields = ['consumption2']

    def vars_for_template(self):
        max_borrow = 0 if self.player.borrowing_constrained else self.session.config['income_min'] - 1
        income = self.player.income2
        savings = self.player.savings1
        return {
            'max_consumption': int(income + savings + max_borrow),
            'constrained': self.player.borrowing_constrained,
            'max_borrow': c(max_borrow),
            'net_income': int(income + savings) if savings < 0 else int(income),
            'multiplier': self.session.config['utility_multiplier'],
            'income': income,
            'net_of_debt': ' (net of debt repayment)' if savings < 0 else '',
            'savings': savings,
            'debt': -1*savings,
            'round_number': self.round_number,
            'income_min': self.session.config['income_min'],
            'income_max': self.session.config['income_max'],
            'max_savings': int(income + savings - 1),
        }

    def before_next_page(self):
        player = self.player
        player.savings2 = player.income2 + player.savings1 - player.consumption2
        player.payoff += player.get_payoff(player.consumption2)

class FinishSection(WaitPage):
    def after_all_players_arrive(self):
        pass

    def is_displayed(self):
        return self.round_number == int(Constants.num_rounds/2) or self.round_number == Constants.num_rounds

class Results(Page):
    def vars_for_template(self):
        player = self.player
        player.consumption3 = player.income3 + player.savings2
        period_payoff = player.get_payoff(player.consumption3)
        player.payoff += period_payoff
        player.real_payoff_dollars = int(c(player.payoff).to_real_world_currency(self.session))
        player.real_payoff_cents = int(100*(c(player.payoff).to_real_world_currency(self.session) -
                                            player.real_payoff_dollars))
        income = player.income3
        savings = player.savings2

        return {
            'multiplier': self.session.config['utility_multiplier'],
            'income': income,
            'net_of_debt': ' (net of debt repayment)' if savings < 0 else '',
            'net_income': int(income + savings) if savings < 0 else int(income),
            'savings': savings,
            'debt': -1 * savings,
            'consumption': player.consumption3,
            'round_number': self.round_number,
            'period_payoff': c(period_payoff).to_real_world_currency(self.session),
            'total_payoff': c(player.payoff).to_real_world_currency(self.session),
            'income_min': self.session.config['income_min'],
            'income_max': self.session.config['income_max'],
        }


class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['CRT_answer_1', 'CRT_answer_2', 'CRT_answer_3', 'CRT_answer_4']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class RiskAttitude(Page):
    form_model = 'player'
    form_fields = ['risk_answer_01', 'risk_answer_02', 'risk_answer_03', 'risk_answer_04',
                   'risk_answer_05', 'risk_answer_06', 'risk_answer_07', 'risk_answer_08',
                   'risk_answer_09', 'risk_answer_10']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def before_next_page(self):
        player = self.player
        paying_gamble = self.session.vars['paying_gamble']

        if paying_gamble == 1:
            took_risk = player.risk_answer_01 == 2
        elif paying_gamble == 2:
            took_risk = player.risk_answer_02 == 2
        elif paying_gamble == 3:
            took_risk = player.risk_answer_03 == 2
        elif paying_gamble == 4:
            took_risk = player.risk_answer_04 == 2
        elif paying_gamble == 5:
            took_risk = player.risk_answer_05 == 2
        elif paying_gamble == 6:
            took_risk = player.risk_answer_06 == 2
        elif paying_gamble == 7:
            took_risk = player.risk_answer_07 == 2
        elif paying_gamble == 8:
            took_risk = player.risk_answer_08 == 2
        elif paying_gamble == 9:
            took_risk = player.risk_answer_09 == 2
        else:
            took_risk = player.risk_answer_10 == 2

        p = random.random()
        if p < 0.5:
            if took_risk:
                player.risk_payoff = Constants.risky_choice_constant
            else:
                player.risk_payoff = Constants.safe_choice_constant
        else:
            if took_risk:
                player.risk_payoff = Constants.risky_choice_list[paying_gamble-1]
            else:
                player.risk_payoff = Constants.safe_choice_list[paying_gamble-1]

        # Gamble results go here
        player.risk_payoff = 5


class TowerOfHanoi(Page):
    form_model = 'player'
    form_fields = ['Hanoi_moves']

    def get_timeout_seconds(self):
        return self.session.config['Hanoi_time'] * 60

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        self.participant.vars['start_time'] = time.time()

        return {
            'available_time': self.session.config['Hanoi_time'],
            'Hanoi_intercept': c(self.session.config['Hanoi_intercept']).to_real_world_currency(self.session),
            'Hanoi_penalty': c(self.session.config['Hanoi_penalty']).to_real_world_currency(self.session),
        }

    def before_next_page(self):
        self.player.Hanoi_time = time.time() - self.participant.vars['start_time']

        if self.timeout_happened:
            self.player.Hanoi_success = False
            self.player.Hanoi_payoff = 0
        else:
            self.player.Hanoi_success = True
            self.player.Hanoi_payoff = max(0, self.session.config['Hanoi_intercept'] -
                                   self.player.Hanoi_moves * self.session.config['Hanoi_penalty'])


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'major', 'GPA']

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class FinalResults(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        paying_round_1 = self.session.vars['paying_round_1']
        paying_round_1_payoff = self.player.in_round(paying_round_1).payoff
        paying_round_2 = self.session.vars['paying_round_2']
        paying_round_2_payoff = self.player.in_round(paying_round_2).payoff
        Hanoi_paid = self.session.vars['Hanoi_paid']
        if Hanoi_paid:
            bonus_payoff = self.player.Hanoi_payoff
        else:
            bonus_payoff = self.player.risk_payoff
        self.participant.payoff = paying_round_1_payoff + paying_round_2_payoff + bonus_payoff
        return {
            'player_in_all_rounds': self.player.in_all_rounds(),
            'paying_round_1': paying_round_1,
            'paying_round_2': paying_round_2,
            'paying_round_1_payoff': c(paying_round_1_payoff).to_real_world_currency(self.session),
            'paying_round_2_payoff': c(paying_round_2_payoff).to_real_world_currency(self.session),
            'gamble': self.session.vars['paying_gamble'],
            'Hanoi_paid': Hanoi_paid,
            'bonus_payoff': c(bonus_payoff).to_real_world_currency(self.session),
            'participation_fee': self.session.config['participation_fee'],
            'total_earnings': c(self.participant.payoff).to_real_world_currency(self.session),
            'final_payoff': self.participant.payoff_plus_participation_fee(),
        }


page_sequence = [
    Practice,
    Choice1,
    Choice2,
    Results,
    FinishSection,
    WaitForInstructions,
    RiskAttitude,
    Wait,
    TowerOfHanoi,
    Wait,
    CognitiveReflectionTest,
    Questionnaire,
    FinalResults,
]
