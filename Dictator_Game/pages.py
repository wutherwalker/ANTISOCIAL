from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class GroupAssignment(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):

        if self.session.config['assign_groups']:
            for player in self.subsession.get_players():
                if player.participant.vars['artist'] == 'Klee':
                    player.assigned_group = True
                    player.Klee = True
                elif player.participant.vars['artist'] == 'Kandinsky':
                    player.assigned_group = True
                    player.Klee = False
                else:
                    player.assigned_group = False

            if self.round_number == 1:
                Klee_group = []
                Kandinsky_group = []
                send_home = []

                for player in self.subsession.get_players():
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

                # Assumes equal number of senders and receivers
                for i in range(0, len(Klee_senders)):
                    new_group = [Klee_senders[i], Klee_receivers[i]]
                    group_matrix.append(new_group)

                for i in range(0, len(Kandinsky_senders)):
                    new_group = [Kandinsky_senders[i], Kandinsky_receivers[i]]
                    group_matrix.append(new_group)

                # group_matrix.append(send_home)

                print(group_matrix)
                print("Group matrix assigned")
                self.subsession.set_group_matrix(group_matrix)
            else:
                self.subsession.group_randomly()
                for group in self.subsession.get_groups():
                    group.get_player_by_id(1).sender = True
                    group.get_player_by_id(2).sender = False

                # players = self.subsession.get_players()
                # group_size = int(self.session.num_participants/2)
                # sender_ids = random.sample(range(0, 2*group_size), group_size)
                # senders = []
                # receivers = []
                # for i in range(0, 2*group_size):
                #     if i in sender_ids:
                #         players[i].sender = True
                #         senders.append(players[i])
                #     else:
                #         players[i].sender = False
                #         receivers.append(players[i])
                #
                #
                #
                # group_matrix = []
                # send_home = []
                # for i in range(0, len(senders)):
                #     new_group = [senders[i], receivers[i]]
                #     group_matrix.append(new_group)

                # group_matrix.append(send_home)

            # else:
            #     for player in self.subsession.get_players():
            #         player.assigned_group = player.in_round(self.round_number-1).assigned_group
            #         player.sender = player.in_round(self.round_number-1).sender
            #         player.Klee = player.in_round(self.round_number-1).Klee
            #
            #
            #     # Assign sender-receiver pairs
            #     # Later rounds: Group randomly
            #     self.subsession.group_like_round(self.round_number-1)
            #     senders = []
            #     receivers = []
            #     groups = self.subsession.get_groups()
            #     for i in range(0, len(groups)-1):
            #         senders.append(groups[i].get_player_by_role("sender"))
            #         receivers.append(groups[i].get_player_by_role("receiver"))
            #     random.shuffle(senders)
            #     random.shuffle(receivers)
            #
            #     group_matrix = []
            #     send_home = []
            #     for player in self.subsession.get_players():
            #         if not player.assigned_group:
            #             send_home.append(player)
            #
            #     for i in range(0, len(senders)):
            #         new_group = [senders[i], receivers[i]]
            #         group_matrix.append(new_group)
            #
            #     group_matrix.append(send_home)
            #
            #     # Only do the group matrix once
            #     if self.subsession.get_groups()[0] == self.group:
            #         self.subsession.set_group_matrix(group_matrix)


class Instructions1(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
        }


class Instructions2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds
        }


class Role(Page):
    def is_displayed(self):
        return True

    def vars_for_template(self):
        if self.session.config['WTP_task']:
            self.player.purchased = self.participant.vars['item_purchased']
        else:
            self.player.purchased = None

        return {
            'num_rounds': Constants.num_rounds,
            'role': self.player.role,
            'sender': self.player.sender,
        }


class Decision(Page):
    form_model = 'player'
    form_fields = ['allocation']

    def allocation_max(self):
        return self.player.endowment

    def is_displayed(self):
        return self.player.sender

    def vars_for_template(self):
        # partner = self.group.get_player_by_role("receiver")
        partner = self.player.get_others_in_group()[0]
        if self.session.config['WTP_task']:
            item_purchased = partner.participant.vars['item_purchased']
        else:
            item_purchased = None
        print(item_purchased)
        self.player.partner_purchased = item_purchased
        self.player.partner_Klee = partner.Klee
        return {
            'round_number': self.round_number,
            'num_rounds': Constants.num_rounds,
            'endowment': self.player.endowment,
            'assign_groups': self.session.config['assign_groups'],
            'WTP_task': self.session.config['WTP_task'],
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
        return True

    def vars_for_template(self):
        if self.player.sender:
            allocation = self.player.allocation
        else:
            allocation = self.player.get_others_in_group()[0].allocation
        # allocation = self.group.get_player_by_role("sender").allocation
        remainder = self.session.config['endowment'] - allocation

        if self.player.sender:
            self.player.payoff = remainder
        else:
            self.player.payoff = allocation

        # Hide payoffs until the end
        if self.round_number == self.session.vars['dictator_paying_round']:
            self.participant.vars['dictator_payoff'] = self.player.payoff

        return {
            'round_number': self.round_number,
        }


class FinalResult(Page):
    def is_displayed(self):
        # Payoffs are not shown until the VERY end
        return False

    def vars_for_template(self):
        paying_round = self.session.vars['dictator_paying_round']
        player = self.player.in_round(paying_round)
        matching_money = self.player.participant.vars['matching_money']
        self.participant.payoff = player.payoff + matching_money
        self.participant.vars['dictator_payoff'] = player.payoff
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
    Role,
    Decision,
    ResultsWaitPage,
    Results,
    FinalResult,
]
