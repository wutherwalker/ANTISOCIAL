from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Patrick Julius'

doc = """
A very simple app to fill a gap in our consumer choice experiment.
"""


class Constants(BaseConstants):
    name_in_url = 'Reveal_Purchase'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Only used in grouping logic; analogous to Dictator Game
    sender = models.BooleanField()
    assigned_group = models.BooleanField()

    # True if Klee, False if Kandinsky
    Klee = models.BooleanField()
