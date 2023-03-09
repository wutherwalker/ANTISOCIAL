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
    name_in_url = 'Allocation'
    players_per_group = 2
    num_rounds = 10


class Subsession(BaseSubsession):
    def creating_session(self):
        print(self.get_group_matrix())
        if self.round_number == 1:
            # Choose which round is real
            self.session.vars['dictator_paying_round'] = random.randint(1, Constants.num_rounds)

        for player in self.get_players():
            player.endowment = self.session.config['endowment']

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Assigned to any group; False if sent home
    assigned_group = models.BooleanField()

    # True if Klee, False if Kandinsky
    Klee = models.BooleanField()

    # True if sender, False if receiver
    sender = models.BooleanField()

    # True if other partner is Klee, False if Kandinsky
    partner_Klee = models.BooleanField()
    purchased = models.StringField()
    partner_purchased = models.StringField()

    # Amount allocated to other player
    allocation = models.CurrencyField(
        min=0,
        max=100,
        widget=widgets.Slider(),
        initial=0,
    )

    endowment = models.CurrencyField()

    def role(self):
        if self.sender:
            return "sender"
        else:
            return "receiver"
