from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'John Duffy and Patrick Julius'

doc = """
This experiment implements a 4-player Battle of the Sexes game with 3 Nash equilibria.
Red players prefer X, while Blue players prefer Y; but all players prefer coordination over miscoordination.
The treatment is to introduce randomized announcements as a correlated equilibrium device.
"""


class Constants(BaseConstants):
    name_in_url = 'Duffy_2018'
    players_per_group = 4
    num_rounds = 40
    high_payoff = c(9)
    low_payoff = c(3)
    # Probability of announcing X; announce Y otherwise
    announce_X_prob = 0.5
    # Expected duration of experiment in minutes
    duration = 90


class Subsession(BaseSubsession):
    announcement = models.StringField()
    memory_number = models.IntegerField()

    def creating_session(self):

        if self.round_number == 1:
            # This ensures that changing the conversion rate does not change the show-up fee
            self.session.vars['participation_fee'] = \
                c(self.session.config['participation_fee']/c(1.00).to_real_world_currency(self.session))
            self.session.vars['paying_round_1'] = random.randint(1, Constants.num_rounds)
            # Ensures the same round isn't chosen twice
            self.session.vars['paying_round_2'] = self.session.vars['paying_round_1']
            while self.session.vars['paying_round_2'] == self.session.vars['paying_round_1']:
                self.session.vars['paying_round_2'] = random.randint(1, Constants.num_rounds)

            for player in self.get_players():
                player.player_class = player.id_in_group

            self.session.vars['num_groups'] = int(self.session.num_participants/Constants.players_per_group)

        if self.round_number > 1:
            # In original matrix, each row is a group
            old_matrix = self.get_group_matrix()
            # Transpose so that each row is a role
            new_matrix = [list(t) for t in list(zip(*old_matrix))]
            # Randomly swap entries within each row of transposed matrix so that players keep roles but change groups
            for swap in range(0, 10):
                for role in new_matrix:
                    x = random.randint(0, self.session.vars['num_groups']-1)
                    y = random.randint(0, self.session.vars['num_groups']-1)
                    role[x], role[y] = role[y], role[x]
            # Transpose back so that each row is a group
            new_matrix = [list(t) for t in list(zip(*new_matrix))]

            self.set_group_matrix(new_matrix)
            for player in self.get_players():
                player.player_class = player.id_in_group

        if self.session.config['announce_treatment']:
            p = random.random()
            if p < Constants.announce_X_prob:
                self.announcement = "X"
            else:
                self.announcement = "Y"

        # This generates the numbers to memorize
        digit_span = self.session.config['digit_span']
        if digit_span > 0:
            self.memory_number = random.randint(1, 9) * 10**(digit_span-1) + random.randint(0, 10**(digit_span-1))
        else:
            self.memory_number = 0


class Group(BaseGroup):
    count_X = models.IntegerField()
    count_Y = models.IntegerField()

    def set_payoffs(self):
        self.count_X = 0
        self.count_Y = 0
        for player in self.get_players():
            if player.decision == "X":
                self.count_X += 1
            else:
                self.count_Y += 1

        for player in self.get_players():
            if player.decision == "X":
                player.others_X = self.count_X - 1
                player.others_Y = self.count_Y

                if player.player_class == 1 or player.player_class == 2:
                    # Red players
                    player.payoff = player.others_X * Constants.high_payoff
                else:
                    # Blue players
                    player.payoff = player.others_X * Constants.low_payoff
            else:
                player.others_X = self.count_X
                player.others_Y = self.count_Y - 1

                if player.player_class == 1 or player.player_class == 2:
                    player.payoff = player.others_Y * Constants.low_payoff
                else:
                    player.payoff = player.others_Y * Constants.high_payoff


class Player(BasePlayer):
    # 1 and 2 are Red, 3 and 4 are Blue
    player_class = models.IntegerField()

    def role(self):
        return self.player_class

    # Choices
    decision = models.StringField(choices=["X", "Y"])

    # Outcomes
    others_X = models.IntegerField()
    others_Y = models.IntegerField()

    # Number to memorize
    memory_number = models.IntegerField(min=0)

    ## Quiz ##

    # Correct answer: True
    q1 = models.StringField(choices=["True", "False"])

    # Correct answer: False
    q2 = models.StringField(choices=["True", "False"])

    # Correct answer: False
    q3 = models.StringField(choices=["True", "False"])

    # Correct answer: 50
    q4a = models.IntegerField(min=0, max=100)
    q4b = models.IntegerField(min=0, max=100)

    # Correct answer: False
    q5 = models.StringField(choices=["True", "False"])

    # Correct answer: 18
    q6 = models.IntegerField()

    # Correct answer: 18
    q7 = models.IntegerField()

    # Correct answer: 0
    q8 = models.IntegerField()

    # Correct answer: 3
    q9 = models.IntegerField()

    # Correct answer: True
    q10 = models.StringField(choices=["True", "False"])

    # Errors recorded
    errors = models.IntegerField(initial=0)

