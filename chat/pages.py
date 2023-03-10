from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from django.shortcuts import render


class Index(Page):
    pass

class MyPage(Page):
    pass

class Room(Page):
    pass

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
