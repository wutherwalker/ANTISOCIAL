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
    name_in_url = 'ns_experiment'
    players_per_group = 2   #***
    num_rounds = 50 #***

    pizza_types = ["Cheese", "Pepperoni", "Hawaiian", "Mushroom and Sausage", "Tomato & Basil", "BBQ Chicken", "Meat Lover's", "Vegan"]   #***
    movie_types = ["Horror", "Comedy", "Action", "Musical", "Documentary", "Animated", "Sci-Fi", "Drama"]   #***


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()  # ***
            for g in self.get_groups():
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
                    p.participant.vars['num_items'] = num_items
                    p.participant.vars['item_type'] = item_type
                    p.participant.vars['outcomes'] = outcomes
                    p.participant.vars['randout'] = random.choice(outcomes)  # ***
                    p.participant.vars['outcome_pairs'] = outcome_pairs


            for player in self.get_players():
                # player.participant.vars['self_utils'] = list(np.zeros(len(self.session.vars['outcomes'])))
                # player.participant.vars['opp_util_model'] = list(np.zeros(len(self.session.vars['outcomes'])))

                player.participant.vars['movie_utils'] = [0]*(len(Constants.movie_types))
                player.participant.vars['pizza_utils'] = [0]*(len(Constants.pizza_types))
                player.participant.vars['self_utils'] = [0]*(player.participant.vars['num_items'])    #***

                player.participant.vars['likert_info'] = ('x', 'y')   #(outcome, likert_answer) #***
                player.participant.vars['scale_max_value'] = 0.5
                player.participant.vars['options_to_display'] = ('x', 'y')  #***
                player.participant.vars['success_pairs'] = []   #***
                player.participant.vars['disagree_count'] = 0   #***
                player.participant.vars['end_experiment'] = False   #***
                player.participant.vars['reach_equilibrium'] = False    #***
                # player.participant.vars['expiry'] = None  #***
                player.participant.vars['payoff_history'] = dict()

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
    gender = models.StringField(choices=['Male', 'Female'],
                                verbose_name='Which gender do you currently identify with the most?',
                                widget=widgets.RadioSelect,
                                blank=True)
    major = models.StringField(verbose_name='What is your major at UCI?',
                               blank=True)
    langs = models.StringField(verbose_name='What languages are you proficient in? Please list them in the order in which you learned them and separate them with a forward slash (/).',
                               blank=True)
    attend_hs = models.StringField(choices=['Yes', 'No'],
                                   verbose_name='Did you attend high school?',
                                   widget=widgets.RadioSelect,
                                   blank=True)
    hs_input = models.StringField(verbose_name='If yes, please give the name of the high school you attended.',
                                  blank=True)

    likert_scale = models.StringField(choices=random.sample(["am indifferent to", "love", "sometimes enjoy", "hate",
                                                             "am not fond of", "am interested in",
                                                            "am generally displeased by"], 7))
    # ***

    # outcome1 = models.FloatField()
    # outcome2 = models.FloatField()
    # outcome3 = models.FloatField()
    # outcome4 = models.FloatField()
    # outcome5 = models.FloatField()
    # if Constants.num_items == 8:
    #     outcome6 = models.FloatField()
    #     outcome7 = models.FloatField()
    #     outcome8 = models.FloatField()

    m_outcome1 = models.FloatField()
    m_outcome2 = models.FloatField()
    m_outcome3 = models.FloatField()
    m_outcome4 = models.FloatField()
    m_outcome5 = models.FloatField()
    m_outcome6 = models.FloatField()
    m_outcome7 = models.FloatField()
    m_outcome8 = models.FloatField()

    p_outcome1 = models.FloatField()
    p_outcome2 = models.FloatField()
    p_outcome3 = models.FloatField()
    p_outcome4 = models.FloatField()
    p_outcome5 = models.FloatField()
    p_outcome6 = models.FloatField()
    p_outcome7 = models.FloatField()
    p_outcome8 = models.FloatField()

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

    participant_vars_dump = models.StringField()

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

        # for i in range(len(self.session.vars['outcomes'])):
        #     p = opp_utils[i] / opp_utils[outcome_index]
        #     opp_util_model[i] = p * likert_value

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

