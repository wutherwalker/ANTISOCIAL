from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        # print("Round:" + str(self.round_number))

        fake_round = self.round_number <= self.player.session.config['fake_rounds'] and not self.participant.vars['fake_rounds_done']
        real_round = self.round_number == 1 and self.participant.vars['fake_rounds_done']
        max_price = self.player.session.config['max_price']
        if fake_round or real_round:
            if self.round_number == 1:
                yield (pages.Instructions1)
                yield (pages.Instructions2)

            group_prime = self.participant.vars['fake_rounds_done'] and \
                          self.session.config['assign_groups']

            if group_prime:
                yield (pages.GroupMug)

            if random.random() < 0.5:
                yield (pages.Bid, {'object_choice': 'Mug A', 'bid': random.randint(0, max_price)})
            else:
                yield (pages.Bid, {'object_choice': 'Mug B', 'bid': random.randint(0, max_price)})
            yield (pages.Auction)