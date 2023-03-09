from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Instructions1(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'assign_groups': self.session.config['assign_groups'],
            'token_value': c(1).to_real_world_currency(self.session),
            'show_up_fee': Constants.participation_fee,
        }


class Instructions2(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'assign_groups': self.session.config['assign_groups'],
            'show_up_fee': Constants.participation_fee,
            'paintings_to_choose': Constants.num_rounds-1,
        }


class Choice(Page):
    form_model = 'player'
    form_fields = ['choice']

    def is_displayed(self):
        return self.round_number < Constants.num_rounds

    def vars_for_template(self):
        return {
            'Klee_first': self.player.Klee_first,
            'assign_groups': self.session.config['assign_groups'],
            'round_number': self.round_number,
            'Klee_painting': "Klee_Kandinsky/Klee_" + str(self.round_number) + ".png",
            'Kandinsky_painting': "Klee_Kandinsky/Kandinsky_" + str(self.round_number) + ".png",
        }


class WaitForNextPainting(Page):
    timeout_seconds = 1

    def is_displayed(self):
        return True

    def vars_for_template(self):
        # In this function because it's always run when the page loads
        # Copy the choices from previous rounds into this round
        # Necessary because a Player object only exists for a single round
        if self.round_number > 1:
            self.player.Klee_chosen = self.player.in_round(self.round_number - 1).Klee_chosen
            self.player.Kandinsky_chosen = self.player.in_round(self.round_number - 1).Kandinsky_chosen

        if self.player.Klee_first:
            if self.player.field_maybe_none('choice') == 'A':
                self.player.Klee_chosen += 1
            elif self.player.field_maybe_none('choice') == 'B':
                self.player.Kandinsky_chosen += 1
        else:
            if self.player.field_maybe_none('choice') == 'B':
                self.player.Klee_chosen += 1
            elif self.player.field_maybe_none('choice') == 'A':
                self.player.Kandinsky_chosen += 1

        return {

        }


class GroupMatching(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == Constants.num_rounds and self.session.config['assign_groups']

    def after_all_players_arrive(self):
        if self.round_number == Constants.num_rounds:
            # Sort players based on which artist they prefer
            playerlist = self.subsession.get_players()
            playerlist.sort(key=lambda x: x.Klee_chosen, reverse=True)

            group_size = int(self.session.config['Klee_group_proportion'] * self.session.num_participants)
            # group_size = 2
            # print("Group size: " + str(group_size))


            # Groups are always the same size, but some players may be assigned to
            # the artist they did not actually prefer
            Klee_group = playerlist[0:group_size]
            Kandinsky_group = playerlist[group_size:self.session.num_participants]
            self.subsession.set_group_matrix([Klee_group, Kandinsky_group])

            # Name the groups by their artist, and store that as a variable;
            # also store that as a participant variable to pass to the next app
            for group in self.subsession.get_groups():
                if group.get_players() == Klee_group:
                    group.artist = "Klee"
                    for player in group.get_players():
                        player.participant.vars['artist'] = "Klee"
                else:
                    group.artist = "Kandinsky"
                    for player in group.get_players():
                        player.participant.vars['artist'] = "Kandinsky"


class GroupResult(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'show_up_fee': Constants.participation_fee,
            'assign_groups': self.session.config['assign_groups'],
        }


page_sequence = [
    Instructions2,
    Choice,
    WaitForNextPainting,
    GroupMatching,
    GroupResult,
]
