from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Patrick Julius'

doc = """
This app implements the standard 'Klee-Kandinsky' group paradigm.
Participants are shown a number of paintings and asked to choose which they prefer,
and then grouped based on which artist they chose most often.

Group logic is set to ensure that groups satisfy two constraints:
(1) Everyone in an artist's group strictly preferred more of that artist
(2) Both groups are the same size

Participants that cannot be matched using these criteria are told to leave the experiment early.
"""


class Constants(BaseConstants):
    name_in_url = 'Klee_Kandinsky'
    # This is used to ensure that there are always an even number of participants
    players_per_group = 2
    # This should be the number of paintings plus one, as the last round assigns groups
    num_rounds = 6
    participation_fee = 7


class Subsession(BaseSubsession):
    def creating_session(self):
        for player in self.get_players():
            if not self.session.config['assign_groups']:
                player.participant.vars['artist'] = None
            # Set a flag to randomly determine the order of the artists at the beginning of each round
            player.Klee_first = random.random() < 0.5
            print("Klee first? " + str(player.Klee_first))


class Group(BaseGroup):
    artist = models.StringField()

    def assign_to_group(self):
        klee_players = [p for p in self.get_players() if p.choice == 'A']
        kandinsky_players = [p for p in self.get_players() if p.choice == 'B']

        # Check that both groups are the same size
        if len(klee_players) != len(kandinsky_players):
            self.subsession.round_number = Constants.num_rounds
            return

        # Check preference for Klee
        for p in klee_players:
            if p.Klee_chosen >= p.Kandinsky_chosen:
                p.participant.vars['artist'] = 'Klee'
            else:
                self.subsession.round_number = Constants.num_rounds
                return

        # Check preference for Kandinsky
        for p in kandinsky_players:
            if p.Kandinsky_chosen >= p.Klee_chosen:
                p.participant.vars['artist'] = 'Kandinsky'
            else:
                self.subsession.round_number = Constants.num_rounds
                return

        # Assign groups based on preferred artist
        artist = random.choice(['Klee', 'Kandinsky'])
        self.artist = artist
        for p in self.get_players():
            if p.participant.vars['artist'] == artist:
                p.group = self.get_group_matrix()[0][0]
            else:
                p.group = self.get_group_matrix()[0][1]


class Player(BasePlayer):
    Klee_first = models.BooleanField()
    Klee_chosen = models.IntegerField(initial=0)
    Kandinsky_chosen = models.IntegerField(initial=0)
    choice = models.StringField(
        choices=['A', 'B'],
        widget=widgets.RadioSelectHorizontal,
    )