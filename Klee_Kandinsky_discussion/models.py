from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Patrick Julius'

doc = """
This is a follow-up to the Klee-Kandinsky group paradigm, which primes group identity
by allowing members of a group to chat with one another and decide which artist made
each of a set of paintings. 
"""


class Constants(BaseConstants):
    name_in_url = 'Klee_Kandinsky_discussion'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # True if assigned to a group, False if not
    assigned_group = models.BooleanField()
    # True if Klee, False if Kandinsky
    Klee = models.BooleanField()

    painting_1 = models.StringField(
        label="",
        choices=['Klee', 'Kandinsky'],
        blank=False,
        widget=widgets.RadioSelectHorizontal,
    )

    painting_2= models.StringField(
        label="",
        choices=['Klee', 'Kandinsky'],
        blank=False,
        widget=widgets.RadioSelectHorizontal,
    )

    score = models.IntegerField(
        initial=0,
    )