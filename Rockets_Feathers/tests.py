from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants as C
import random

# I don't like making this global, but I can't seem to save it in the participant
strategies = list(1000 for t in range(0, 400))


class PlayerBot(Bot):
    # cases = ['CUC', 'NBR', 'Nash', 'collusive', 'mix1', 'mix2', 'mix3']
    cases = ['NBR']

    def play_round(self):
        N = C.players_per_group
        A = self.player.subsession.session.config['demand_constant']
        D = 0
        B = self.player.subsession.session.config['demand_multiplier']

        if self.round_number == 1:
            yield(pages.Instructions)

        if self.round_number <= self.session.vars['num_rounds']:
            if self.case == 'NBR' or self.case == 'noisy':
                if self.round_number == 1:
                    yield(pages.Decision, {'price': 50})
                else:
                    last_time = self.player.in_round(self.round_number - 1)
                    # Naive best response function
                    new_price = A/(2*(D+B/N)) + ((D+B/N)-B)/(2*(D+B/N))*last_time.other_average + self.player.cost/2
                    if self.case == 'NBR':
                        yield(pages.Decision, {'price': new_price})
                    elif self.case == 'noisy':
                        yield (pages.Decision, {'price': new_price + random.randint(-2, 2)})
            elif self.case == 'Nash':
                best_price = A/(D+B)+(D+B/N)/(D+B)*self.player.cost
                yield(pages.Decision, {'price': best_price})

            elif self.case == 'CUC':
                # Conservative undercutting
                if self.round_number == 1:
                    yield(pages.Decision, {'price': self.player.cost + random.randint(0, 100)})
                else:
                    last_time = self.player.in_round(self.round_number - 1)
                    min_price = min(p.price for p in last_time.group.get_players())
                    yield(pages.Decision, {'price': max(min_price - 1, self.player.cost + 1)})
            elif self.case == 'collusive':
                best_price = A/(2*B) + self.player.cost / 2
                yield (pages.Decision, {'price': best_price})

            elif self.case == 'Markov':
                # Markov reinforcement learning with 5-point price increments
                if self.round_number <= 50:
                    yield (pages.Decision, {'price': 5*random.randint(0, 20)})
                    if self.player.other_average > 100:
                        self.player.other_average = 100
                    strategies[int(self.player.other_average/5)*20 + int(self.player.price/5)] += self.player.payoff
                else:
                    last_time = self.player.in_round(self.round_number - 1)
                    p = random.random()
                    q = 0
                    denom = sum(strategies[int(last_time.other_average/5)*20:int(last_time.other_average/5)*20+20])
                    for t in range(0, 20):
                        q += strategies[int(last_time.other_average/5)*20 + t]
                        if p*denom - q < strategies[int(last_time.other_average/5)*20 + t]:
                            break
                    yield (pages.Decision, {'price': 5 * t})
                    strategies[int(self.player.other_average / 5) * 20 + int(self.player.price / 5)] += self.player.payoff

            elif self.case == 'mix1':
                if self.player.id_in_group == 1 or self.player.id_in_group == 3:
                    # NBR player
                    if self.round_number == 1:
                        yield (pages.Decision, {'price': 30})
                    else:
                        last_time = self.player.in_round(self.round_number - 1)
                        # Naive best response function
                        new_price = A/(2*(D+B/N)) + ((D+B/N)-B)/(D+B/N) * last_time.other_average + self.player.cost / 2
                        yield (pages.Decision, {'price': new_price})
                elif self.player.id_in_group == 2 or self.player.id_in_group == 4:
                    # Collusive player
                    best_price = A / (2 * B) + self.player.cost / 2
                    yield (pages.Decision, {'price': best_price})
            elif self.case == 'mix2':
                if self.player.id_in_group == 1:
                    # NBR player
                    if self.round_number == 1:
                        yield (pages.Decision, {'price': 30})
                    else:
                        last_time = self.player.in_round(self.round_number - 1)
                        other_average = (last_time.group.average_price * C.players_per_group - last_time.price) / \
                                        (C.players_per_group - 1)
                        # Naive best response function
                        new_price = A/(2*(D+B/N)) + ((D+B/N)-B)/(D+B/N) * last_time.other_average + self.player.cost / 2
                        yield (pages.Decision, {'price': new_price})
                elif self.player.id_in_group == 2:
                    # Collusive player
                    best_price = C.max_quantity / 2 / C.elasticity + self.player.cost / 2
                    yield (pages.Decision, {'price': best_price})
                else:
                    # CUC players
                    if self.round_number == 1:
                        yield (pages.Decision, {'price': self.player.cost + random.randint(0, 100)})
                    else:
                        last_time = self.player.in_round(self.round_number - 1)
                        min_price = min(p.price for p in last_time.group.get_players())
                        yield (pages.Decision, {'price': max(min_price - 1, self.player.cost + 1)})
            elif self.case == 'mix3':
                if self.player.id_in_group == 1 or self.player.id_in_group == 2:
                    # NBR player
                    if self.round_number == 1:
                        yield (pages.Decision, {'price': 30})
                    else:
                        last_time = self.player.in_round(self.round_number - 1)
                        other_average = (last_time.group.average_price * C.players_per_group - last_time.price) / \
                                        (C.players_per_group - 1)
                        # Naive best response function
                        new_price = A/(2*(D+B/N)) + ((D+B/N)-B)/(D+B/N) * last_time.other_average + self.player.cost / 2
                        yield (pages.Decision, {'price': new_price})
                else:
                    # CUC players
                    if self.round_number == 1:
                        yield (pages.Decision, {'price': self.player.cost + random.randint(0, 100)})
                    else:
                        last_time = self.player.in_round(self.round_number - 1)
                        min_price = min(p.price for p in last_time.group.get_players())
                        yield (pages.Decision, {'price': max(min_price - 1, self.player.cost + 1)})

            yield (pages.Results)

            # if self.round_number == self.session.vars['num_rounds']:
            #     yield(pages.FinalOutcome)
