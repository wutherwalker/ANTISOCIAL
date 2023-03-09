from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'ns_experiment_two'
    players_per_group = 2   #***
    num_rounds = 50 #***


    pizza_types = ["Cheese", "Pepperoni", "Hawaiian", "Mushroom and Sausage", "Tomato & Basil", "BBQ Chicken", "Meat Lover's", "Vegan"]   #***
    movie_types = ["Horror", "Comedy", "Action", "Musical", "Documentary", "Animated", "Sci-Fi", "Drama"]   #***


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()  # ***

        else:
            self.group_like_round(1)    #***


class Group(BaseGroup):
    def set_payoffs(self):
        if self.subsession.round_number <= 2:
            for p in self.get_players():
                p.payoff = c(0)
        else:
            if self.get_player_by_id(1).round_result == "Agree":
                for p in self.get_players():
                    best_choice = p.best_choice
                    if p.participant.vars['item_type'] == "movies":
                        index = Constants.movie_types.index(best_choice)
                        p.payoff = p.participant.vars['movie_payoffs'][index]
                    else:
                        index = Constants.pizza_types.index(best_choice)
                        p.payoff = p.participant.vars['pizza_payoffs'][index]

            else:
                for p in self.get_players():
                    p.payoff = c(0)


class Player(BasePlayer):
    likert_scale = models.StringField(choices=random.sample(["am indifferent to", "love", "sometimes enjoy", "hate",
                                                             "am not fond of", "am interested in",
                                                            "am generally displeased by"], 7))
    # ***
    actother = models.FloatField()  #***


    # ***
    opp_util_model_1 = models.FloatField()
    opp_util_model_2 = models.FloatField()
    opp_util_model_3 = models.FloatField()
    opp_util_model_4 = models.FloatField()
    opp_util_model_5 = models.FloatField()
    opp_util_model_6 = models.FloatField()
    opp_util_model_7 = models.FloatField()
    opp_util_model_8 = models.FloatField()

    tradeoff_constant = models.FloatField() #***

    best_choice = models.StringField(initial="")    #***
    round_result = models.StringField(initial="")   #***

    # *** Everything below this point stays...I think
    def get_partner(self):
        return self.get_others_in_group()[0]

    def set_opp_model(self, likert_outcome, likert_value, opp_utils):
        # opp_util_model = [self.opp_util_model_1, self.opp_util_model_2, self.opp_util_model_3, self.opp_util_model_4]
        outcome_index = self.participant.vars['outcomes'].index(likert_outcome)
        p = float(likert_value) / opp_utils[outcome_index]

        # opp_util_model[outcome_index] = likert_value
        if outcome_index == 0:
            self.opp_util_model_1 = likert_value
        elif outcome_index == 1:
            self.opp_util_model_2 = likert_value
        elif outcome_index == 2:
            self.opp_util_model_3 = likert_value
        elif outcome_index == 3:
            self.opp_util_model_4 = likert_value
        elif outcome_index == 4:
            self.opp_util_model_5 = likert_value
        elif outcome_index == 5:
            self.opp_util_model_6 = likert_value
        elif outcome_index == 6:
            self.opp_util_model_7 = likert_value
        else:
            self.opp_util_model_8 = likert_value

        self.opp_util_model_1 = p * opp_utils[0]
        self.opp_util_model_2 = p * opp_utils[1]
        self.opp_util_model_3 = p * opp_utils[2]
        self.opp_util_model_4 = p * opp_utils[3]
        self.opp_util_model_5 = p * opp_utils[4]
        if self.participant.vars['num_items'] == 8:
            self.opp_util_model_6 = p * opp_utils[5]
            self.opp_util_model_7 = p * opp_utils[6]
            self.opp_util_model_8 = p * opp_utils[7]

    def set_tradeoff_constant(self):
        numerator = max(self.participant.vars['self_utils']) - min(self.participant.vars['self_utils'])
        if self.participant.vars['num_items'] == 5:
            opp_util_model = [self.opp_util_model_1, self.opp_util_model_2, self.opp_util_model_3,
                              self.opp_util_model_4, self.opp_util_model_5]
        else:
            opp_util_model = [self.opp_util_model_1, self.opp_util_model_2, self.opp_util_model_3,
                              self.opp_util_model_4, self.opp_util_model_5, self.opp_util_model_6,
                              self.opp_util_model_7, self.opp_util_model_8]
        denominator = max(opp_util_model) - min(opp_util_model)
        self.tradeoff_constant = numerator/denominator

    def pick_pair(self, seed_value):
        non_success_pairs = [pair for pair in self.participant.vars['outcome_pairs'] if pair not in self.participant.vars['success_pairs']]
        random.seed(seed_value)
        index = random.randint(0, len(non_success_pairs) - 1)
        return non_success_pairs[index]

    def best_option(self, option1, option2):
        if self.participant.vars['num_items'] == 5:
            opp_util_model = [self.opp_util_model_1, self.opp_util_model_2, self.opp_util_model_3,
                              self.opp_util_model_4, self.opp_util_model_5]
        else:
            opp_util_model = [self.opp_util_model_1, self.opp_util_model_2, self.opp_util_model_3,
                              self.opp_util_model_4, self.opp_util_model_5, self.opp_util_model_6,
                              self.opp_util_model_7, self.opp_util_model_8]
        opt1_index = self.participant.vars['outcomes'].index(option1)
        opt2_index = self.participant.vars['outcomes'].index(option2)
        self_vals = (self.participant.vars['self_utils'][opt1_index], self.participant.vars['self_utils'][opt2_index])
        opp_vals = (opp_util_model[opt1_index], opp_util_model[opt2_index])
        joint_opt1 = self_vals[0] + opp_vals[0]
        joint_opt2 = self_vals[1] + opp_vals[1]
        if joint_opt1 > joint_opt2:
            choice = option1
        elif joint_opt1 < joint_opt2:
            choice = option2
        else:
            coin_flip = random.randint(0, 1)
            if coin_flip == 0:
                choice = option1
            else:
                choice = option2
        self.best_choice = choice

    def update_tradeoff_constant(self, p):
        self.tradeoff_constant = p * self.in_round(self.subsession.round_number-1).tradeoff_constant

    def get_prev_opp_model(self):
        self_last_round = self.in_round(self.subsession.round_number-1)
        # prev_opp_util_model = [self_last_round.opp_util_model_1, self_last_round.opp_util_model_2, self_last_round.opp_util_model_3, self_last_round.opp_util_model_4]
        # opp_util_model = [self.opp_util_model_1, self.opp_util_model_2, self.opp_util_model_3, self.opp_util_model_4]

        # for i in range(len(opp_util_model)):
        #     opp_util_model[i] = p*prev_opp_util_model[i]

        self.opp_util_model_1 = self_last_round.opp_util_model_1
        self.opp_util_model_2 = self_last_round.opp_util_model_2
        self.opp_util_model_3 = self_last_round.opp_util_model_3
        self.opp_util_model_4 = self_last_round.opp_util_model_4
        self.opp_util_model_5 = self_last_round.opp_util_model_5
        if self.participant.vars['num_items'] == 8:
            self.opp_util_model_6 = self_last_round.opp_util_model_6
            self.opp_util_model_7 = self_last_round.opp_util_model_7
            self.opp_util_model_8 = self_last_round.opp_util_model_8

    def join_lists(self, list1, list2):
        '''For list1 = [l1, l2, l3, ...] and list2 = [m1, m2, m3, ...], returns [(l1, m1), (l2, m2), ...].
        Assumes list1 and list2 are the same length.'''

        joined_list = []
        for i in range(len(list1)):
            joined_list.append((list1[i], list2[i]))

        return joined_list

    def round_to_quarter(self, value):
        two_decimal = round(value, 2)
        (dollars, cents) = str(two_decimal).split(".")
        dollars = int(dollars)
        cents = int(cents)
        if cents > 0 and cents < 25:
            cents = 25
        elif cents > 25 and cents < 50:
            cents = 50
        elif cents > 50 and cents < 75:
            cents = 75
        elif cents > 75:
            cents = 0
            dollars += 1

        return dollars + cents*0.01

