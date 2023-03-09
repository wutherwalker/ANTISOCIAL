from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


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
        self.subsession.set_group_matrix([Klee_group, Kandinsky_group, send_home])


class WaitBeforeChat(WaitPage):
    pass

class ChatPage(Page):
    def is_displayed(self):
        return self.player.assigned_group

    def get_timeout_seconds(self):
        return self.session.config['chat_time']*60

    def vars_for_template(self):
        return {
            'artist': "Klee" if self.player.Klee else "Kandinsky",
            'chat_time': self.session.config['chat_time'],
            # Not sure which paintings to use here; should this be randomized? Session config? By group?
            'painting_1_path': "Klee_Kandinsky/Klee_6.png",
            'painting_2_path': "Klee_Kandinsky/Kandinsky_6.png",
            'num_paintings': 5,
            'answer_value': c(self.session.config['answer_value']),
            'participation_fee': self.session.config['participation_fee'],
            'username': ("Klee" if self.player.Klee else "Kandinsky") + "Fan" + str(self.player.id_in_group),
        }


class Answers(Page):
    form_model = 'player'
    form_fields = ['painting_1', 'painting_2']

    def is_displayed(self):
        return self.player.assigned_group

    def vars_for_template(self):
        return {
            'artist': "Klee" if self.player.Klee else "Kandinsky",
            'chat_time': self.session.config['chat_time'],
            # Not sure which paintings to use here; should this be randomized? Session config? By group?
            'painting_1_path': "Klee_Kandinsky/Klee_6.png",
            'painting_2_path': "Klee_Kandinsky/Kandinsky_6.png",
            'num_paintings': 5,
            'answer_value': c(self.session.config['answer_value']),
            'participation_fee': self.session.config['participation_fee'],
            'username': ("Klee" if self.player.Klee else "Kandinsky") + "Fan" + str(self.player.id_in_group),
        }


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True


class Results(Page):
    def is_displayed(self):
        return self.player.assigned_group

    def vars_for_template(self):
        self.player.score = 0
        # These depend on what the correct answers are
        if self.player.painting_1 == "Klee":
            self.player.score += 1

        if self.player.painting_2 == "Kandinsky":
            self.player.score += 1

        self.player.payoff = self.session.config['answer_value']*self.player.score
        self.participant.vars['matching_money'] = self.player.payoff
        # print("Klee_Kandinsky_discussion, matching money: " + str(self.participant.vars['matching_money']))

        return {
            'score': self.player.score,
            'payoff': self.player.payoff,
        }


page_sequence = [
    GroupAssignment,
    WaitBeforeChat,
    ChatPage,
    Answers,
    ResultsWaitPage,
    Results,
]
