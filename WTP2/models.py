from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

author = 'Patrick Julius'

doc = """
A simple willingness-to-pay task that can be used to measure the effect of group identification.
"""


class Constants(BaseConstants):
    name_in_url = 'WTP2'
    players_per_group = None
    num_rounds = 10


class Subsession(BaseSubsession):
    price = models.CurrencyField()

    def creating_session(self):
        # 0 to 100 points in increments of 5 points
        # Specific to each Subsession, i.e. each round; constant across participants
        self.price = random.randint(0, self.session.config['max_price'])

        if self.round_number == 1:
            self.session.vars['WTP_paying_round'] = 1
            for player in self.get_players():
                if 'fake_rounds_done' not in player.participant.vars:
                    player.participant.vars['fake_rounds_done'] = False


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    object_choice = models.StringField(
        choices=['Mug A', 'Mug B'],
        widget=widgets.RadioSelectHorizontal,
    )

    bid = models.CurrencyField(
        min=0,
        max=50,
        widget=widgets.Slider(attrs={'step': 1})
    )

    price = models.CurrencyField()
