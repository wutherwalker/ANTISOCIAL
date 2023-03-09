from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random, math

author = 'Patrick Julius'

doc = """
This app implements a simple individual choice task, choosing how much to borrow 
or save in order to smooth consumption under a volatile income process. 

The participants are assessed for risk aversion using a series of lottery choices.

They then are tested for backward induction capacity using a Tower of Hanoi puzzle
and a new version of the Cognitive Reflection Test.
"""


class Constants(BaseConstants):
    name_in_url = 'Savings'
    players_per_group = None
    # num_rounds = 30
    num_rounds = 4
    safe_choice_constant = 4.44
    safe_choice_list = [4.67, 4.89, 5.11, 5.33, 5.56, 5.78, 6.00, 6.22, 6.44, 6.67]
    risky_choice_constant = 2.78
    risky_choice_list = [5.58, 6.03, 6.44, 6.89, 7.36, 7.94, 8.72, 9.83, 12.50, 13.06]


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['paying_round_1'] = random.randint(1, int(Constants.num_rounds/2))
            self.session.vars['paying_round_2'] = random.randint(int(Constants.num_rounds/2)+1, Constants.num_rounds)

            if random.random() < 0.5:
                self.session.vars['Hanoi_paid'] = True
            else:
                self.session.vars['Hanoi_paid'] = False
            print("Hanoi paid? " + str(self.session.vars['Hanoi_paid']))
            self.session.vars['paying_gamble'] = random.randint(1, 10)

        min = self.session.config['income_min']
        max = self.session.config['income_max']
        for player in self.get_players():
            player.income1 = random.randint(min, max)
            player.income2 = random.randint(min, max)
            player.income3 = random.randint(min, max)

            if self.session.config['constrained_first']:
                if self.round_number <= Constants.num_rounds/2:
                    player.borrowing_constrained = True
                else:
                    player.borrowing_constrained = False
            else:
                if self.round_number <= Constants.num_rounds/2:
                        player.borrowing_constrained = False
                else:
                    player.borrowing_constrained = True



class Group(BaseGroup):
    pass


def make_risk_choice(step):
    safe_choice = Constants.safe_choice_list[step]
    risky_choice = Constants.risky_choice_list[step]
    return models.IntegerField(
        choices=[1, 2],
        label="Lottery 1: 50% chance of $" + str(round(Constants.safe_choice_constant, 2)) + \
              ", 50% chance of $" + str(round(safe_choice, 2)) + \
              "; Lottery 2: 50% chance of $" + str(round(Constants.risky_choice_constant, 2)) + \
              ", 50% chance of $" + str(round(risky_choice, 2)),
        widget=widgets.RadioSelectHorizontal()
    )


class Player(BasePlayer):
    borrowing_constrained = models.BooleanField()
    income1 = models.CurrencyField()
    income2 = models.CurrencyField()
    income3 = models.CurrencyField()

    # For the practice round
    consumption0 = models.CurrencyField(
        initial=1,
        min=1,
        widget=widgets.Slider(),
    )

    consumption1 = models.CurrencyField(
        initial=1,
        min=1,
        widget=widgets.Slider(),
    )
    consumption2 = models.CurrencyField(
        initial=1,
        min=1,
        widget=widgets.Slider(),
    )
    consumption3 = models.CurrencyField()
    savings1 = models.CurrencyField()
    savings2 = models.CurrencyField()
    # This is kludgy, but oTree doesn't seem to give me any choice;
    # in the table it needs to not be a Currency variable or it will show up as "points"
    real_payoff_dollars = models.IntegerField()
    real_payoff_cents = models.IntegerField()

    # Choice 1 is risk-averse option, Choice 2 is risk-seeking option
    risk_answer_01 = make_risk_choice(0)
    risk_answer_02 = make_risk_choice(1)
    risk_answer_03 = make_risk_choice(2)
    risk_answer_04 = make_risk_choice(3)
    risk_answer_05 = make_risk_choice(4)
    risk_answer_06 = make_risk_choice(5)
    risk_answer_07 = make_risk_choice(6)
    risk_answer_08 = make_risk_choice(7)
    risk_answer_09 = make_risk_choice(8)
    risk_answer_10 = make_risk_choice(9)


    risk_payoff = models.CurrencyField()

    # Number of moves taken to solve Hanoi game; 99 indicates timed out
    Hanoi_moves = models.IntegerField(
        # initial=99,
    )

    Hanoi_success = models.BooleanField()
    Hanoi_payoff = models.CurrencyField()
    Hanoi_time = models.FloatField()

    CRT_answer_1 = models.IntegerField(
        label="",
    )
    CRT_answer_2 = models.IntegerField(
        label="",
    )
    CRT_answer_3 = models.IntegerField(
        label="",
    )
    CRT_answer_4 = models.StringField(
        label="",
        choices=['lost money in the stock market',
                 'broken even in the stock market',
                 'made money in the stock market'],
        widget=widgets.RadioSelect(),
    )

    age = models.IntegerField(
        label="What is your age?"
    )
    gender = models.StringField(
        label="What is your gender?",
        choices=["Man", "Woman", "Other"],
    )
    major = models.StringField(
        label="What is your major?",
    )
    GPA = models.FloatField(
        label="What is your GPA?",
    )

    def consumption0_max(self):
        return self.income1 + self.session.config['income_min'] - 1

    def consumption1_max(self):
        return self.income1 + self.session.config['income_min'] - 1

    def consumption2_max(self):
        if self.borrowing_constrained:
            return self.income2 + self.savings1
        else:
            return self.income2 + self.savings1 + self.session.config['income_min'] - 1

    def get_payoff(self, consumption):
        return self.session.config['utility_multiplier'] * math.log(consumption)

