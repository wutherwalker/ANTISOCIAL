from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Patrick Julius'

doc = """
This app implements a dictator game with group identity.
It assumes that players were already assigned to groups using the Klee-Kandinsky paradigm.
"""


class Constants(BaseConstants):
    name_in_url = 'Cheap_Talk'
    players_per_group = 2
    num_rounds = 15


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            # Choose which round is real
            self.session.vars['paying_round'] = random.randint(1, Constants.num_rounds)


class Group(BaseGroup):
    # True if heads, False if tails
    coin_heads = models.BooleanField()


class Player(BasePlayer):
    # Assigned to any group; False if sent home
    assigned_group = models.BooleanField()

    # True if Klee, False if Kandinsky
    Klee = models.BooleanField()

    # True if sender, False if receiver
    sender = models.BooleanField()

    # True if partner in Klee group, False if partner in Kandinsky group
    partner_Klee = models.BooleanField()

    # Message to/from other player
    message = models.StringField(
        choices=["Heads", "Tails"],
        widget=widgets.RadioSelect(),
    )

    # Action taken in response
    action = models.StringField(
        choices=['H', 'T'],
        widget=widgets.RadioSelect(),
    )

    def role(self):
        if self.sender:
            return "sender"
        else:
            return "receiver"