from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield (pages.Instructions1)
            yield (pages.Instructions2)
            yield (pages.Instructions3)

        amount_sent = random.randint(0, self.player.endowment)
        if self.player.sender:
            yield (pages.DecisionSender, {'amount_sent': amount_sent})
        else:
            if self.player.endowment > 0:
                yield (pages.DecisionReceiver, {'amount_sent': amount_sent})
            else:
                yield (pages.DecisionReceiver)
        yield (pages.Results)