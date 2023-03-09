from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from math import factorial
import datetime
import random
import time


class WaitingPageNewApp(WaitPage):
    template_name = 'accom_dynam_two/WaitingPageNewApp.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == 1

    def after_all_players_arrive(self):
        for g in self.subsession.get_groups():
            num_items = 5 #random.choice([5, 8])  # ***
            item_type = random.choice(["pizzas", "movies"])  # ***

            if item_type == "pizzas":
                outcomes = random.sample(Constants.pizza_types, num_items)  # ***
            elif item_type == "movies":
                outcomes = random.sample(Constants.movie_types, num_items)  # ***
            else:
                outcomes = []

            outcome_pairs = [[x, y] for x in outcomes for y in outcomes if outcomes.index(x) < outcomes.index(y)]

            for p in g.get_players():
                #Redefine variables for the new round
                p.participant.vars['num_items'] = num_items
                p.participant.vars['item_type'] = item_type
                p.participant.vars['outcomes'] = outcomes
                p.participant.vars['randout'] = random.choice(outcomes)
                p.participant.vars['outcome_pairs'] = outcome_pairs
                # p.participant.vars['expiry'] = []

                #Pull utility values from set_util in the first app
                self_utils = []
                for i in outcomes:
                    if item_type == 'pizzas':
                        index = Constants.pizza_types.index(i)
                        util = p.participant.vars['pizza_utils'][index]
                    else:
                        index = Constants.movie_types.index(i)
                        util = p.participant.vars['movie_utils'][index]
                    self_utils.append(util)
                p.participant.vars['self_utils'] = self_utils

                #Reset other participant variables
                p.participant.vars['likert_info'] = ('x', 'y')  # (outcome, likert_answer) #***
                p.participant.vars['scale_max_value'] = 0.5
                p.participant.vars['options_to_display'] = ('x', 'y')  # ***
                p.participant.vars['success_pairs'] = []  # ***
                p.participant.vars['disagree_count'] = 0  # ***
                p.participant.vars['end_experiment'] = False  # ***
                p.participant.vars['reach_equilibrium'] = False  # ***


class SetOppModelPage1(Page):
    form_model = 'player'
    form_fields = ['likert_scale']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return{
            'random_outcome': self.participant.vars['randout'],
            'item_type': self.participant.vars['item_type'],
            'num_items': len(self.participant.vars['outcomes']),
            'outcomes': self.participant.vars['outcomes'],
        }

    def before_next_page(self):
        self.participant.vars['likert_info'] = (self.participant.vars['randout'], self.player.likert_scale)


class SetOppModelPage2(Page):
    form_model = 'player'
    form_fields = ['actother']

    def vars_for_template(self):
        return {
            'opp_likert_answer': self.player.get_partner().participant.vars['likert_info'][1],
            'opp_likert_outcome': self.player.get_partner().participant.vars['likert_info'][0],
            'item_type': self.participant.vars['item_type'][:-1],
            'item_type_plural': self.participant.vars['item_type']
        }

    def is_displayed(self):
        return self.subsession.round_number == 2

    def before_next_page(self):
        self.player.set_opp_model(self.player.in_round(self.round_number - 1).get_partner().participant.vars['randout'],
                                  self.player.actother, self.player.get_partner().participant.vars['self_utils'])
        self.player.set_tradeoff_constant()

        all_vals = list(self.participant.vars['self_utils'])
        if self.participant.vars['num_items'] == 5:
            all_vals.extend([self.player.opp_util_model_1, self.player.opp_util_model_2, self.player.opp_util_model_3,
                             self.player.opp_util_model_4, self.player.opp_util_model_5])
        else:
            all_vals.extend([self.player.opp_util_model_1, self.player.opp_util_model_2, self.player.opp_util_model_3,
                             self.player.opp_util_model_4, self.player.opp_util_model_5, self.player.opp_util_model_6,
                             self.player.opp_util_model_7, self.player.opp_util_model_8])
        magnitudes = [abs(x) for x in all_vals]
        self.participant.vars['scale_max_value'] = max(max(magnitudes), 0.5)


class WaitingPageTimer(WaitPage):
    template_name = 'accom_dynam_two/WaitingPageTimer.html'

    def is_displayed(self):
        return self.subsession.round_number == 2

    def after_all_players_arrive(self):
        # user has 10 minutes to complete as many pages as possible
        self.group.get_player_by_id(1).participant.vars['expiry'] = time.time() + 2 * 60
        self.group.get_player_by_id(2).participant.vars['expiry'] = time.time() + 2 * 60


class AccomDynamPage(Page):
    form_model = 'player'
    form_fields = ['opp_util_model_1', 'opp_util_model_2', 'opp_util_model_3', 'opp_util_model_4',
                   'opp_util_model_5', 'opp_util_model_6', 'opp_util_model_7', 'opp_util_model_8']

    timer_text = 'Time left to complete interaction with Second Partner:'

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.subsession.round_number >= 3 and self.participant.vars['end_experiment'] == False

    def vars_for_template(self):
        for p in self.group.get_players():
            p.get_prev_opp_model()

        self.group.get_player_by_id(1).participant.vars['options_to_display'] = self.group.get_player_by_id(1).pick_pair(self.subsession.round_number)
        self.group.get_player_by_id(2).participant.vars['options_to_display'] = self.group.get_player_by_id(1).participant.vars['options_to_display']
        rand_index = random.randint(0, 1)
        if rand_index == 0:
            option1, option2 = self.group.get_player_by_id(1).participant.vars['options_to_display']
        else:
            option2, option1 = self.group.get_player_by_id(1).participant.vars['options_to_display']

        self.player.best_option(option1, option2)
        self.player.get_partner().best_option(option1, option2)
        result = int(self.player.best_choice == self.player.get_partner().best_choice)   #0=disagreement, 1=agreement

        if result == 0:
            self.player.round_result = "Disagree"
            # self.participant.vars['disagree_count'] += 1
            # self.participant.vars['success_pairs'] = []
        else:
            self.player.round_result = "Agree"
            # self.participant.vars['success_pairs'].append(self.participant.vars['options_to_display'])

        if self.participant.vars['num_items'] == 5:
            opp_model = [self.player.opp_util_model_1, self.player.opp_util_model_2, self.player.opp_util_model_3, self.player.opp_util_model_4, self.player.opp_util_model_5]
        else:
            opp_model = [self.player.opp_util_model_1, self.player.opp_util_model_2, self.player.opp_util_model_3, self.player.opp_util_model_4,
                         self.player.opp_util_model_5, self.player.opp_util_model_6, self.player.opp_util_model_7, self.player.opp_util_model_8]
        payoff_sess = []
        for i in range(len(self.participant.vars['self_utils'])):
            payoff_sess.append("{:0.2f}".format(self.participant.vars['self_utils'][i] + 2))

        return {
            'round_number': self.subsession.round_number - 2,
            'num_items': self.participant.vars['num_items'],
            'self_utils': self.participant.vars['self_utils'],
            'opp_model': opp_model,
            'scale_max_value': self.participant.vars['scale_max_value'],
            'option1': option1,
            'option2': option2,
            'self_best_choice': self.player.best_choice,
            'opp_best_choice': self.player.get_partner().best_choice,
            'result': self.player.round_result,
            'table': self.player.join_lists(self.participant.vars['outcomes'], payoff_sess),
            'item_type': self.participant.vars['item_type'],
        }

    def before_next_page(self):
        self_last_round = self.player.in_round(self.subsession.round_number - 1)
        if self.timeout_happened:
            self.player.opp_util_model_1 = self_last_round.opp_util_model_1
            self.player.opp_util_model_2 = self_last_round.opp_util_model_2
            self.player.opp_util_model_3 = self_last_round.opp_util_model_3
            self.player.opp_util_model_4 = self_last_round.opp_util_model_4
            self.player.opp_util_model_5 = self_last_round.opp_util_model_5
            if self.participant.vars['num_items'] == 8:
                self.player.opp_util_model_6 = self_last_round.opp_util_model_6
                self.player.opp_util_model_7 = self_last_round.opp_util_model_7
                self.player.opp_util_model_8 = self_last_round.opp_util_model_8
            p = self.player.opp_util_model_1 / self_last_round.opp_util_model_1
            self.player.update_tradeoff_constant(p)
        else:
            p = self.player.opp_util_model_1 / self_last_round.opp_util_model_1
            self.player.update_tradeoff_constant(p)


class WaitingPage(WaitPage):
    template_name = 'accom_dynam_two/WaitingPage.html'

    def after_all_players_arrive(self):
        self.group.set_payoffs()

        if self.subsession.round_number > 2:
            for p in self.group.get_players():
                if p.round_result == "Agree":
                    p.participant.vars['success_pairs'].append(p.participant.vars['options_to_display'])
                else:
                    p.participant.vars['disagree_count'] += 1
                    p.participant.vars['success_pairs'] = []

            if len(self.group.get_player_by_id(1).participant.vars['success_pairs']) == len(self.group.get_player_by_id(1).participant.vars['outcome_pairs']):
                for p in self.group.get_players():
                    p.participant.vars['end_experiment'] = True
                    p.participant.vars['reach_equilibrium'] = True
            elif self.group.get_player_by_id(1).participant.vars['expiry'] - time.time() < 2 or \
                    self.group.get_player_by_id(2).participant.vars['expiry'] - time.time() < 2:
                for p in self.group.get_players():
                    p.participant.vars['end_experiment'] = True
                    p.participant.vars['reach_equilibrium'] = False
            else:
                for p in self.group.get_players():
                    p.participant.vars['end_experiment'] = False

    def vars_for_template(self):
        return {
            'a': self.participant.vars['end_experiment'],
            'b': self.participant.vars['reach_equilibrium'],
            'next_round': self.subsession.round_number - 1,
        }

    def is_displayed(self):
        return self.subsession.round_number == 1 or self.subsession.round_number > 2


# class PersonalityTestPage(Page):
#     def is_displayed(self):
#         return self.participant.vars['end_experiment']


class Results(Page):
    def is_displayed(self):
        return self.participant.vars['end_experiment']

    def vars_for_template(self):
        total_rounds = (self.subsession.round_number - 2)
        try:
            paying_rounds = random.sample(range(1, total_rounds+1), 5)
        except ValueError:  #less than 5 rounds played in total
            paying_rounds = []
        player_in_paying_rounds = []

        for round_num in paying_rounds:
            player_in_paying_rounds.append((round_num, self.player.in_round(round_num + 2)))

        cumulative_payoff = sum([p[1].payoff for p in player_in_paying_rounds])

        if self.participant.vars['reach_equilibrium']:
            eq_payoff = c(4)
        else:
            eq_payoff = c(0)

        total_payoff = cumulative_payoff + eq_payoff + c(7)

        payment_info = {
            'date': datetime.datetime.today().strftime("%B %d, %Y"),
            'total_rounds': total_rounds,
            'paying_rounds': sorted(paying_rounds),
            'player_in_paying_rounds': sorted(player_in_paying_rounds),
            'cumulative_payoff': cumulative_payoff,
            'reach_eq_payoff': eq_payoff,
            'total_earned_payoff': cumulative_payoff + eq_payoff,
            'total_payoff': total_payoff,
            'rounded_total': c(self.player.round_to_quarter(total_payoff)),
            'reach_equilibrium': self.player.participant.vars['reach_equilibrium'],
            'num_rounds_agree': total_rounds - self.participant.vars['disagree_count'],
        }

        self.participant.vars['payoff_history'][2] = payment_info

        return payment_info

    def app_after_this_page(self, upcoming_apps):
        return 'accom_dynam_three'


page_sequence = [
    WaitingPageNewApp,
    SetOppModelPage1,
    SetOppModelPage2,
    WaitingPageTimer,
    AccomDynamPage,
    WaitingPage,
    Results,

]
