from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    cases = ['smart', 'dumb', 'obedient', 'random']

    def play_round(self):
        if self.round_number == 1:
            yield (pages.Intro)
            yield (pages.Matching)
            yield (pages.Payoffs)
            if self.session.config['announce_treatment']:
                yield (pages.Announcements)
            yield (pages.Summary)
            yield (pages.Administration)

        if self.case == 'smart':
            if self.player.player_class == 1 or self.player.player_class == 2:
                yield (pages.Decision, {'decision': 'X'})
            else:
                yield (pages.Decision, {'decision': 'Y'})
        elif self.case == 'dumb':
            if self.player.player_class == 1 or self.player.player_class == 2:
                yield (pages.Decision, {'decision': 'Y'})
            else:
                yield (pages.Decision, {'decision': 'X'})
        elif self.case == 'obedient':
            if self.session.config['announce_treatment']:
                yield(pages.Decision, {'decision': self.subsession.announcement})
            else:
                yield(pages.Decision, {'decision': 'X'})
        elif self.case == 'random':
            if random.random() < 0.5:
                yield(pages.Decision, {'decision': 'X'})
            else:
                yield(pages.Decision, {'decision': 'Y'})
        yield(pages.Results)
