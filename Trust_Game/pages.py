from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class GroupAssignment(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        if self.round_number == 1:
            if self.session.config['assign_groups']:
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

                # Assumes equal number of senders and receivers
                for i in range(0, len(Klee_senders)):
                    new_group = [Klee_senders[i], Klee_receivers[i]]
                    group_matrix.append(new_group)

                for i in range(0, len(Kandinsky_senders)):
                    new_group = [Kandinsky_senders[i], Kandinsky_receivers[i]]
                    group_matrix.append(new_group)

                # group_matrix.append(send_home)
            else:
                players = self.subsession.get_players()
                group_size = int(self.session.num_participants/2)
                senders = players[0:group_size]
                receivers = players[group_size:2*group_size]

                for player in players:
                    player.assigned_group = True
                    if player in senders:
                        player.sender = True
                    else:
                        player.sender = False

                group_matrix = []
                send_home = []
                for i in range(0, len(senders)):
                    new_group = [senders[i], receivers[i]]
                    group_matrix.append(new_group)

                # group_matrix.append(send_home)

            # Only do the group matrix once
            print(group_matrix)

            self.subsession.set_group_matrix(group_matrix)
            for group in self.subsession.get_groups():
                print("Group: " + str(group.id_in_subsession))
                for player in group.get_players():
                    print("Player: " + str(player) + ", Group: " + str(player.group.id_in_subsession) +
                          ", Klee: " + str(player.Klee) + ", Sender: " + str(player.sender))

        else:
            senders = []
            receivers = []
            for player in self.subsession.get_players():
                player.assigned_group = player.in_round(self.round_number-1).assigned_group
                player.sender = player.in_round(self.round_number-1).sender
                if player.sender:
                    senders.append(player)
                else:
                    receivers.append(player)
                player.Klee = player.in_round(self.round_number-1).Klee
                player.participant.vars['trust_role'] = player.role()


            # Assign sender-receiver pairs
            # Later rounds: Keep role the same, otherwise group randomly
            # But we need to exclude the send_home group
            # self.subsession.group_like_round(self.round_number-1)
            # groups = self.subsession.get_groups()
            # for i in range(0, len(groups)-1):
            #     for player in groups[i].get_players():
            #         if player.sender:
            #             senders.append(player)
            #         else:
            #             receivers.append(player)
                # senders.append(groups[i].get_player_by_role("sender"))
                # receivers.append(groups[i].get_player_by_role("receiver"))

            print("Senders and Receivers:")
            print(senders)
            print(receivers)
            random.shuffle(senders)
            random.shuffle(receivers)

            group_matrix = []
            send_home = []
            for player in self.subsession.get_players():
                if not player.assigned_group:
                    send_home.append(player)

            for i in range(0, len(senders)):
                new_group = [senders[i], receivers[i]]
                print("New group:")
                print(new_group)
                group_matrix.append(new_group)

            # group_matrix.append(send_home)
            print("Group Matrix:")
            print(group_matrix)
            # Only do the group matrix once
            # if self.subsession.get_groups()[0] == self.group:
            self.subsession.set_group_matrix(group_matrix)


class Instructions1(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'assign_groups': self.session.config['assign_groups'],
            'artist': self.participant.vars['artist'],
            'num_rounds': Constants.num_rounds,
        }


class Instructions2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'assign_groups': self.session.config['assign_groups'],
            'artist': self.player.participant.vars['artist'],
        }


class Instructions3(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'assign_groups': self.session.config['assign_groups'],
            'artist': self.player.participant.vars['artist'],
            'endowment': self.session.config['endowment'],
            'multiplier': self.session.config['multiplier'],
        }


class DecisionSender(Page):
    form_model = 'player'
    form_fields = ['amount_sent']

    def amount_sent_max(self):
        self.player.endowment = self.session.config['endowment']
        return self.player.endowment

    def is_displayed(self):
        return self.player.sender

    def vars_for_template(self):
        self.player.endowment = self.session.config['endowment']
        self.player.partner_Klee = self.player.get_partner().Klee

        if self.session.config['WTP_task']:
            item_purchased = self.player.get_partner().participant.vars['item_purchased']
            self.player.purchased = self.participant.vars['item_purchased']
        else:
            self.player.purchased = None
            item_purchased = None

        self.player.partner_purchased = item_purchased

        return {
            'round': self.round_number,
            'num_rounds': Constants.num_rounds,
            'assign_groups': self.session.config['assign_groups'],
            'WTP_task': self.session.config['WTP_task'],
            'artist': self.player.participant.vars['artist'],
            'other_artist': self.player.get_partner().participant.vars['artist'],
            'other_item_purchased': item_purchased,
            'object_group': 'Klee' if item_purchased == "Mug A" else "Kandinsky",
            'other_purchased_something': item_purchased is not None,
            'endowment': c(self.player.endowment),
        }


class DecisionWait(WaitPage):
    def is_displayed(self):
        return True

    def after_all_players_arrive(self):
        for player in self.group.get_players():
            if not player.sender:
                player.endowment = player.get_partner().amount_sent * self.session.config['multiplier']


class DecisionReceiver(Page):
    form_model = 'player'
    form_fields = ['amount_sent']

    def amount_sent_max(self):
        return self.player.endowment

    def is_displayed(self):
        return not self.player.sender

    def vars_for_template(self):
        partner = self.player.get_partner()
        if self.session.config['WTP_task']:
            item_purchased = partner.participant.vars['item_purchased']
        else:
            item_purchased = None
        endowment = self.player.endowment
        self.player.partner_Klee = partner.Klee

        if self.session.config['WTP_task']:
            self.player.purchased = self.participant.vars['item_purchased']
            self.player.partner_purchased = partner.participant.vars['item_purchased']
        else:
            self.player.purchased = None
            self.player.partner_purchased = None

        multiplier = self.session.config['multiplier']
        return {
            'no_endowment': self.player.endowment == 0,
            'round': self.round_number,
            'num_rounds': Constants.num_rounds,
            'assign_groups': self.session.config['assign_groups'],
            'WTP_task': self.session.config['WTP_task'],
            'artist': self.player.participant.vars['artist'],
            'other_artist': self.player.get_partner().participant.vars['artist'],
            'other_item_purchased':  item_purchased,
            'object_group': 'Klee' if item_purchased == "Mug A" else "Kandinsky",
            'other_purchased_something': item_purchased is not None,
            'amount_sent': c(endowment/multiplier),
            'multiplier': multiplier,
            'endowment': c(endowment),
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


# This page is only here to assign payoffs; can I do that earlier?
class Results(Page):
    def is_displayed(self):
        return True

    def vars_for_template(self):
        self.player.payoff = self.player.endowment - self.player.amount_sent

        if self.round_number == self.session.vars['trust_paying_round']:
            self.participant.vars['trust_payoff'] = self.player.payoff

        return {
        }


page_sequence = [
    GroupAssignment,
    Instructions1,
    Instructions2,
    Instructions3,
    DecisionSender,
    DecisionWait,
    DecisionReceiver,
    Results
]
