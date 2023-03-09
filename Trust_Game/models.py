from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Patrick Julius'

doc = """
This app implements a trust game with groups that have been assigned by the Klee-Kandinsky paradigm.
"""


class Constants(BaseConstants):
    name_in_url = 'Trust_Game'
    players_per_group = 2
    num_rounds = 10


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['trust_paying_round'] = random.randint(1, Constants.num_rounds)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    sender = models.BooleanField()
    endowment = models.CurrencyField(
        min=0
    )
    amount_sent = models.CurrencyField(
        widget=widgets.Slider(),
        initial=0,
        # I'd prefer to only make it optional if you get no endowment,
        # but that turns out to be very complicated.
        # It will default to zero if you just click "Next", which is the DSE.
        blank=True,
    )

    # Assigned to any group; False if sent home
    assigned_group = models.BooleanField()

    # True if Klee, False if Kandinsky
    Klee = models.BooleanField()

    # True if other partner is Klee, False if Kandinsky
    partner_Klee = models.BooleanField()

    purchased = models.StringField()
    partner_purchased = models.StringField()

    def role(self):
        if self.sender:
            return "sender"
        else:
            return "receiver"

    def get_partner(self):
        return self.get_others_in_group()[0]
