from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.player.assigned_group:
            yield (pages.ChatPage)
            yield (pages.Answers, {'painting_1': 'Klee', 'painting_2': 'Kandinsky'})
            yield (pages.Results)