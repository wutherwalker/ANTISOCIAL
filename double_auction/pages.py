# This is all standard Python stuff
import random
import time
import datetime
from math import floor, ceil
import logging

# This is all standard oTree stuff
from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

# This seems to be for processing iterables in some fashion
# I think it's a base Python class
from itertools import zip_longest

# I'm not sure where they are using this import; is this where they get message functionality?
import otree.common_internal

# This is just for their automated bidding system
from .tasks import automated_bid

# Get an instance of a logger
logger = logging.getLogger(__name__)


# The first page just shows instructions; I have commented out most of the special functionality
class Instructions(Page):
    timeout_seconds = 300
    # form_model = 'player'
    # form_fields = ["instructions_da1",  "instructions_da3", "instructions_da4"]
    def is_displayed(self):
        return self.subsession.round_number == 1

    # # Error messages for the quiz section
    # def instructions_da1_error_message(self, value):
    #     if value != 10:
    #         return "Value is not correct"
    # def instructions_da3_error_message(self, value):
    #     if value != 5:
    #         return "Value is not correct"
    # def instructions_da4_error_message(self, value):
    #         if value != 2:
    #             return "Answer is not correct"

    def vars_for_template(self):
        # num_players = ceil(len(self.subsession.get_players())) if 'test_users' in self.session.config and self.session.config["test_users"] else ceil(self.session.config["market_size"])
        #
        # picture_path_number = str(num_players) if num_players <= 20 else "over_20"
        # picture_path = "instructions/num_players_" + picture_path_number + ".png"
        #
        # label_buyer = "buyer" if num_players == 2 else "buyers"
        # label_seller = "seller" if num_players == 2 else "sellers"

        return {
            'daPlayers': ceil(len(self.subsession.get_players())/2) if 'test_users' in self.session.config and self.session.config["test_users"] else ceil(self.session.config["market_size"]/2),
            'num_of_rounds': self.session.config['num_rounds'] - self.session.config["num_of_test_rounds"],
            'market_time': self.session.config["time_per_round"],
            'freeze_time': self.session.config["delay_before_market_opens"],
            # 'picture': picture_path,
            # 'label_buyer': label_buyer,
            # 'label_seller': label_seller,
            'num_groups': self.session.num_participants/Constants.players_per_group,
            'random_grouping': self.session.config['random_grouping'],
            'quantity_min': self.session.config['quantity_min'],
            'quantity_max': self.session.config['quantity_max'],
            'money_min': self.session.config['money_min'],
            'money_max': self.session.config['money_max'],
            'conversion_value': c(1).to_real_world_currency(self.session),
        }
    def before_next_page(self):
        if self.timeout_happened:
            self.player.participant.vars['instructions_failed'] = True


# I think this is for if you fail the quiz too many times?
class PostInstructions(Page):
    timeout_seconds = 120
    def is_displayed(self):
        return self.subsession.round_number == 1 and 'instructions_failed' in self.player.participant.vars

# Introduces the double auction and the payoffs
class WhatNextDA(Page):
    timeout_seconds = 90
    def is_displayed(self):
        return self.subsession.round_number == 1
    def vars_for_template(self):
        return {
            'payoff_per_point': c(1).to_real_world_currency(self.session),
            'num_of_rounds': Constants.num_rounds - self.session.config["num_of_test_rounds"]
        }

# Tells you what role you will play
class Role(Page):
    timeout_seconds = 15
    def is_displayed(self):
        return self.subsession.round_number == 1
    def before_next_page(self):
        # if self.timeout_happened:
        #     self.player.participant.vars["is_bot"] = True
        # else:
        self.player.participant.vars["is_bot"] = False

# This page is displayted at the conclusion of all the test rounds
class AfterTestrounds(Page):
    timeout_seconds = 20
    def is_displayed(self):
        return self.subsession.round_number == self.session.config["num_of_test_rounds"]
    def before_next_page(self):
        # if self.timeout_happened:
        #     self.player.participant.vars["is_bot"] = True
        # else:
        #
        self.player.participant.vars["is_bot"] = False
    def vars_for_template(self):
        return {
            'num_of_rounds': Constants.num_rounds - self.session.config["num_of_test_rounds"]
        }

# This is a standard wait page
class InitialWait(WaitPage):
    template_name = 'double_auction/InitialWait.html'

    def is_displayed(self):
        """ is displayed """
        return self.subsession.round_number == 1


# This wait page appears after you are assigned a role
class WaitAfterRole(WaitPage):
    template_name = 'double_auction/WaitAfterRole.html'

    def is_displayed(self):
        """ is displayed """
        return self.round_number <= self.session.config['num_rounds']

    def after_all_players_arrive(self):
        """ after all players arrived """

        da_players = self.group.get_players()
        #
        # # All of this is going to need to be changed for the new game
        # # setup valuation table
        # money_max_value = self.session.config['money_max']
        # money_min_value = self.session.config['money_min']
        # money_steps = self.session.config['valuation_increments']
        # num_of_values = int(floor( (money_max_value - money_min_value) / money_steps) + 1)
        #
        # buyer_valuation = [money_min_value + m * money_steps for m in range(num_of_values) ]
        #
        # logger.info("Buyer Valuation %s" % buyer_valuation)
        #
        # # These parameters will all be unnecessary once I implement the new payoff structure
        # cost_max_value = self.session.config['production_costs_max']
        # cost_min_value = self.session.config['production_costs_min']
        # cost_steps = self.session.config['production_costs_increments']
        # num_of_values = int(floor( (cost_max_value - cost_min_value) / cost_steps) + 1)
        #
        # seller_valuation = [cost_min_value + m * cost_steps for m in range(num_of_values) ]
        # logger.info("Seller Valuation %s" % seller_valuation)
        #
        # # This can probably be removed, for the 2-player group
        # # setup display ids
        # num_of_da_players_per_role = int(ceil(len(da_players)/2))
        # seller_ids = [ i+1 for i in range(num_of_da_players_per_role) ]
        # buyer_ids = [ i+1 for i in range(num_of_da_players_per_role) ]
        # random.shuffle(seller_ids)
        # random.shuffle(buyer_ids)

        # Set timer for players
        starttime = time.time() + self.session.config['delay_before_market_opens']
        endtime = starttime + self.session.config['time_per_round']
        self.session.vars["starttime"] = starttime
        self.session.vars["endtime"] = endtime

        # for index, player in enumerate(da_players):
        #     # create bots for missing players
        #
        #     # Generate valuations for the buyers if they don't already have them
        #     if player.participant.vars["role"]=="buyer":
        #         # if not buyer_valuation:
        #         #     buyer_valuation = [ money_min_value + m * money_steps for m in range(num_of_values) ]
        #         #
        #         # random_index = random.randint(0, len(buyer_valuation) - 1)
        #         #
        #         # # This sets the valuation, and will need to be changed
        #         # player.money = buyer_valuation[random_index]
        #         # buyer_valuation.pop(random_index)
        #         player.display_id = buyer_ids.pop()
        #
        #     else:
        #         # Likewise, generate valuations for sellers if they don't already have them
        #         # if len(seller_valuation)==0:
        #         #     seller_valuation = [ cost_min_value + m * cost_steps for m in range(num_of_values) ]
        #         #
        #         # random_index = random.randint(0, len(seller_valuation) - 1 )
        #         #
        #         # # This sets the valuation, and will need to be changed
        #         # player.cost = seller_valuation[random_index]
        #         # seller_valuation.pop(random_index)
        #
        #         player.display_id = seller_ids.pop()

# Standard group assignment stuff on the wait page
class FirstWait(WaitPage):
    template_name = 'double_auction/FirstWait.html'
    # group_by_arrival_time = True

    def is_displayed(self):
        """ is displayed """
        return self.subsession.round_number == 1

    def after_all_players_arrive(self):
        for player in self.subsession.get_players():
            if player.id_in_group % 2 == 0:
                player.participant.vars["role"] = "buyer"
            else:
                player.participant.vars["role"] = "seller"

# Display the results of the auction, successful or not
class Results(Page):
    """ Result Page """
    def get_timeout_seconds(self):
        return self.participant.vars['endtime'] - time.time()

    def is_displayed(self):
        return self.round_number <= self.session.config['num_rounds']

    def vars_for_template(self):
        # transactions = []
        # for g in self.player.group.in_all_rounds():
        #     for p in g.get_players():
        #         if p.value is not None:
        #             if p.participant.vars["role"] == "buyer" and p.match_with is not None:
        #                 quantity = round(p.quantity, 2)
        #                 value = round(p.value, 2)
        #                 cost = round(p.compute_cost(quantity), 2)
        #                 benefit = round(p.compute_value(quantity), 2)
        #                 message = {
        #                     "type": "transactions",
        #                     "round": p.round_number,
        #                     "buyer": p.id,
        #                     "buyer_id_in_group": p.display_id,
        #                     "seller": p.match_with.id,
        #                     "seller_id_in_group": p.match_with.display_id,
        #                     "value": value,
        #                     "quantity": quantity,
        #                     "cost": cost,
        #                     "benefit": benefit,
        #                     "buyer_payoff": round(benefit - value),
        #                     "seller_payoff": round(value - cost),
        #                 }
        #                 transactions.append(message)
        # rounds = [
        #     {
        #         'round_number': player.round_number,
        #         'test_round': True if player.round_number < self.session.config['num_of_test_rounds'] else False,
        #         'quantity': player.quantity if player.match_with else "-",
        #         'price': player.value if player.match_with else '-',
        #         'payoff': player.payoff,
        #     } for player in self.player.in_rounds(1, self.round_number)
        # ]
        # print(self.player.in_all_rounds())
        return {
            # 'transactions': transactions,
            'player_in_all_rounds': reversed(self.player.in_all_rounds()),
            'round_number': self.subsession.round_number - self.session.config["num_of_test_rounds"],
            'num_of_rounds': self.session.config['num_rounds'] - self.session.config["num_of_test_rounds"],
            "cost": round(self.player.compute_cost(self.player.quantity), 2),
            "benefit": round(self.player.compute_value(self.player.quantity), 2),
        }

    def before_next_page(self):
        # if self.timeout_happened:
        #     self.player.participant.vars["is_bot"] = True
        # else:
        self.player.participant.vars["is_bot"] = False


# This is the page where the actual auction occurs
# 'Game' is not a very helpful name for the page.
class Game(Page):
    def get_timeout_seconds(self):
        return self.session.vars["endtime"] - time.time()

    def is_displayed(self):
        return self.round_number <= self.session.config['num_rounds']

    def vars_for_template(self):
        self.participant.vars['starttime'] = time.time()
        self.player.auction_start_time = time.time()
        players = self.group.get_players()

        seller= [ {'id': p.id, 'id_in_group': p.display_id, 'role': p.participant.vars["role"], 'status': '' } for p in players if p.participant.vars["role"] == "seller" ]
        buyer= [ {'id': p.id, 'id_in_group': p.display_id, 'role': p.participant.vars["role"], 'status': '' } for p in players if p.participant.vars["role"] == "buyer" ]
        # This is where itertools is used
        # It converts a list of buyers and a list of sellers into a list of buyer-seller pairs
        # I can probably drop it, if I limit groups to 2 players
        # On the other hand, I might be able to use it to handle multiple offers from the same player
        participant_table = [ list(i) for i in  zip_longest( buyer, seller) ]
        buyer_payoff_data = []
        seller_payoff_data = []
        increment = self.session.config['graph_increments']
        quantity_min = self.session.config['quantity_min']
        quantity_max = self.session.config['quantity_max']
        num_of_quantities = int(floor((quantity_max - quantity_min) / increment) + 1)


        for q in range(0, num_of_quantities):
            quantity = quantity_min + q * increment
            buyer_payoff_data.append((quantity, self.player.compute_value(quantity)))
            seller_payoff_data.append((quantity, self.player.compute_cost(quantity)))
        print("It should be using this group: " + str(self.group.id_in_subsession))
        return {
            'group': self.group.id_in_subsession,
            'minValue': self.session.config["money_min"],
            'maxValue': self.session.config["money_max"],
            'minQuantity': self.session.config["quantity_min"],
            'maxQuantity': self.session.config["quantity_max"],
            'money_increment': self.session.config["money_increment"],
            'quantity_increment': self.session.config["quantity_increment"],
            'lock': True if self.player.match_with else False,
            'participants': participant_table,
            'seconds_to_start': self.session.vars["starttime"] - time.time(),
            'round_number': self.subsession.round_number - self.session.config["num_of_test_rounds"],
            'num_of_rounds': self.session.config['num_rounds'] - self.session.config["num_of_test_rounds"],
            'vm': self.session.config['value_multiplier'],
            'vx': self.session.config['value_exponent'],
            'cm': self.session.config['cost_multiplier'],
            'cx': self.session.config['cost_exponent'],
            'buyer_payoff_data': buyer_payoff_data,
            'seller_payoff_data': seller_payoff_data,
            'increment': increment,
        }

    def before_next_page(self):
        # set timeout to small amount if is_bot
        # if 'is_bot' in self.participant.vars and self.participant.vars['is_bot']:
        #     self.participant.vars['endtime'] = time.time()
        # else:
        self.participant.vars['endtime'] = time.time() + 15
        self.player.auction_duration = time.time() - self.participant.vars['starttime']
        # Delete last proposed offer if no trade occurred
        if not self.player.match_with:
            self.player.value = None
            self.player.quantity = None



# Results at the end of each round
class EndResults(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        paying_rounds = self.session.vars['paying_rounds']
        paying_round1 = paying_rounds[0]
        paying_round2 = paying_rounds[1]
        if paying_round2 < paying_round1:
            (paying_round1, paying_round2) = (paying_round2, paying_round1)
        round1_payoff = self.player.in_round(paying_round1).payoff
        round2_payoff = self.player.in_round(paying_round2).payoff
        final_payoff = round1_payoff + round2_payoff
        # rounds = [
        #     {
        #         'round_number': player.round_number,
        #         'test_round': True if player.round_number < self.session.config['num_of_test_rounds'] else False,
        #         'quantity': player.quantity if player.match_with else "-",
        #         'price': player.value if player.match_with else '-',
        #         'payoff': player.payoff,
        #         'this_round_pays': player.round_number in paying_rounds,
        #     } for player in self.player.in_rounds(1, self.session.config["num_rounds"])
        # ]
        # self.player.participant.vars["da_payoffs"] = rounds
        return {
            'player_in_all_rounds': self.player.in_rounds(1, self.session.config["num_rounds"]),
            'paying_rounds': paying_rounds,
            'paying_round1': paying_round1,
            'paying_round2': paying_round2,
            'payoff1_points': round1_payoff,
            'payoff1_money': c(round1_payoff).to_real_world_currency(self.session),
            'payoff2_points': round2_payoff,
            'payoff2_money': c(round2_payoff).to_real_world_currency(self.session),
            'payoff_points': final_payoff,
            'payoff_money': c(final_payoff).to_real_world_currency(self.session),
            'showup_fee': self.session.config['participation_fee'],
        }



page_sequence = [
    FirstWait,
    Instructions,
    # PostInstructions,
    # WhatNextDA,
    # InitialWait,
    Role,
    WaitAfterRole,
    Game,
    Results,
    AfterTestrounds,
    EndResults
]
