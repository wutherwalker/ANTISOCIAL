from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
import random


class PlayerBot(Bot):

    def play_round(self):
        honesty = 0.3

        if self.round_number == 1 and self.participant.vars['artist'] != "send_home":
            yield (pages.Instructions1)
            yield (pages.Instructions2)
            yield (pages.Instructions3)
            yield (pages.Role)

        if self.player.sender:
            if random.random() < honesty:
                if self.group.coin_heads:
                    yield (pages.ChoiceSender, {'message': 'Heads'})
                else:
                    yield (pages.ChoiceSender, {'message': 'Tails'})
            else:
                yield (pages.ChoiceSender, {'message': 'Heads'})
        elif self.player.assigned_group:
            if self.player.message == "Tails":
                yield (pages.ChoiceReceiver, {'action': 'T'})
            else:
                if random.random() < honesty or random.random() < 0.5:
                    yield (pages.ChoiceReceiver, {'action': 'H'})
                else:
                    yield (pages.ChoiceReceiver, {'action': 'T'})

        if self.participant.vars['artist'] != "send_home":
            yield (pages.Results)

        # if self.round_number == Constants.num_rounds and self.participant.vars['artist'] != "send_home":
        #     yield (pages.FinalResult)