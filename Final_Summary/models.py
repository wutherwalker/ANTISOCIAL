from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Patrick Julius'

doc = """
A final summary for the consumer choice experiment, dealing with all the possible cases.
"""


class Constants(BaseConstants):
    name_in_url = 'Final_Summary'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
