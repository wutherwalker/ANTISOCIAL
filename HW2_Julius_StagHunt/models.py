from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Patrick Julius'

doc = """
This app implements a Stag Hunt experiment with variable payoffs, with roles arranged randomly at the start and 
indefinite iteration with a minimum of 5 rounds, maximum of 10 rounds, and continuation probability 0.45. 
"""


class Constants(BaseConstants):
    name_in_url = 'HW2_Julius_StagHunt'
    players_per_group = 2
    num_rounds = 10
    prob_continue = 0.45
    show_up_fee = 7.00
    player_assignment = random.randint(1, 2)


class Subsession(BaseSubsession):
    both_stag_payoff = models.IntegerField(initial=4)
    stag_alone_payoff = models.IntegerField(initial=0)
    h1_hare_payoff = models.IntegerField(initial=1)
    h2_hare_payoff = models.IntegerField(initial=2)
    paying_round = models.IntegerField(initial=1)

    def creating_session(self):
        if self.round_number <= 1:
            self.session.config['participation_fee'] = Constants.show_up_fee
            self.group_randomly()
        if self.round_number >= 4:
            # Change the payoff after round 3
            self.h2_hare_payoff = 3


class Group(BaseGroup):
    def set_payoffs(self):
        hunter1 = self.get_player_by_role("Hunter 1")
        hunter2 = self.get_player_by_role("Hunter 2")

        if hunter1.decision == 'A':
            # Hunter 1 chose Stag
            if hunter2.decision == 'A':
                # Hunter 2 also chose Stag
                hunter1.payoff = self.subsession.both_stag_payoff
                hunter2.payoff = self.subsession.both_stag_payoff
            elif hunter2.decision == 'B':
                # Hunter 2 chose Hare
                hunter1.payoff = self.subsession.stag_alone_payoff
                hunter2.payoff = self.subsession.h2_hare_payoff
        elif hunter1.decision == 'B':
            # Hunter 1 chose Hare
            if hunter2.decision == 'A':
                # Hunter 2 chose Stag
                hunter1.payoff = self.subsession.h1_hare_payoff
                hunter2.payoff = self.subsession.stag_alone_payoff
            elif hunter2.decision == 'B':
                # Hunter 2 also chose Hare
                hunter1.payoff = self.subsession.h1_hare_payoff
                hunter2.payoff = self.subsession.h2_hare_payoff


class Player(BasePlayer):
    decision = models.StringField(
            choices=['A', 'B'],
            doc="""This player's decision""",
            widget=widgets.RadioSelect,
            blank=True
        )

    race = models.StringField(
        choices=['White', 'Black/African American', 'Asian', 'Hispanic/Latinx', 'Native American/Pacific Islander',
                 'Two or more races', 'Other'],
        doc="""Player's self-reported race""",
        widget=widgets.RadioSelect,
        blank=True,
    )

    gender = models.StringField(
        choices=['Man', 'Woman', 'Other'],
        doc="""Player's self-reported gender""",
        widget=widgets.RadioSelect,
        blank=True
    )

    age = models.IntegerField(
        min=0,
        max=120,
        doc="""Player's self-reported age""",
        blank=True,
    )

    income = models.StringField(
        choices=['$10,000 or less', '$10,001 to $20,000', '$20,001 to $30,000', '$30,001 to $40,000',
                 '$40,001 to $50,000', '$50,001 to $60,000', '$60,001 to $70,000', '$70,001 to $80,000',
                 '$80,001 to $90,000', '$90,001 to $100,000', '$100,001 or more', 'Not sure'],
        doc="""Player's self-reported income""",
        widget=widgets.Select,
        blank=True,
    )

    major = models.StringField(
        choices=['Aerospace Engineering', 'African American Studies', 'Anthropology', 'Applied Physics',
                 'Art', 'Art History', 'Asian American Studies', 'Biochemistry and Molecular Biology',
                 'Biological Sciences', 'Biology / Education', 'Biomedical Engineering', 'Business Adiminstration',
                 'Business Economics', 'Business Information Management', 'Chemical Engineering', 'Chemistry',
                 'Chicano / Latino studies', 'Chinese Studies', 'Civil Engineering', 'Classics', 'Cognitive Science',
                 'Comparative Literature', 'Computer Engineering', 'Computer Game Science', 'Computer Science',
                 'Computer Science and Engineering', 'Criminology, Law and Society', 'Dance', 'Data Science',
                 'Developmental and Cell Biology', 'Drama', 'Earth System Science', 'East Asian Cultures',
                 'Ecology and Evolutionary Biology', 'Economics', 'Education Sciences', 'Electrical Engineering',
                 'Engineering', 'English', 'Environmental Engineering', 'Environmental Science',
                 'European Studies', 'Exercise Sciences', 'Film and Media Studies', 'French', 'Gender and Sexuality',
                 'Genetics', 'German Studies', 'Global Cultures', 'Global Middle East Studies', 'History',
                 'Human Biology', 'Informatics', 'International Studies', 'Japanese Language and Literature',
                 'Korean Literature and Culture', 'Literary Journalism', 'Materials Science Engineering',
                 'Mathematics', 'Mechanical Engineering', 'Microbiology and Immunology', 'Music', 'Neurobiology',
                 'Nursing Science', 'Pharmaceutical Sciences', 'Philosophy', 'Physics', 'Political Science',
                 'Psychology', 'Psychology and Social Behavior', 'Public Health', 'Quantitative Economics',
                 'Religious Studies', 'Social Ecology', 'Social Policy and Public Service', 'Sociology',
                 'Software Engineering', 'Spanish', 'Urban Studies', 'Undeclared', 'Major not listed'],
        doc="""Player's choice from list of UCI majors""",
        widget=widgets.Select,
        blank=True,
    )

    def role(self):
        if Constants.player_assignment == 1:
            if self.id_in_group == 1:
                return "Hunter 1"
            if self.id_in_group == 2:
                return "Hunter 2"
        elif Constants.player_assignment == 2:
            if self.id_in_group == 1:
                return "Hunter 2"
            if self.id_in_group == 2:
                return "Hunter 1"

    def get_partner(self):
        return self.get_others_in_group()[0]

