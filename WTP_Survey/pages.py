from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Survey(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'race', 'major', 'year', 'student',
                   'past_studies', 'charity', 'volunteer',
                   'artist', 'bought_mug',
                   'group_help', 'group_identity',
                   'paintings_Klee', 'paintings_Kandinsky']


class MotivationWTP(Page):
    def is_displayed(self):
        return self.session.config['WTP_task']

    form_model = 'player'
    form_fields = ['why_bought_identity', 'why_bought_ostracism',
                   'why_bought_reward', 'why_bought_preference',
                   'why_bought_different', 'why_bought_explain']


class MotivationDictator(Page):
    def is_displayed(self):
        return self.session.config['dictator_game']

    form_model = 'player'
    form_fields = ['dictator_self', 'dictator_other', 'dictator_fair', 'dictator_envy',
                   'dictator_group_mug', 'dictator_own_group', 'dictator_own_group_mug',
                   'dictator_different', 'dictator_explain']


class MotivationSender(Page):
    def is_displayed(self):
        return self.session.config['trust_game']

    form_model = 'player'
    form_fields = ['sender_self', 'sender_other', 'sender_fair', 'sender_envy',
                   'sender_group_mug', 'sender_own_group', 'sender_own_group_mug',
                   'sender_different', 'sender_explain']


class MotivationGeneral(Page):
    def is_displayed(self):
        return self.session.config['assign_groups']  and (self.session.config['dictator_game'] or self.session.config['trust_game'])

    form_model = 'player'
    form_fields = ['general_loyal', 'general_traitor',
                   'general_other_loyal', 'general_other_traitor']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


page_sequence = [
    Survey,
    MotivationWTP,
    MotivationDictator,
    MotivationSender,
    MotivationGeneral,
    ResultsWaitPage,
]
