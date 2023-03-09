from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1 and self.participant.vars['artist'] != "send_home":
            yield (pages.Instructions1)
            yield (pages.Instructions2)

        yield (pages.Role)

        if self.player.sender:
            choice = random.randint(0, self.player.endowment)
            print("Choosing allocation: " + str(choice))
            yield (pages.Decision, {'allocation': choice})

        if self.participant.vars['artist'] != "send_home":
            yield (pages.Results)

        # if self.round_number == Constants.num_rounds and self.participant.vars['artist'] != "send_home":
        #     yield (pages.FinalResult)