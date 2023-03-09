from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    cases = ['saver', 'spender', 'rational', 'hand-mouth', 'random']

    def play_round(self):
        mean = int((self.player.session.config['income_max'] + self.player.session.config['income_min'])/2)
        max_borrow = int(self.player.session.config['income_min']-1)

        if self.round_number == 1 or self.round_number == int(Constants.num_rounds/2)+1:
            yield (pages.Practice, {'consumption0': 50})

        if self.case == "saver":
            consumption1 = 1
        elif self.case == "spender":
            consumption1 = self.player.income1 + max_borrow
        elif self.case == 'rational':
            consumption1 = mean
        elif self.case == 'hand-mouth':
            consumption1 = self.player.income1
        else:
            consumption1 = random.randint(1, self.player.income1 + max_borrow)

        yield (pages.Choice1, {'consumption1': consumption1})

        if self.case == "saver":
            consumption2 = 1
        elif self.case == "spender":
            if self.player.borrowing_constrained:
                consumption2 = self.player.income2 + self.player.savings1
            else:
                consumption2 = self.player.income2 + self.player.savings1 + max_borrow
        elif self.case == "rational":
            if self.player.borrowing_constrained:
                consumption2 = min(mean, self.player.income2 + self.player.savings1)
            else:
                consumption2 = mean
        elif self.case == 'hand-mouth':
            consumption2 = self.player.income2
        else:
            if self.player.borrowing_constrained:
                consumption2 = random.randint(1, self.player.income2 + self.player.savings1)
            else:
                consumption2 = random.randint(1, self.player.income2 + self.player.savings1 + max_borrow)

        yield (pages.Choice2, {'consumption2': consumption2})

        yield (pages.Results)

        if self.round_number == int(Constants.num_rounds/2) or self.round_number == Constants.num_rounds:
            yield (pages.WaitForInstructions)

        if self.round_number == Constants.num_rounds:
            yield (pages.RiskAttitude, {'risk_answer_01': 1, 'risk_answer_02': 1,
                                        'risk_answer_03': 1, 'risk_answer_04': 1,
                                        'risk_answer_05': 1, 'risk_answer_06': 2,
                                        'risk_answer_07': 2, 'risk_answer_08': 2,
                                        'risk_answer_09': 2, 'risk_answer_10': 2})
            yield (pages.TowerOfHanoi, {'Hanoi_moves': random.randint(7, 30)})
            yield (pages.CognitiveReflectionTest, {'CRT_answer_1': 4, 'CRT_answer_2': 29,
                                                   'CRT_answer_3': 20,
                                                   'CRT_answer_4': 'lost money in the stock market'})
            yield (pages.Questionnaire, {'age': 31, 'gender': 'Man', 'major': 'Economics', 'GPA': 4.0})

        print(self.case.capitalize() + ", with a payoff of " + str(self.player.payoff))
