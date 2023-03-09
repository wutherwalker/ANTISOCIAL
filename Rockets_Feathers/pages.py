from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        market_size = self.session.config['market_size']
        return {
            'market_size': market_size,
            'other_firms': market_size-1,
            'point_value': c(1).to_real_world_currency(self.session),
        }


class Decision(Page):
    form_model = 'player'
    form_fields = ['price']

    def is_displayed(self):
        return self.round_number <= self.session.vars['num_rounds']

    def vars_for_template(self):
        payoff_matrix = []

        increment = self.session.config['increment']
        # This setup ensures that minimum profit on the diagonal is positive
        # It's still possible to take a loss if you set a much higher price than others
        minprice = self.player.cost - self.session.config['payoff_adjustment'] / \
                   self.session.config['real_world_currency_per_point'] / self.session.config['demand_constant']
        minprice = increment * int(minprice/increment + 1)
        cost_USD = c(self.player.cost).to_real_world_currency(self.session)
        maxprice = minprice + self.session.config['price_range']

        num_steps = int((maxprice-minprice)/increment)+1

        demand_constant = self.session.config['demand_constant']
        demand_multiplier = self.session.config['demand_multiplier']
        payoff_adjustment = self.session.config['payoff_adjustment']

        prices = []

        for i in range(0, num_steps):
            price = c(minprice + i*increment).to_real_world_currency(self.session)
            prices.append(price)
            # Create new row
            payoff_matrix.append([])

            for j in range(0, num_steps):
                other_price = c(minprice + j*increment).to_real_world_currency(self.session)
                demand = demand_constant - demand_multiplier * (price - other_price)
                payoff = demand * (price - cost_USD) + payoff_adjustment
                # Get most recent item
                payoff_matrix[i].append(payoff)

        return {
            'cost': c(self.player.cost).to_real_world_currency(self.session),
            'round_number': self.round_number,
            'payoff_matrix': payoff_matrix,
            'prices': prices,
            'rows': range(0, len(payoff_matrix)),
            'cols': range(0, len(payoff_matrix[0])),
        }


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number <= self.session.vars['num_rounds']

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def is_displayed(self):
        return self.round_number <= self.session.vars['num_rounds']

    def vars_for_template(self):
        return {
            'price': self.player.price,
            'average_price': self.group.average_price,
            'payoff': self.player.payoff,
            'round_number': self.round_number,
        }


class FinalOutcome(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
    Instructions,
    Decision,
    ResultsWaitPage,
    Results,
    FinalOutcome,
]
