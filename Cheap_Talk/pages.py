from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class GroupAssignment(WaitPage):
    def after_all_players_arrive(self):
        Klee_group = []
        Kandinsky_group = []
        send_home = []
        for player in self.subsession.get_players():
            if player.participant.vars['artist'] == 'Klee':
                player.assigned_group = True
                player.Klee = True
            elif player.participant.vars['artist'] == 'Kandinsky':
                player.assigned_group = True
                player.Klee = False
            else:
                player.assigned_group = False

            if player.assigned_group:
                if player.Klee:
                    Klee_group.append(player)
                else:
                    Kandinsky_group.append(player)
            else:
                send_home.append(player)

        # Assign roles
        Klee_senders_ids = random.sample(range(0, len(Klee_group)), int(len(Klee_group)/2))
        Kandinsky_senders_ids = random.sample(range(0, len(Kandinsky_group)), int(len(Kandinsky_group)/2))

        Klee_senders = []
        Kandinsky_senders = []

        for i in range(0, len(Klee_group)):
            if i in Klee_senders_ids:
                Klee_senders.append(Klee_group[i])

        for i in range(0, len(Kandinsky_group)):
            if i in Kandinsky_senders_ids:
                Kandinsky_senders.append(Kandinsky_group[i])

        for player in self.subsession.get_players():
            if player in Klee_senders or player in Kandinsky_senders:
                player.sender = True
            else:
                player.sender = False

        Klee_receivers = []
        Kandinsky_receivers = []

        for player in self.subsession.get_players():
            if player.assigned_group:
                if not player.sender:
                    if player.Klee:
                        Klee_receivers.append(player)
                    else:
                        Kandinsky_receivers.append(player)

        # print("Klee:")
        # print(Klee_senders)
        # print(len(Klee_senders))
        # print(Klee_receivers)
        # print(len(Klee_receivers))
        # print("Kandinsky:")
        # print(Kandinsky_senders)
        # print(len(Kandinsky_senders))
        # print(Kandinsky_receivers)
        # print(len(Kandinsky_receivers))

        # Assign sender-receiver pairs
        # First round: Always with an in-group member, always sender has id_in_group == 1
        group_matrix = []

        if self.round_number == 1:
            for player in self.subsession.get_players():
                player.participant.vars['part'] += 1

            # Assumes equal number of senders and receivers
            for i in range(0, len(Klee_senders)):
                new_group = [Klee_senders[i], Klee_receivers[i]]
                group_matrix.append(new_group)

            for i in range(0, len(Kandinsky_senders)):
                new_group = [Kandinsky_senders[i], Kandinsky_receivers[i]]
                group_matrix.append(new_group)

            group_matrix.append(send_home)
            # print(group_matrix)

            self.subsession.set_group_matrix(group_matrix)

        else:
            for player in self.subsession.get_players():
                player.assigned_group = player.in_round(self.round_number-1).assigned_group
                player.sender = player.in_round(self.round_number-1).sender
                player.Klee = player.in_round(self.round_number-1).Klee

            # Assign sender-receiver pairs
            # Later rounds: Keep role the same, otherwise group randomly
            # But we need to exclude the send_home group
            self.subsession.group_like_round(self.round_number-1)
            senders = []
            receivers = []
            groups = self.subsession.get_groups()
            for i in range(0, len(groups)-1):
                senders.append(groups[i].get_player_by_role("sender"))
                receivers.append(groups[i].get_player_by_role("receiver"))

            random.shuffle(senders)
            random.shuffle(receivers)

            group_matrix = []

            for i in range(0,len(senders)):
                new_group = [senders[i], receivers[i]]
                group_matrix.append(new_group)

            group_matrix.append(send_home)
            # print(group_matrix)
            self.subsession.set_group_matrix(group_matrix)

        for group in self.subsession.get_groups():
            # Make coin flips
            group.coin_heads = (random.random() < 0.5)


class Instructions1(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['artist'] != "send_home"

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'part': self.player.participant.vars['part'],
        }


class Instructions2(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['artist'] != "send_home"

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds
        }


class Instructions3(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['artist'] != "send_home"

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'win_payoff': c(self.session.config['win_payoff']),
            'lose_payoff': c(self.session.config['lose_payoff']),
        }


class Role(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['artist'] != "send_home"

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'role': self.player.role,
            'sender': self.player.sender,
        }


class ChoiceSender(Page):
    form_model = 'player'
    form_fields = ['message']

    def is_displayed(self):
        return self.player.sender

    def vars_for_template(self):
        partner = self.group.get_player_by_role("receiver")
        item_purchased = partner.participant.vars['item_purchased']
        self.player.partner_Klee = partner.Klee
        return {
            'round_number': self.round_number,
            'num_rounds': Constants.num_rounds,
            'coin_flip': "Heads" if self.group.coin_heads else "Tails",
            'own_group': "Klee" if self.player.Klee else "Kandinsky",
            'other_group': "Klee" if partner.Klee else "Kandinsky",
            'other_purchased': item_purchased is not None,
            'other_object_choice': item_purchased,
            'object_group': "Klee" if item_purchased == "Mug A" else "Kandinsky",
        }


class ChoiceReceiver(Page):
    form_model = 'player'
    form_fields = ['action']

    def is_displayed(self):
        return not self.player.sender and self.player.assigned_group

    def vars_for_template(self):
        partner = self.group.get_player_by_role("sender")
        item_purchased = partner.participant.vars['item_purchased']
        self.player.partner_Klee = partner.Klee
        self.player.message = partner.message
        return {
            'round_number': self.round_number,
            'num_rounds': Constants.num_rounds,
            'message': self.player.message,
            'own_group': "Klee" if self.player.Klee else "Kandinsky",
            'other_group': "Klee" if partner.Klee else "Kandinsky",
            'other_purchased': item_purchased is not None,
            'other_object_choice': item_purchased,
            'object_group': "Klee" if item_purchased == "Mug A" else "Kandinsky",
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    def is_displayed(self):
        return self.participant.vars['artist'] != "send_home"

    def vars_for_template(self):
        self.player.message = self.group.get_player_by_role("sender").message
        self.player.action = self.group.get_player_by_role("receiver").action
        win_payoff = self.session.config['win_payoff']
        lose_payoff = self.session.config['lose_payoff']
        coin_heads = self.group.coin_heads

        if self.player.sender:
            self.player.payoff = win_payoff if self.player.action == "H" else lose_payoff
        else:
            self.player.payoff = win_payoff if coin_heads and self.player.action == "H" or not coin_heads and self.player.action == "T" else lose_payoff

        # Don't include this round in the payoff, unless it's chosen later to be the paying round
        self.participant.payoff -= self.player.payoff
        return {
            'round_number': self.round_number,
            'sender': self.player.sender,
            'message': self.player.message,
            'coin_flip': "Heads" if coin_heads else "Tails",
            'action': self.player.action,
            'payoff': self.player.payoff,
            'real_payoff': c(self.player.payoff).to_real_world_currency(self.session),
        }


class FinalResult(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.participant.vars['artist'] != "send_home"

    def vars_for_template(self):
        paying_round = self.session.vars['paying_round']
        player = self.player.in_round(paying_round)
        matching_money = self.player.participant.vars['matching_money']
        self.participant.payoff = player.payoff + matching_money
        return {
            'paying_round': paying_round,
            'payoff': player.payoff,
            'real_payoff': c(player.payoff).to_real_world_currency(self.session),
            'matching_money': c(matching_money).to_real_world_currency(self.session),
            'total_earnings': c(player.participant.payoff).to_real_world_currency(self.session),
            'participation_fee': self.session.config['participation_fee'],
        }


page_sequence = [
    GroupAssignment,
    Instructions1,
    Instructions2,
    Instructions3,
    Role,
    ChoiceSender,
    ChoiceReceiver,
    ResultsWaitPage,
    Results,
    FinalResult,
]
