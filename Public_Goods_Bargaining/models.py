import random, math, itertools

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Jason Ralston and Patrick Julius'

doc = """
A game where two players bargain sequentially over 100 points split between their account, the other's account and 
the public account.
"""

rollfive = [1, 2, 3, 4]


class Constants(BaseConstants):
    # The number of rounds will be governed by how many rounds will be determined to be played for a supergame.
    # a, b, and c are the lengths of the super games which should be determined by a negative binomial distribution

    ShowUpPayment = 7

    a = 3
    b = 8
    d = 6
    e = 5
    f = 1
    g = 10
    h = 3
    i = 3
    j = 0

    # a = 1
    # b = 2
    # d = 2
    # e = 3
    # f = 1
    # g = 2
    # h = 2
    # i = 1
    # j = 0

    sevenrandomdraws = random.sample(range(1, 9), 8)
    supergame1 = sevenrandomdraws.index(2) + 1
    supergame2 = sevenrandomdraws.index(3) + 1

    # Probability that a proposer stays proposer and responder stays responder
    ProbSwitch = 0.6

    # Multipliers for the payoff functions
    HMultiplier = 55
    LMultiplier = 25

    name_in_url = 'Public_Goods_Bargaining'
    players_per_group = 2
    num_rounds = a + b + d + e + f + g + h + i + j

    endowment = 100


class Subsession(BaseSubsession):
    randomchoice = models.IntegerField()

    # Every round there is a chance that the proposer/responder roles switch within a group
    def before_session_starts(self):
        self.randomchoice = random.randint(1, 4)

        if self.round_number == 1:
            self.group_randomly()
            for group in self.get_groups():
                for p in group.get_players():
                    if p.id_in_group == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number <= Constants.a:
            self.group_like_round(1)
            for group in self.get_groups():
                for p in group.get_players():
                    if p.in_round(1).HighLow == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number == Constants.a + 1:
            self.group_randomly()
            for group in self.get_groups():
                for p in group.get_players():
                    if p.id_in_group == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number <= Constants.a + Constants.b:
            self.group_like_round(Constants.a + 1)
            for group in self.get_groups():
                for p in group.get_players():
                    if p.in_round(Constants.a + 1).HighLow == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number == Constants.a + Constants.b + 1:
            self.group_randomly()
            for group in self.get_groups():
                for p in group.get_players():
                    if p.id_in_group == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number <= Constants.a + Constants.b + Constants.d:
            self.group_like_round(Constants.a + Constants.b + 1)
            for group in self.get_groups():
                for p in group.get_players():
                    if p.in_round(Constants.a + Constants.b + 1).HighLow == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number == Constants.a + Constants.b + Constants.d + 1:
            self.group_randomly()
            for group in self.get_groups():
                for p in group.get_players():
                    if p.id_in_group == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number <= Constants.a + Constants.b + Constants.d + Constants.e:
            self.group_like_round(Constants.a + Constants.b + Constants.d + 1)
            for group in self.get_groups():
                for p in group.get_players():
                    if p.in_round(Constants.a + Constants.b + Constants.d + 1).HighLow == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number == Constants.a + Constants.b + Constants.d + Constants.e + 1 :
            self.group_randomly()
            for group in self.get_groups():
                for p in group.get_players():
                    if p.id_in_group == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f:
            self.group_like_round(Constants.a + Constants.b + Constants.d + Constants.e + 1)
            for group in self.get_groups():
                for p in group.get_players():
                    if p.in_round(Constants.a + Constants.b + Constants.d + Constants.e + 1).HighLow == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + 1:
            self.group_randomly()
            for group in self.get_groups():
                for p in group.get_players():
                    if p.id_in_group == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g:
            self.group_like_round(Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + 1)
            for group in self.get_groups():
                for p in group.get_players():
                    if p.in_round(Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + 1).HighLow == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + 1 :
            self.group_randomly()
            for group in self.get_groups():
                for p in group.get_players():
                    if p.id_in_group == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h:
            self.group_like_round(Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + 1)
            for group in self.get_groups():
                for p in group.get_players():
                    if p.in_round(Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + 1).HighLow == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + 1:
            self.group_randomly()
            for group in self.get_groups():
                for p in group.get_players():
                    if p.id_in_group == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i:
            self.group_like_round(Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + 1)
            for group in self.get_groups():
                for p in group.get_players():
                    if p.in_round(Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + 1).HighLow == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        elif self.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i + 1:
            self.group_randomly()
            for group in self.get_groups():
                for p in group.get_players():
                    if p.id_in_group == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2
        else:
            self.group_like_round(Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i + 1)
            for group in self.get_groups():
                for p in group.get_players():
                    if p.in_round(Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i + 1).HighLow == 1:
                        p.HighLow = 1
                    else:
                        p.HighLow = 2

        for g in self.get_groups():
            if random.random() < Constants.ProbSwitch:
                players = g.get_players()
                players.reverse()
                g.set_players(players)

        if self.round_number == 1:
            sevenrandomdraws = random.sample(range(1, 9), 8)
            supergame1 = sevenrandomdraws.index(2) + 1
            supergame2 = sevenrandomdraws.index(3) + 1
            self.session.vars['supergame1'] = supergame1
            self.session.vars['supergame2'] = supergame2


class Group(BaseGroup):

    High_Account_offered = models.CurrencyField(min=0,max=99)
    Low_Account_offered = models.CurrencyField(min=0,max=99)
    Group_Account_offered = models.CurrencyField(min=1)

    Group_Account_floor = models.CurrencyField(initial=1)

    offer_accepted = models.BooleanField()

    def set_new_floor(self):
        p1, p2 = self.get_players()
        if self.session.config['mandatory_treatment']:
            if not (self.subsession.round_number == 1 or self.subsession.round_number == Constants.a + 1 or self.subsession.round_number == Constants.a + Constants.b + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + 1 or self.subsession.round_number == Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + 1):
                if self.in_round(self.subsession.round_number - 1).offer_accepted:
                    self.Group_Account_floor = self.in_round(self.subsession.round_number - 1).Group_Account_offered
                    p1.GroupFloor = self.Group_Account_floor
                    p2.GroupFloor = self.Group_Account_floor
                else:
                    self.Group_Account_floor = self.in_round(self.subsession.round_number - 1).Group_Account_floor
                    p1.GroupFloor = self.Group_Account_floor
                    p2.GroupFloor = self.Group_Account_floor
        else:
            self.Group_Account_floor = 1

    def set_payoffs(self):
        p1, p2 = self.get_players()

        if self.offer_accepted:
            if p1.HighLow == 1:
                p1.payoff = self.High_Account_offered + Constants.HMultiplier*math.log(self.Group_Account_offered)
                p1.YourOffer = self.High_Account_offered
                p1.TheirOffer = self.Low_Account_offered
                p1.GroupOffer = self.Group_Account_offered
                p2.payoff = self.Low_Account_offered + Constants.LMultiplier*math.log(self.Group_Account_offered)
                p2.YourOffer = self.Low_Account_offered
                p2.TheirOffer = self.High_Account_offered
                p2.GroupOffer = self.Group_Account_offered
            else:
                p1.payoff = self.Low_Account_offered + Constants.LMultiplier*math.log(self.Group_Account_offered)
                p1.YourOffer = self.Low_Account_offered
                p1.TheirOffer = self.High_Account_offered
                p1.GroupOffer = self.Group_Account_offered
                p2.payoff = self.High_Account_offered + Constants.HMultiplier*math.log(self.Group_Account_offered)
                p2.YourOffer = self.High_Account_offered
                p2.TheirOffer = self.Low_Account_offered
                p2.GroupOffer = self.Group_Account_offered
            p1.OfferDecision = "Accept"
            p2.OfferDecision = "Accept"
        else:
            if p1.HighLow == 1:
                p1.YourOffer = self.High_Account_offered
                p1.TheirOffer = self.Low_Account_offered
                p1.GroupOffer = self.Group_Account_offered
                p2.YourOffer = self.Low_Account_offered
                p2.TheirOffer = self.High_Account_offered
                p2.GroupOffer = self.Group_Account_offered
                p1.payoff = Constants.HMultiplier * math.log(self.Group_Account_floor)
                p2.payoff = Constants.LMultiplier * math.log(self.Group_Account_floor)
            else:
                p1.YourOffer = self.Low_Account_offered
                p1.TheirOffer = self.High_Account_offered
                p1.GroupOffer = self.Group_Account_offered
                p2.YourOffer = self.High_Account_offered
                p2.TheirOffer = self.Low_Account_offered
                p2.TheirOffer = self.Low_Account_offered
                p2.GroupOffer = self.Group_Account_offered
                p1.payoff = Constants.LMultiplier * math.log(self.Group_Account_floor)
                p2.payoff = Constants.HMultiplier * math.log(self.Group_Account_floor)
            p1.OfferDecision = "Reject"
            p2.OfferDecision = "Reject"


class Player(BasePlayer):

    fiftyfifty = models.CurrencyField()
    sendreceiver = models.IntegerField()

    TheirOffer = models.CurrencyField()
    YourOffer = models.CurrencyField()
    GroupOffer = models.CurrencyField()
    OfferDecision = models.CharField()

    HighLow = models.IntegerField()

    yourrole = models.CharField()
    theirrole = models.CharField()
    yourtype = models.CharField()

    bigpayoff = models.CurrencyField()

    totalpayoff = models.CurrencyField()

    Sequence = models.IntegerField()

    def set_roles(self):
        if self.id_in_group == 1:
            self.yourrole = "Proposer"
            self.theirrole = "Receiver"
        else:
            self.yourrole = "Receiver"
            self.theirrole = "Proposer"
        if self.HighLow == 1:
            self.yourtype = "High"
        else:
            self.yourtype = "Low"

    def set_supergame_payoffs(self):
        self.participant.vars['payoff' + str(self.Sequence)] = self.payoff

        if self.session.vars['supergame1'] == self.Sequence:
            self.participant.vars['supergame1_payoff'] = self.payoff
        elif self.session.vars['supergame2'] == self.Sequence:
            self.participant.vars['supergame2_payoff'] = self.payoff

        if self.Sequence > max(self.session.vars['supergame2'], self.session.vars['supergame2']):
            self.bigpayoff = self.session.config['real_world_currency_per_point']*self.participant.vars['supergame1_payoff'] + self.participant.vars['supergame2_payoff']
            self.totalpayoff = self.bigpayoff + 7

    def SetSequence(self):
        if self.subsession.round_number <= Constants.a:
            self.Sequence = 1
        elif self.subsession.round_number <= Constants.a + Constants.b:
            self.Sequence = 2
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d:
            self.Sequence = 3
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d + Constants.e:
            self.Sequence = 4
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f:
            self.Sequence = 5
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g:
            self.Sequence = 6
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h:
            self.Sequence = 7
        elif self.subsession.round_number <= Constants.a + Constants.b + Constants.d + Constants.e + Constants.f + Constants.g + Constants.h + Constants.i:
            self.Sequence = 8
        else:
            self.Sequence = 9

    GroupFloor = models.CurrencyField(min=1, initial=1)



