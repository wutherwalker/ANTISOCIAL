from . import views
from ._builtin import Bot
from otree.api import Submission, SubmissionMustFail
import random
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        if self.subsession.round_number == Constants.a + 1 or self.subsession.round_number == Constants.a + Constants.b + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i + Constants.j + 1:
            yield Submission(views.NewSequence, check_html=False)
        if self.player.id_in_group == 1:
            yield SubmissionMustFail(views.Offer, {'High_Account_offered': 100,
                                'Low_Account_offered': 0,
                                'Group_Account_offered': 0})
            yield SubmissionMustFail(views.Offer, {'High_Account_offered': 110,
                                'Low_Account_offered': -20,
                                'Group_Account_offered': 10})
            yield SubmissionMustFail(views.Offer, {'High_Account_offered': 60,
                                'Low_Account_offered': 60,
                                'Group_Account_offered': 60})
            group_account = random.randint(1, 100)
            low_account = random.randint(0, 100-group_account)
            high_account = 100 - low_account - group_account
            yield(views.Offer, {'High_Account_offered': high_account,
                                'Low_Account_offered': low_account,
                                'Group_Account_offered': group_account})
        else:
            acceptance = random.random() < 0.75
            yield(views.Accept, {'offer_accepted': acceptance})
        yield (views.Results)
        if self.subsession.round_number == Constants.a or self.subsession.round_number == Constants.a + Constants.b or self.subsession.round_number == Constants.a + Constants.b + Constants.d or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.j:
            yield(views.SupergameResults)
