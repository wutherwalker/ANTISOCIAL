from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.Survey, {'age': 31, 'gender': 'Male', 'race': 'Mixed',
                              'major': 'Economics', 'student': 'Graduate', 'year': 3,
                              'past_studies': True, 'charity': 1961, 'volunteer': 10,
                              'artist': 'Klee', 'bought_mug': False,
                              'group_help': 4, 'group_identity': 3,
                              'paintings_Klee': 5, 'paintings_Kandinsky': 6})
        if self.player.session.config['WTP_task']:
            yield (pages.MotivationWTP, {'why_bought_identity': 0, 'why_bought_ostracism': 3,
                                         'why_bought_reward': 3, 'why_bought_preference': 10,
                                         'why_bought_different': 0})
        if self.player.session.config['dictator_game']:
            yield (pages.MotivationDictator, {'dictator_self': 5, 'dictator_other': 3,
                                              'dictator_fair': 10, 'dictator_envy': 5,
                                              'dictator_group_mug': 0, 'dictator_own_group': 2,
                                              'dictator_own_group_mug': 0,
                                              'dictator_different': 0})
        if self.player.session.config['trust_game']:
            yield (pages.MotivationSender, {'sender_self': 5, 'sender_other': 3,
                                            'sender_fair': 10, 'sender_envy': 5,
                                            'sender_group_mug': 0, 'sender_own_group': 2,
                                            'sender_own_group_mug': 0,
                                            'sender_different': 0})
        if self.player.session.config['dictator_game'] or self.player.session.config['trust_game']:
            yield (pages.MotivationGeneral, {'general_loyal': 0, 'general_traitor': 0,
                                             'general_other_loyal': 0, 'general_other_traitor': 0})
