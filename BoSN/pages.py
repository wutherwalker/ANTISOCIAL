from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Intro(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'digit_span': self.session.config['digit_span'],
            'players_per_session': self.session.num_participants,
            'num_rounds': Constants.num_rounds,
            'half_session': int(self.session.num_participants / 2),
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'duration': Constants.duration,
        }


class IntroWait(WaitPage):
    template_name = 'BoSN/IntroWait.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'digit_span': self.session.config['digit_span'],
            'players_per_session': self.session.num_participants,
            'num_rounds': Constants.num_rounds,
            'half_session': int(self.session.num_participants/ 2),
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
        }

    def after_all_players_arrive(self):
        pass


class Matching(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'players_per_session': self.session.num_participants,
            'players_per_group': Constants.players_per_group,
            'num_rounds': Constants.num_rounds,
            'half_session': int(self.session.num_participants / 2),
            'half_group': int(Constants.players_per_group / 2),
            'num_groups': self.session.vars['num_groups'],
        }


class MatchingWait(WaitPage):
    template_name = 'BoSN/MatchingWait.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'players_per_session': self.session.num_participants,
            'players_per_group': Constants.players_per_group,
            'num_rounds': Constants.num_rounds,
            'half_session': int(self.session.num_participants / 2),
            'half_group': int(Constants.players_per_group / 2),
            'num_groups': self.session.vars['num_groups'],
        }

    def after_all_players_arrive(self):
        pass


class Payoffs(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'high_payoff': Constants.high_payoff,
            'low_payoff': Constants.low_payoff,
            'double_high': Constants.high_payoff * 2,
            'double_low': Constants.low_payoff * 2,
            'triple_high': Constants.high_payoff * 3,
            'triple_low': Constants.low_payoff * 3,
            'nothing': c(0),
        }


class PayoffsWait(WaitPage):
    template_name = 'BoSN/PayoffsWait.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'high_payoff': Constants.high_payoff,
            'low_payoff': Constants.low_payoff,
            'double_high': Constants.high_payoff * 2,
            'double_low': Constants.low_payoff * 2,
            'triple_high': Constants.high_payoff * 3,
            'triple_low': Constants.low_payoff * 3,
            'nothing': c(0),
        }

    def after_all_players_arrive(self):
        pass


class Announcements(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.session.config['announce_treatment']

    def vars_for_template(self):
        return {
            'announce_X_percent': int(100 * Constants.announce_X_prob),
            'announce_Y_percent': 100 - int(100 * Constants.announce_X_prob),
            'num_rounds': Constants.num_rounds,
        }


class AnnouncementsWait(WaitPage):
    template_name = 'BoSN/AnnouncementsWait.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1 and self.session.config['announce_treatment']

    def vars_for_template(self):
        return {
            'announce_X_percent': int(100 * Constants.announce_X_prob),
            'announce_Y_percent': 100 - int(100 * Constants.announce_X_prob),
            'num_rounds': Constants.num_rounds,
        }

    def after_all_players_arrive(self):
        pass


class Summary(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'digit_span': self.session.config['digit_span'],
            'announce_treatment': self.session.config['announce_treatment'],
            'num_rounds': Constants.num_rounds,
        }


class SummaryWait(WaitPage):
    template_name = 'BoSN/SummaryWait.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'digit_span': self.session.config['digit_span'],
            'announce_treatment': self.session.config['announce_treatment'],
            'num_rounds': Constants.num_rounds,
        }

    def after_all_players_arrive(self):
        pass


class Administration(Page):
    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class AdministrationWait(WaitPage):
    template_name = 'BoSN/AdministrationWait.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class QuizQ1(Page):
    form_model = 'player'
    form_fields = ['q1']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class QuizQ2(Page):
    form_model = 'player'
    form_fields = ['q2']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class QuizQ3(Page):
    form_model = 'player'
    form_fields = ['q3']

    def is_displayed(self):
        return self.round_number == 1 and self.session.config['announce_treatment']

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class QuizQ4(Page):
    form_model = 'player'
    form_fields = ['q4a', 'q4b']

    def is_displayed(self):
        return self.round_number == 1 and self.session.config['announce_treatment']

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class QuizQ5(Page):
    form_model = 'player'
    form_fields = ['q5']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class QuizQ6(Page):
    form_model = 'player'
    form_fields = ['q6']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class QuizQ7(Page):
    form_model = 'player'
    form_fields = ['q7']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class QuizQ8(Page):
    form_model = 'player'
    form_fields = ['q8']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class QuizQ9(Page):
    form_model = 'player'
    form_fields = ['q9']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class QuizQ10(Page):
    form_model = 'player'
    form_fields = ['q10']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }


class QuizA1(Page):
    form_model = 'player'
    # form_fields = ['q1']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }

    ## Most recent oTree update removed this functionality ##
    # def inner_dispatch(self):
    #     self._is_frozen = False
    #
    # def before_next_page(self):
    #     if self.request.POST.get('back') == '1':
    #         self.player.errors += 1
    #         self._index_in_pages -= 2
    #         self.participant._index_in_pages -= 2


class QuizA2(Page):
    form_model = 'player'
    # form_fields = ['q2']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }

    # def inner_dispatch(self):
    #     self._is_frozen = False
    #
    # def before_next_page(self):
    #     if self.request.POST.get('back') == '1':
    #         self.player.errors += 1
    #         self._index_in_pages -= 2
    #         self.participant._index_in_pages -= 2


class QuizA3(Page):
    form_model = 'player'
    # form_fields = ['q3']

    def is_displayed(self):
        return self.round_number == 1 and self.session.config['announce_treatment']

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }

    # def inner_dispatch(self):
    #     self._is_frozen = False
    #
    # def before_next_page(self):
    #     if self.request.POST.get('back') == '1':
    #         self.player.errors += 1
    #         self._index_in_pages -= 2
    #         self.participant._index_in_pages -= 2


class QuizA4(Page):
    form_model = 'player'
    # form_fields = ['q4a', 'q4b']

    def is_displayed(self):
        return self.round_number == 1 and self.session.config['announce_treatment']

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }

    # def inner_dispatch(self):
    #     self._is_frozen = False
    #
    # def before_next_page(self):
    #     if self.request.POST.get('back') == '1':
    #         self.player.errors += 1
    #         self._index_in_pages -= 2
    #         self.participant._index_in_pages -= 2


class QuizA5(Page):
    form_model = 'player'
    # form_fields = ['q5']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }

    # def inner_dispatch(self):
    #     self._is_frozen = False
    #
    # def before_next_page(self):
    #     if self.request.POST.get('back') == '1':
    #         self.player.errors += 1
    #         self._index_in_pages -= 2
    #         self.participant._index_in_pages -= 2


class QuizA6(Page):
    form_model = 'player'
    # form_fields = ['q6']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }

    # def inner_dispatch(self):
    #     self._is_frozen = False
    #
    # def before_next_page(self):
    #     if self.request.POST.get('back') == '1':
    #         self.player.errors += 1
    #         self._index_in_pages -= 2
    #         self.participant._index_in_pages -= 2


class QuizA7(Page):
    form_model = 'player'
    # form_fields = ['q7']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }

    # def inner_dispatch(self):
    #     self._is_frozen = False
    #
    # def before_next_page(self):
    #     if self.request.POST.get('back') == '1':
    #         self.player.errors += 1
    #         self._index_in_pages -= 2
    #         self.participant._index_in_pages -= 2


class QuizA8(Page):
    form_model = 'player'
    # form_fields = ['q8']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }

    # def inner_dispatch(self):
    #     self._is_frozen = False
    #
    # def before_next_page(self):
    #     if self.request.POST.get('back') == '1':
    #         self.player.errors += 1
    #         self._index_in_pages -= 2
    #         self.participant._index_in_pages -= 2


class QuizA9(Page):
    form_model = 'player'
    # form_fields = ['q9']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }

    # def inner_dispatch(self):
    #     self._is_frozen = False
    #
    # def before_next_page(self):
    #     if self.request.POST.get('back') == '1':
    #         self.player.errors += 1
    #         self._index_in_pages -= 2
    #         self.participant._index_in_pages -= 2


class QuizA10(Page):
    form_model = 'player'
    # form_fields = ['q10']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'exchange_rate': c(1).to_real_world_currency(self.session),
        }

    # def inner_dispatch(self):
    #     self._is_frozen = False
    #
    # def before_next_page(self):
    #     if self.request.POST.get('back') == '1':
    #         self.player.errors += 1
    #         self._index_in_pages -= 2
    #         self.participant._index_in_pages -= 2


class QuizWait(WaitPage):
    template_name = 'BoSN/QuizWait.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    def after_all_players_arrive(self):
        pass


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    def is_displayed(self):
        return True

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'player_class': self.player.player_class,
            'high_payoff': Constants.high_payoff,
            'low_payoff': Constants.low_payoff,
            'announce_treatment': self.session.config['announce_treatment'],
            'announcement': self.subsession.announcement,
            'player_in_previous_rounds': self.player.in_previous_rounds(),
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def is_displayed(self):
        return True

    def vars_for_template(self):
        digit_span = self.session.config['digit_span']
        if digit_span > 0:
            if self.player.memory_number == self.subsession.memory_number:
                correct = True
            else:
                correct = False
                self.player.payoff = 0
        else:
            correct = True

        return {
            'digit_span': digit_span,
            'correct': correct,
            'round_number': self.round_number,
            'player_class': self.player.player_class,
            'high_payoff': Constants.high_payoff,
            'low_payoff': Constants.low_payoff,
            'announce_treatment': self.session.config['announce_treatment'],
            'announcement': self.subsession.announcement,
            'player_in_previous_rounds': self.player.in_previous_rounds(),
            'payoff': self.player.payoff,
            'decision': self.player.decision,
            'others_X': self.player.others_X,
            'others_Y': self.player.others_Y,
        }


class MemoryTaskBegin(Page):
    def is_displayed(self):
        return self.session.config['digit_span'] > 0

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'memory_number': self.subsession.memory_number,
        }


class MemoryTaskEnd(Page):
    form_model = 'player'
    form_fields = ['memory_number']

    def is_displayed(self):
        return self.session.config['digit_span'] > 0

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
        }


class FinalOutcome(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        # It seems slightly kludgy to put this here, but it works
        self.participant.payoff = self.player.in_round(self.session.vars['paying_round_1']).payoff +\
                                  self.player.in_round(self.session.vars['paying_round_2']).payoff
        return {
            'player_in_all_rounds': self.player.in_all_rounds(),
            'paying_round_1': self.session.vars['paying_round_1'],
            'paying_round_2': self.session.vars['paying_round_2'],
            'round_1_payoff': self.player.in_round(self.session.vars['paying_round_1']).payoff,
            'round_1_value': c(self.player.in_round(self.session.vars['paying_round_1']).payoff).to_real_world_currency(self.session),
            'round_2_payoff': self.player.in_round(self.session.vars['paying_round_2']).payoff,
            'round_2_value': c(self.player.in_round(self.session.vars['paying_round_2']).payoff).to_real_world_currency(self.session),
            'show_up_fee': c(self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'total_payoff': c(self.participant.payoff + self.session.vars['participation_fee']).to_real_world_currency(self.session),
            'announce_treatment': self.session.config['announce_treatment'],
        }


page_sequence = [
    Intro,
    IntroWait,
    Matching,
    MatchingWait,
    Payoffs,
    PayoffsWait,
    Announcements,
    AnnouncementsWait,
    Summary,
    SummaryWait,
    Administration,
    AdministrationWait,
    QuizQ1,
    QuizA1,
    QuizQ2,
    QuizA2,
    QuizQ3,
    QuizA3,
    QuizQ4,
    QuizA4,
    QuizQ5,
    QuizA5,
    QuizQ6,
    QuizA6,
    QuizQ7,
    QuizA7,
    QuizQ8,
    QuizA8,
    QuizQ9,
    QuizA9,
    QuizQ10,
    QuizA10,
    QuizWait,
    MemoryTaskBegin,
    Decision,
    MemoryTaskEnd,
    ResultsWaitPage,
    Results,
    FinalOutcome
]
