from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):
    def play_round(self):
        Klee_probability = 0.3

        if self.round_number == 1:
            # yield (pages.Instructions1)
            yield (pages.Instructions2)

        if self.round_number < Constants.num_rounds:
            p = random.random()
            if p < Klee_probability:
                yield (pages.Choice, {'choice': 'A'})
            else:
                yield (pages.Choice, {'choice': 'B'})
            # print(self.player.choice)
            # print("Klee: " + str(self.player.Klee_chosen))
            # print("Kandinsky " + str(self.player.Kandinsky_chosen))
            # print(self.round_number)
            assert(self.player.Klee_chosen + self.player.Kandinsky_chosen == self.round_number)

        yield (pages.WaitForNextPainting)

        if self.round_number == Constants.num_rounds:
            # print("Klee: " + str(self.player.Klee_chosen))
            # print("Kandinsky " + str(self.player.Kandinsky_chosen))
            # print(self.group.artist)
            yield (pages.GroupResult)