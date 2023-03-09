from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    cases = ['generous', 'selfish', 'random', 'reverse']

    def play_round(self):

        if self.round_number == 1:
            yield (pages.Welcome)
            yield (pages.Task)
            yield (pages.Payoffs)
            yield (pages.Taxes)
        if self.subsession.round_number == Constants.num_rounds / 2 + 1 or self.subsession.round_number == 1:
            yield (pages.ConditionChange)
            yield (pages.Summary)
        if (self.round_number == Constants.num_rounds / 2 + 1 or self.round_number == 1) and not self.player.revenue_return:
            yield (pages.PracticeA, {'contribution': random.randint(0, 15)})
        if (self.round_number == Constants.num_rounds / 2 + 1 or self.round_number == 1) and self.player.revenue_return:
            yield (pages.PracticeB, {'contribution': random.randint(0, 15)})
        if self.case == 'selfish':
            if self.player.revenue_return:
                if self.player.gross_income == 10:
                    yield (pages.DecisionB, {'contribution': 0})
                elif self.player.gross_income == 15:
                    yield (pages.DecisionB, {'contribution': 2})
                elif self.player.gross_income == 20:
                    yield (pages.DecisionB, {'contribution': 7})
            else:
                if self.player.gross_income == 10:
                    yield (pages.DecisionA, {'contribution': 2})
                elif self.player.gross_income == 15:
                    yield (pages.DecisionA, {'contribution': 7})
                elif self.player.gross_income == 20:
                    yield (pages.DecisionA, {'contribution': 12})
        elif self.case == 'generous':
            if self.player.revenue_return:
                yield (pages.DecisionB, {'contribution': 0})
            else:
                yield (pages.DecisionA, {'contribution': self.player.gross_income})
        elif self.case == 'random':
            if self.player.revenue_return:
                yield (pages.DecisionB, {'contribution': random.randint(0, self.player.gross_income)})
            else:
                yield (pages.DecisionA, {'contribution': random.randint(0, self.player.gross_income)})
        elif self.case == 'reverse':
            if self.player.revenue_return:
                yield (pages.DecisionB, {'contribution': self.player.gross_income})
            else:
                yield (pages.DecisionA, {'contribution': 0})
        yield (pages.Results)
        if self.round_number == Constants.num_rounds:
            # yield (pages.CharityIntro)
            # yield (pages.CharityList)
            # if self.case == 'generous':
            #     yield(pages.CharityGame, {'charity': 'UNICEF', 'donation': 5})
            # else:
            #     yield(pages.CharityGame, {'donation': 0})
            yield (pages.Questionnaire)
