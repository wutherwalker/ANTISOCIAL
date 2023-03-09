from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instructions1(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'object_type': self.session.config['object_type'],
            'endowment': c(self.session.config['max_price']),
            'conversion_value': c(1).to_real_world_currency(self.session),
            'real': self.participant.vars['fake_rounds_done'],
            'fake_rounds': self.session.config['fake_rounds'],
        }


class Instructions2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        example_bid = c(int(self.session.config['max_price']/2))
        return {
            'object_1': 'Mug A',
            'object_2': 'Mug B',
            'fake_rounds': self.session.config['fake_rounds'],
            'example_bid': example_bid,
            'high_price': example_bid+5,
            'low_price': example_bid-5,
            'real': self.participant.vars['fake_rounds_done'],
        }


class GroupMug(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['fake_rounds_done'] and self.session.config['assign_groups']

    def vars_for_template(self):
        Klee_size = int(self.session.config['Klee_group_proportion']*self.session.num_participants)
        Kandinsky_size = self.session.num_participants - Klee_size
        Klee = self.participant.vars['artist'] == "Klee"
        return {
            'artist': "Klee" if Klee else "Kandinsky",
            'other_artist': "Kandinsky" if Klee else "Klee",
            'own_group_size': Klee_size if Klee else Kandinsky_size,
            'other_group_size': Kandinsky_size if Klee else Klee_size,
            'games': self.session.config['dictator_game'] or self.session.config['trust_game'],
            'round_number': self.round_number,
            'group_object': "Mug A" if Klee else "Mug B",
            'group_proportion_known': self.session.config['group_proportion'] is not None,
            'group_proportion': self.session.config['group_proportion'],
        }


class Bid(Page):
    def is_displayed(self):
        fake_round = self.round_number <= self.session.config['fake_rounds'] and not self.participant.vars['fake_rounds_done']
        real_round = self.round_number == 1 and self.participant.vars['fake_rounds_done']
        return fake_round or real_round

    form_model = 'player'
    form_fields = ['object_choice', 'bid']

    def bid_max(self):
        return self.session.config['max_price']

    def vars_for_template(self):
        group_prime = self.participant.vars['fake_rounds_done']
        assign_groups = self.session.config['assign_groups']
        if assign_groups:
            Klee_size = int(self.session.config['Klee_group_proportion']*self.session.num_participants)
            Kandinsky_size = self.session.num_participants - Klee_size
        else:
            Klee_size = self.session.num_participants
            Kandinsky_size = 0

        if group_prime:
            artist = self.participant.vars['artist']
            Klee = artist == "Klee"
        else:
            artist = None
            Klee = False

        return {
            'object_A': 'WTP/GroupMug_Klee.png' if group_prime else 'WTP/Mug_White.png',
            'object_B': 'WTP/GroupMug_Kandinsky.png' if group_prime else 'WTP/Mug_Black.png',
            'group_prime': group_prime,
            'assign_groups': assign_groups,
            'artist': artist,
            'own_group_size': Klee_size if Klee else Kandinsky_size,
            'other_group_size': Kandinsky_size if Klee else Klee_size,
            'round_number': self.round_number,
            'group_object': "Mug A" if Klee else "Mug B",
            'real': self.participant.vars['fake_rounds_done'],
            'group_proportion_known': self.session.config['group_proportion'] is not None,
            'group_proportion': self.session.config['group_proportion'],
        }


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        fake_round = self.round_number <= self.session.config['fake_rounds']
        real_round = self.round_number == 1
        return fake_round or real_round

    def after_all_players_arrive(self):
        if self.round_number == self.session.config['fake_rounds']:
            for group in self.subsession.get_groups():
                for player in group.get_players():
                    player.participant.vars['fake_rounds_done'] = True
                    

class Auction(Page):
    def is_displayed(self):
        fake_round = self.round_number <= self.session.config['fake_rounds'] and not self.participant.vars['fake_rounds_done']
        real_round = self.round_number == 1 and self.participant.vars['fake_rounds_done']
        return fake_round or real_round

    def vars_for_template(self):
        price = self.subsession.price
        purchased = self.subsession.price <= self.player.bid
        endowment = self.session.config['max_price']
        payoff = endowment - price if purchased else endowment
        real = self.participant.vars['fake_rounds_done']


        player = self.player
        player.payoff = payoff if real else 0
        player.price = price

        if real:
            self.participant.vars['WTP_payoff'] = self.player.payoff

        if purchased:
            player.participant.vars['item_purchased'] = player.object_choice
        else:
            player.participant.vars['item_purchased'] = None

        return {
            'round_number': self.round_number,
            'object_choice': self.player.object_choice,
            'bid': self.player.bid,
            'price': price,
            'purchased': purchased,
            'money_left': c(payoff),
            'real_money': c(payoff).to_real_world_currency(self.session),
            'real': real,
        }

page_sequence = [
    Instructions1,
    Instructions2,
    GroupMug,
    Bid,
    Auction,
    ResultsWaitPage,
    # Results,
]
