from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Patrick Julius'

doc = """
This app rapidly generates randomized groups as if they had gone through a Klee-Kandinsky paradigm.
"""


class Constants(BaseConstants):
    name_in_url = 'quickstart'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        group_matrix = []
        players = self.get_players()
        players_per_group = self.session.config['players_per_group']
        for i in range(0, len(players), players_per_group):
            group_matrix.append(players[i:i + players_per_group])
        self.set_group_matrix(group_matrix)
        self.group_randomly()
        print(self.get_group_matrix())
        for player in self.get_group_matrix()[0]:
            player.participant.vars['artist'] = "Klee"
        for player in self.get_group_matrix()[1]:
            player.participant.vars['artist'] = "Kandinsky"

        if self.round_number == 1:
            for player in self.get_players():
                player.participant.vars['part'] = 1


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
