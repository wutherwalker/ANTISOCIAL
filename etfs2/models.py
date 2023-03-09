from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c 
)

import random
import decimal
doc = """
ETF: Duffy, Rabanal, Rud
by JP Rabanal
"""

def call_market(market_bids,market_asks):
    qstar = 0 
    price = 0 
    
    # sort the lists of variables
    market_bids_sorted = list(sorted(market_bids,reverse=True))
    market_asks_sorted = list(sorted(market_asks))
    i = 0
    
    while market_bids_sorted[i]>=market_asks_sorted[i]:
        qstar = i + 1 
        i += 1
        if i==len(market_bids_sorted) or i==len(market_asks_sorted): #note we break the loop if we are at the end of the list
            break
    
    #Compute market prices. we extend lists just in case we are at the end of the lists...     
    market_asks_sorted.extend([10000])
    market_bids_sorted.extend([-10])
    price = (min(market_asks_sorted[i],market_bids_sorted[i-1])+max(market_bids_sorted[i],market_asks_sorted[i-1]))/2
   
    return qstar, price


class Constants(BaseConstants):
    name_in_url = 'etfs2'
    players_per_group = 9
    rounds_per_market = 15
    num_markets = 2
    num_rounds = int(rounds_per_market*num_markets)
    show_up_fee = 7.00

class Subsession(BaseSubsession):
    
    ronda = models.IntegerField()
    
    
    def creating_session(self):
        if self.round_number > Constants.rounds_per_market:
            self.ronda = self.round_number - Constants.rounds_per_market
        else:
            self.ronda = self.round_number
        
        if self.round_number == 1: 
            self.session.vars['round_to_pay'] = random.randint(0,1) if Constants.num_markets>1 else 0 
        
        if self.round_number ==1 or self.round_number == int(Constants.rounds_per_market+1):
            
            for tipos in [0,1,2]:
                for p in self.get_players():
                    if p.id_in_group >= tipos*3+1 and p.id_in_group <= tipos*3+3:
                        p.cash = decimal.Decimal(self.session.config["cash"][tipos])
                        p.n_a = self.session.config["na"][tipos]
                        p.n_b = self.session.config["nb"][tipos]
                        p.n_c = self.session.config["nc"][tipos]
                    p.t_a = 0 
                    p.t_b = 0 
                    p.t_c = 0 
        
class Group(BaseGroup):
    nav_a = models.DecimalField(max_digits=5, decimal_places=2)
    nav_b = models.DecimalField(max_digits=5, decimal_places=2)
    nav = models.DecimalField(max_digits=5, decimal_places=2)
    p_a = models.DecimalField(max_digits=5, decimal_places=2)
    q_a = models.IntegerField()
    d_a = models.IntegerField()

    p_b = models.DecimalField(max_digits=5, decimal_places=2)
    q_b = models.IntegerField()
    d_b = models.IntegerField()

    p_c = models.DecimalField(max_digits=5, decimal_places=2)
    q_c = models.IntegerField()
    d_c = models.IntegerField()
    
    def update_values(self):
        players = self.get_players()
        
        for p in players:
            pasado =  p.in_previous_rounds()[-1]
            p.n_a = pasado.n_a + pasado.t_a
            p.n_b = pasado.n_b + pasado.t_b
            p.n_c = pasado.n_c + pasado.t_c
            p.cash = pasado.cash + pasado.delta_cash
            p.t_a = 0 
            p.t_b = 0 
            p.t_c = 0
    
    
    def clearing_market_a(self):
        self.q_a = 0
        self.p_a = 0
    
        #Create lists of variables: asks and bids per unit with their player id
        market_bids = []
        market_bids_random = []
        market_asks = []
        market_asks_random = []
        list_buyers = []
        list_sellers= []
        
        players = self.get_players()
        
        for p in players:
            if p.nbida>0:
                market_bids.extend([p.bida]*p.nbida)
                market_bids_random.extend([decimal.Decimal(p.bida)+decimal.Decimal(random.random()/100000.0)]*p.nbida)
                list_buyers.extend([p]*p.nbida)
                
            if p.naska>0:
                market_asks.extend([p.aska]*p.naska)
                market_asks_random.extend([decimal.Decimal(p.aska)+decimal.Decimal(random.random()/100000.0)]*p.naska)
                list_sellers.extend([p]*p.naska)

        if max(market_bids or [-10])>=min(market_asks or [10000000]):
            self.q_a, self.p_a = call_market(market_bids,market_asks)                
            
            buyers_sorted = sorted(zip(market_bids_random,list_buyers),reverse=True)
            (market_bids_sorted,list_buyers_sorted) = zip(*buyers_sorted)
            final_list_buyers = list(list_buyers_sorted)[:(self.q_a)]

            sellers_sorted = sorted(zip(market_asks_random,list_sellers))
            (market_asks_sorted,list_sellers_sorted) = zip(*sellers_sorted)
            final_list_sellers =  list(list_sellers_sorted)[:(self.q_a)]

            for p in final_list_buyers:
                p.t_a +=1 
            
            for p in final_list_sellers:
                p.t_a -=1 
        
    def clearing_market_b(self):
        self.q_b = 0
        self.p_b = 0
    
         #Create lists of variables: asks and bids per unit with their player id
        market_bids = []
        market_bids_random = []
        market_asks = []
        market_asks_random = []
        list_buyers = []
        list_sellers= []
        
        players = self.get_players()
        
        for p in players:
            if p.nbidb>0:
                market_bids.extend([p.bidb]*p.nbidb)
                market_bids_random.extend([decimal.Decimal(p.bidb)+decimal.Decimal(random.random()/100000.0)]*p.nbidb)
                list_buyers.extend([p]*p.nbidb)
                
            if p.naskb>0:
                market_asks.extend([p.askb]*p.naskb)
                market_asks_random.extend([decimal.Decimal(p.askb)+decimal.Decimal(random.random()/100000.0)]*p.naskb)
                list_sellers.extend([p]*p.naskb)

        if max(market_bids or [-10])>=min(market_asks or [10000000]):
            self.q_b, self.p_b = call_market(market_bids,market_asks)                
            
            buyers_sorted = sorted(zip(market_bids_random,list_buyers),reverse=True)
            (market_bids_sorted,list_buyers_sorted) = zip(*buyers_sorted)
            final_list_buyers = list(list_buyers_sorted)[:(self.q_b)]

            sellers_sorted = sorted(zip(market_asks_random,list_sellers))
            (market_asks_sorted,list_sellers_sorted) = zip(*sellers_sorted)
            final_list_sellers =  list(list_sellers_sorted)[:(self.q_b)]

            for p in final_list_buyers:
                p.t_b +=1 
            
            for p in final_list_sellers:
                p.t_b -=1
                
                
    def clearing_market_c(self):
        self.q_c = 0
        self.p_c = 0
    
        #Create lists of variables: asks and bids per unit with their player id
        market_bids = []
        market_bids_random = []
        market_asks = []
        market_asks_random = []
        list_buyers = []
        list_sellers= []
        
        players = self.get_players()
        
        for p in players:
            if p.nbidc>0:
                market_bids.extend([p.bidc]*p.nbidc)
                market_bids_random.extend([decimal.Decimal(p.bidc)+decimal.Decimal(random.random()/100000.0)]*p.nbidc)
                list_buyers.extend([p]*p.nbidc)
                
            if p.naskc>0:
                market_asks.extend([p.askc]*p.naskc)
                market_asks_random.extend([decimal.Decimal(p.askc)+decimal.Decimal(random.random()/100000.0)]*p.naskc)
                list_sellers.extend([p]*p.naskc)

        if max(market_bids or [-10])>=min(market_asks or [10000000]):
            self.q_c, self.p_c = call_market(market_bids,market_asks)                
            
            buyers_sorted = sorted(zip(market_bids_random,list_buyers),reverse=True)
            (market_bids_sorted,list_buyers_sorted) = zip(*buyers_sorted)
            final_list_buyers = list(list_buyers_sorted)[:(self.q_c)]

            sellers_sorted = sorted(zip(market_asks_random,list_sellers))
            (market_asks_sorted,list_sellers_sorted) = zip(*sellers_sorted)
            final_list_sellers =  list(list_sellers_sorted)[:(self.q_c)]

            for p in final_list_buyers:
                p.t_c +=1 
            
            for p in final_list_sellers:
                p.t_c -=1

    def set_cumpay(self):   
        players = self.get_players()
        
        if self.subsession.round_number<= Constants.rounds_per_market:
            for p in players:
                p.cum_payoff= sum([j.pay_display for j in p.in_all_rounds()])
                p.cum_payoff_topay = sum([j.payoff for j in p.in_all_rounds()])
        else:
            for p in players: 
                p.cum_payoff= sum([j.pay_display for j in p.in_rounds(Constants.rounds_per_market+1,self.subsession.round_number)])
                p.cum_payoff_topay = sum([j.payoff for j in p.in_all_rounds()])
            
          
    def set_nav(self):

        if self.q_a>0:
            self.nav_a = self.p_a
        else: 
            self.nav_a = self.in_previous_rounds()[-1].nav_a
        
        if self.q_b>0:
            self.nav_b = self.p_b
        else: 
            self.nav_b = self.in_previous_rounds()[-1].nav_b
        
class Player(BasePlayer):
    
    cash = models.DecimalField(max_digits=8, decimal_places=2, label="")
    delta_cash = models.DecimalField(max_digits=8, decimal_places=2)
    
    n_a = models.IntegerField(widget=widgets.NumberInput,min=0)
    t_a = models.IntegerField()
    bida = models.DecimalField(max_digits=8, decimal_places=2, label="",min=0)
    nbida = models.IntegerField(min=0, label="")
    naska = models.IntegerField(min=0, label="")
    aska = models.DecimalField(max_digits=8, decimal_places=2, label="", min=0,)
    di_a = models.DecimalField(max_digits=8, decimal_places=2)
    
    n_b = models.IntegerField(widget=widgets.NumberInput,min=0)
    t_b = models.IntegerField()
    bidb = models.DecimalField(max_digits=8, decimal_places=2, label="",min=0)
    nbidb = models.IntegerField(min=0, label="")
    naskb = models.IntegerField(min=0, label="")
    askb = models.DecimalField(max_digits=8, decimal_places=2, label="", min=0,)
    di_b = models.DecimalField(max_digits=8, decimal_places=2) 
    
    n_c = models.IntegerField(widget=widgets.NumberInput,min=0)
    t_c = models.IntegerField()
    bidc = models.DecimalField(max_digits=8, decimal_places=2, label="",min=0)
    nbidc = models.IntegerField(min=0, label="")
    naskc = models.IntegerField(min=0, label="")
    askc = models.DecimalField(max_digits=8, decimal_places=2, label="", min=0,)
    di_c = models.DecimalField(max_digits=8, decimal_places=2)    
    
    cum_payoff = models.CurrencyField(
        null=True,
        doc="cum payoff"
        )
        
    cum_payoff_topay= models.CurrencyField(
        null=True,
        doc="cum real payoff"
        )

    pay_display = models.CurrencyField(
        null=True,
        doc="current payoff"
        )
    
    