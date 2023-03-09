from ._builtin import Bot
from . import pages


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Revelation)
