from ._builtin import Page, WaitPage
from otree.api import Currency as c
from .models import Constants

import random
import decimal


class Updating(WaitPage):
    def vars_for_template(self):
        if self.round_number == 1:
            self.participant.vars['bret_payoff'] = self.participant.payoff
            return {}

    def after_all_players_arrive(self):
        
        if self.subsession.round_number==1 or self.subsession.round_number==int(Constants.rounds_per_market+1): 
            pass
        else:
            self.group.update_values()
        
        for g in self.subsession.get_groups():
            g.d_a = random.sample(self.session.config['dividend_a'],1)[0]
            otro_div = random.sample(self.session.config['dividend_a'],1)[0]

            if 1<=self.subsession.round_number<8 or Constants.rounds_per_market+1<=self.subsession.round_number<Constants.rounds_per_market+8 :
                g.d_b = (self.session.config['rho'])*g.d_a + (1+self.session.config['rho'])*otro_div
            else: 
                g.d_b = self.session.config['divb']+ (self.session.config['rho'])*g.d_a + (1+self.session.config['rho'])*otro_div
            
            g.d_c = g.d_a + g.d_b
        
        
class Market(Page):
    
    
    form_model = 'player'
    form_fields = ['nbida','bida','naska','aska','nbidb','bidb','naskb','askb','nbidc','bidc','naskc','askc']
    
    
    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        
        return {
                'nassets_a': self.player.n_a, 
                'nassets_b': self.player.n_b,
                'nassets_c': self.player.n_c,
                'temp_A': range(self.subsession.round_number-1, 0,-1) if self.subsession.round_number<=Constants.rounds_per_market else range(self.subsession.round_number-1, Constants.rounds_per_market,-1),
                'player_in_all_rounds': player_in_all_rounds,
                'current_round': self.subsession.round_number,
                'previous_ta':  '-'  if self.subsession.round_number==1 or self.subsession.round_number==int(Constants.rounds_per_market+1)  else self.player.in_previous_rounds()[-1].t_a,
                'previous_tb': '-'  if self.subsession.round_number==1 or self.subsession.round_number==int(Constants.rounds_per_market+1)  else self.player.in_previous_rounds()[-1].t_b,
                'previous_tc': '-'  if self.subsession.round_number==1 or self.subsession.round_number==int(Constants.rounds_per_market+1)  else self.player.in_previous_rounds()[-1].t_c,
                'previous_deltacash': '-'  if self.subsession.round_number==1 or self.subsession.round_number==int(Constants.rounds_per_market+1)  else self.player.in_previous_rounds()[-1].delta_cash,
                'previous_profit': '-'  if self.subsession.round_number==1 or self.subsession.round_number==int(Constants.rounds_per_market+1)  else self.player.in_previous_rounds()[-1].pay_display,
                'previous_cumprofit': '-'  if self.subsession.round_number==1 or self.subsession.round_number==int(Constants.rounds_per_market+1) else self.player.in_previous_rounds()[-1].cum_payoff,
                'ta' : self.player.t_a+self.player.n_a,
                'tb' : self.player.t_b+self.player.n_b,
                'tc' : self.player.t_c+self.player.n_c,
                'diva': self.session.config['dividend_a'][1],
                'divb': self.session.config['divb'],
                'pfinala': self.session.config['pfinal'][0],
                'pfinalc': self.session.config['pfinal'][2],
                'rho': self.session.config['rho'],

        }
        
    def naska_error_message(self, value):
        print('values is', value)
        if value > self.player.n_a:
            return 'You cannot sell more assets than what you hold of A'
    
    def naskb_error_message(self, value):
        print('values is', value)
        if value > self.player.n_b:
            return 'You cannot sell more assets than what you hold of B'
    
    def naskc_error_message(self, value):
        print('values is', value)
        if value > self.player.n_c:
            return 'You cannot sell more assets than what you hold of C'
    
    def error_message(self, values):
        print('values is', values)
        if values["bida"]*values["nbida"]+values["bidb"]*values["nbidb"]+values["bidc"]*values["nbidc"] > self.player.cash:
            return 'Your purchase is over the budget'
    

    
class Clearing(WaitPage):
    
    def after_all_players_arrive(self):

        self.group.clearing_market_a()
        self.group.clearing_market_b()
        self.group.clearing_market_c()
        
        players = self.group.get_players()
        
        for p in players: 
            p.delta_cash = decimal.Decimal(-1*p.group.p_a*p.t_a-1*p.group.p_b*p.t_b-1*p.group.p_c*p.t_c)
            p.di_a = p.group.d_a*(p.n_a + p.t_a)
            p.di_b = p.group.d_b*(p.n_b + p.t_b)
            p.di_c = p.group.d_c*(p.n_c + p.t_c)
            
            p.pay_display= p.di_a + p.di_b + p.di_c 
        
            if self.subsession.round_number==Constants.num_rounds or self.subsession.round_number==Constants.rounds_per_market:
                p.pay_display +=  (p.n_a + p.t_a)*self.session.config['pfinal'][0] +(p.n_b + p.t_b)*self.session.config['pfinal'][1] + (p.n_c + p.t_c)*self.session.config['pfinal'][2] + p.cash + p.delta_cash
            
            if self.subsession.round_number > int(Constants.rounds_per_market*self.session.vars['round_to_pay']) and self.subsession.round_number <= Constants.rounds_per_market+int(Constants.rounds_per_market*self.session.vars['round_to_pay']):
                p.payoff = p.pay_display    
            else: 
                p.payoff = c(0)

        self.group.set_cumpay()
        
        if self.subsession.round_number==1 or self.subsession.round_number == int(Constants.rounds_per_market+1):
            self.group.nav_a = self.group.p_a
            self.group.nav_b = self.group.p_b
        else:
            self.group.set_nav()
        
        self.group.nav = self.group.nav_a+self.group.nav_b

class CasiAdios(Page):
    
    def is_displayed(self):
        return self.round_number == Constants.num_rounds or self.round_number == Constants.rounds_per_market
        
            
    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        
        return {
                'nassets_afinal': self.player.n_a+self.player.t_a, 
                'nassets_bfinal': self.player.n_b+self.player.t_b,
                'nassets_cfinal': self.player.n_c+self.player.t_c,
                'temp_A': range(self.subsession.round_number, 0,-1) if self.subsession.round_number<=Constants.rounds_per_market else range(self.subsession.round_number, Constants.rounds_per_market,-1),
                'player_in_all_rounds': player_in_all_rounds,
                'current_round': self.subsession.round_number,
                'cash_final': self.player.cash + self.player.delta_cash,
                'ta' : self.player.t_a+self.player.n_a,
                'tb' : self.player.t_b+self.player.n_b,
                'tc' : self.player.t_c+self.player.n_c,
        }
        
        
        
class PrimerAdios(Page):

    def is_displayed(self):
        return self.round_number == Constants.rounds_per_market or self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        
        return {
                'nassets_afinal': self.player.n_a+self.player.t_a, 
                'nassets_bfinal': self.player.n_b+self.player.t_b,
                'nassets_cfinal': self.player.n_c+self.player.t_c,
                'diva': self.player.di_a, 
                'divb': self.player.di_b,
                'divc': self.player.di_c,
                'cash_final': self.player.cash + self.player.delta_cash,
                'points_final': self.player.cum_payoff,
                'pfinala': self.session.config['pfinal'][0],
                'pfinalc': self.session.config['pfinal'][2],
        }        
    

class Adios(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds 
        
    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()
        
        return{
                'points_final': self.player.cum_payoff_topay,
                'market': self.session.vars['round_to_pay']+1,
                'bret_payoff': self.participant.vars['bret_payoff'],
                'show_up_fee': Constants.show_up_fee,
                'total_payoff': self.player.cum_payoff_topay + self.participant.vars['bret_payoff'],
                'points_indollars':  round(self.player.cum_payoff_topay*self.session.config['real_world_currency_per_point'],2),
        }
                

                
                
page_sequence = [
    Updating,
    Market,
    Clearing,
    CasiAdios,
    PrimerAdios,
    Adios,
    ]
    