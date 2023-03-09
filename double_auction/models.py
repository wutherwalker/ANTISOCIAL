
import random
import time
import logging

# This is all standard oTree stuff
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


# To change the payoff function, I would need to propagate the change across
# models.py, pages.py, double_auction.html, and app.js.

author = 'Jan Dietrich and Patrick Julius'

doc = """
Based on the double auction template created by Jan Dietrich,
I created a two-dimensional version where participants bargain
simultaneously over both quantity and price.

The payoff functions use CRRA utility with configurable parameters.
Value and cost are displayed on a graph.

Proposals are shared only with members of the same group.
"""


##
# KNOWN ISSUES
# 1. Refreshing the page removes all but the most recent proposal
# 2. Accepting a proposal different from the most recent proposal
# actually creates a new offer the other player must accept
##

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Standard Constants section as in any oTree project
class Constants(BaseConstants):
    name_in_url = 'double_auction'
    players_per_group = 2
    num_rounds = 50

    quiz_radio_button = dict(
        choices=[[1, 'Yes'],
                 [2, 'No']],
        widget=widgets.RadioSelectHorizontal
    )

# Nothing is handled at the Group or Subsession level
class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number % 5 == 0:
            print("Loading ... " + str(self.round_number*2) + "%")
        if self.round_number == 1:
            self.session.vars['paying_rounds'] = random.sample(range(1, self.session.config["num_rounds"]+1), 2)
            print("Grouping for the first time")
            self.group_randomly()
            print(self.get_group_matrix())
        else:
            if self.session.config['random_grouping']:
                print("Before:" + str(self.get_group_matrix()))
                self.group_randomly(fixed_id_in_group=True)
                print("Should be grouping randomly")
                print("After:" + str(self.get_group_matrix()))
            else:
                self.group_like_round(self.round_number - 1)


class Group(BaseGroup):
    pass

# Player methods, with obvious auction applications
class Player(BasePlayer):
    money = models.FloatField()
    cost = models.FloatField()
    benefit = models.FloatField()
    # Using FloatField because "object of type Currency is not json serializable" error
    value = models.FloatField(blank=False)
    quantity = models.FloatField(blank=False)
    match_with = models.OneToOneField('Player', null=True, on_delete=models.CASCADE)
    # I will need to change these to assign roles
    instructions_da1 = models.IntegerField(
        verbose_name="You are a buyer. Your valuation for the good is 50 points. You submit a bid of 40 points and a seller accepts this bid. What are your earnings (in points)?",
    )

    instructions_da3 = models.IntegerField(
        verbose_name="You are a seller. Your production costs for the good are 20 points. You submit an ask of 25 points and a buyer accepts this ask. What are your earnings (in points)?",
    )
    instructions_da4 = models.IntegerField(
        verbose_name="You are a buyer. Your valuation for the good is 40 points. Is it possible to submit a bid of 60 points?",
        **Constants.quiz_radio_button
    )

    transaction_log = models.LongStringField(initial="Proposals: ")

    display_id = models.IntegerField()
    # is_bot = models.BooleanField()

    auction_start_time = models.DateTimeField(auto_now=True)
    auction_duration = models.FloatField()

    # These functions can be changed if we vary the cost or utility functional form
    def compute_value(self, quantity):
        if quantity is not None:
            return round(self.session.config['value_multiplier'] * quantity ** self.session.config['value_exponent'], 2)
        else:
            return 0

    def compute_cost(self, quantity):
        if quantity is not None:
            return round(self.session.config['cost_multiplier'] * quantity ** self.session.config['cost_exponent'], 2)
        else:
            return 0

# A new class not defined by default in oTree, used to handle trades
class Transaction(models.Model):
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    value = models.FloatField(blank=False)
    quantity = models.FloatField(blank=False)
    time = models.DateTimeField(auto_now=True)
    buyer_payoff = models.FloatField(blank=True)
    seller_payoff = models.FloatField(blank=True)
    # bot = models.BooleanField()
