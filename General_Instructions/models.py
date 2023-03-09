from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Patrick Julius'

doc = """
This app is designed to show instructions and IRB information for general
'typical' economics lab experiments. It should be appended as the first app
in a sequence. 
"""


class Constants(BaseConstants):
    name_in_url = 'General_Instructions'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
