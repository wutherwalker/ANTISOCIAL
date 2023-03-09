from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Patrick Julius'

doc = """
Nonlinear Public Goods Game using Taxation

This app implements a nonlinear public goods game with an interior dominant strategy equilbrium by using a progressive
tax with deductible contributions. 
"""


class Constants(BaseConstants):
    name_in_url = 'Julius_Taxation'
    players_per_group = 5
    # For testing purposes
    # num_rounds = 4
    # For the actual experiment
    num_rounds = 40
    endowment_poor = 10.00
    endowment_equal = 15.00
    endowment_rich = 20.00
    MPCR_nonprofit = 0.30
    MPCR_government = 0.50
    # tax rate is linear in adjusted gross income;
    # tax_maximum is the income at which tax rate goes to 100%
    tax_maximum = 20.00
    endowment_charity = 10.00


class Subsession(BaseSubsession):
    condition = models.BooleanField()

    def creating_session(self):
        self.group_randomly()

        if self.round_number == 1:
            self.session.vars['paying_round'] = random.randint(1, Constants.num_rounds)

        for p in self.get_players():
            if self.round_number <= Constants.num_rounds/2:
                p.revenue_return = self.session.config['first_revenue_condition']
                if (self.round_number <= Constants.num_rounds/4 and self.session.config['first_inequality_condition'])\
                        or (self.round_number > Constants.num_rounds/4 and not self.session.config['first_inequality_condition']):
                    if p.id_in_group <= 2:
                        p.role = 2
                        p.gross_income = Constants.endowment_rich
                    else:
                        p.role = 0
                        p.gross_income = Constants.endowment_poor
                else:
                    p.role = 1
                    p.gross_income = Constants.endowment_equal
            else:
                p.revenue_return = not self.session.config['first_revenue_condition']
                if (self.round_number <= 3*Constants.num_rounds/4 and self.session.config['first_inequality_condition'])\
                        or (self.round_number > 3*Constants.num_rounds/4 and not self.session.config['first_inequality_condition']):
                    if p.id_in_group <= 2:
                        p.role = 2
                        p.gross_income = Constants.endowment_rich
                    else:
                        p.role = 0
                        p.gross_income = Constants.endowment_poor
                else:
                    p.role = 1
                    p.gross_income = Constants.endowment_equal


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    total_revenue = models.CurrencyField()

    def set_payoffs(self):
        total_contribution = 0
        total_revenue = 0

        for p in self.get_players():
            p.taxable_income = p.gross_income - p.contribution
            p.tax_paid = p.taxable_income**2/Constants.tax_maximum
            total_contribution += p.contribution
            total_revenue += p.tax_paid
            p.after_tax_income = p.taxable_income - p.tax_paid
            if p.revenue_return:
                p.payoff_maximizer = int(Constants.tax_maximum/2 * (1-Constants.MPCR_nonprofit)/(1-Constants.MPCR_government))
                p.payoff_max = p.payoff_maximizer - p.payoff_maximizer**2 / Constants.tax_maximum + \
                               (p.gross_income - p.payoff_maximizer) * Constants.MPCR_nonprofit + \
                               (p.payoff_maximizer**2 / Constants.tax_maximum) * Constants.MPCR_government
            else:
                p.payoff_maximizer = int(Constants.tax_maximum/2 * (1-Constants.MPCR_nonprofit))
                p.payoff_max = p.payoff_maximizer - p.payoff_maximizer**2 / Constants.tax_maximum + \
                               (p.gross_income - p.payoff_maximizer) * Constants.MPCR_nonprofit

            # Correction for corner solution
            if p.payoff_maximizer > p.gross_income:
                p.payoff_maximizer = p.gross_income
                if p.revenue_return:
                    p.payoff_max = p.gross_income - (1-Constants.MPCR_government)*p.gross_income**2/Constants.tax_maximum
                else:
                    p.payoff_max = p.gross_income - p.gross_income**2/Constants.tax_maximum

        for p in self.get_players():
            p.contribution_share = Constants.MPCR_nonprofit * total_contribution
            if p.revenue_return:
                p.revenue_share = Constants.MPCR_government * total_revenue
                p.payoff_net = p.after_tax_income + p.contribution * Constants.MPCR_nonprofit + p.tax_paid * Constants.MPCR_government
            else:
                p.revenue_share = 0
                p.payoff_net = p.after_tax_income + p.contribution * Constants.MPCR_nonprofit

            p.payoff = p.after_tax_income + p.contribution_share + p.revenue_share


            p.payoff_sacrifice = p.payoff_max - p.payoff_net

            if p.revenue_return:
                p.payoff_benefit = (p.tax_paid - p.payoff_maximizer**2 / Constants.tax_maximum) * \
                                   Constants.MPCR_government * (Constants.players_per_group - 1) + \
                                   (p.contribution - (p.gross_income - p.payoff_maximizer)) * \
                                   Constants.MPCR_nonprofit * (Constants.players_per_group - 1)
            else:
                p.payoff_benefit = (p.contribution - (p.gross_income - p.payoff_maximizer)) * \
                                   Constants.MPCR_nonprofit * (Constants.players_per_group - 1)
            if p.payoff_benefit != 0:
                p.altruism = p.payoff_sacrifice / p.payoff_benefit
            else:
                p.altruism = 0


class Player(BasePlayer):
    gross_income = models.CurrencyField(min=0, max=40, default=30)
    contribution = models.CurrencyField(
        default=30,
        min=0,
        max=40,
        widget=widgets.Slider()
    )
    taxable_income = models.CurrencyField(default=0)
    tax_paid = models.CurrencyField(default=0)
    after_tax_income = models.CurrencyField(default=0)
    contribution_share = models.CurrencyField(default=15)
    revenue_share = models.CurrencyField(default=0)
    revenue_return = models.BooleanField()
    game_role = models.IntegerField(default=1)
    # 0 = poor, 1 = equal, 2 = rich
    payoff_max = models.CurrencyField(default=0)
    payoff_maximizer = models.CurrencyField(default=0)
    payoff_sacrifice = models.CurrencyField(default=0)
    payoff_benefit = models.CurrencyField(default=0)
    payoff_net = models.CurrencyField(default=0)
    # oTree says this shouldn't be a FloatField, but it's wrong; currency divided by currency is unitless float!
    altruism = models.CurrencyField(default=0)
    contribution_initial = models.CurrencyField(default=0)

    charity = models.StringField(
        choices=['Amnesty International', 'UNICEF', 'Medecins Sans Frontieres', 'the American Cancer Society'],
        blank=True,
    )

    donation = models.CurrencyField(
        default=0,
        min=0,
        max=5,
        widget=widgets.Slider()
    )

    # Demographics for questionnaire
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
        widget=widgets.RadioSelect,
        blank=True,
    )

    major = models.StringField(
        # choices=['Aerospace Engineering', 'African American Studies', 'Anthropology', 'Applied Physics',
        #          'Art', 'Art History', 'Asian American Studies', 'Biochemistry and Molecular Biology',
        #          'Biological Sciences', 'Biology / Education', 'Biomedical Engineering', 'Business Adminstration',
        #          'Business Economics', 'Business Information Management', 'Chemical Engineering', 'Chemistry',
        #          'Chicano / Latino studies', 'Chinese Studies', 'Civil Engineering', 'Classics', 'Cognitive Science',
        #          'Comparative Literature', 'Computer Engineering', 'Computer Game Science', 'Computer Science',
        #          'Computer Science and Engineering', 'Criminology, Law and Society', 'Dance', 'Data Science',
        #          'Developmental and Cell Biology', 'Drama', 'Earth System Science', 'East Asian Cultures',
        #          'Ecology and Evolutionary Biology', 'Economics', 'Education Sciences', 'Electrical Engineering',
        #          'Engineering', 'English', 'Environmental Engineering', 'Environmental Science',
        #          'European Studies', 'Exercise Sciences', 'Film and Media Studies', 'French', 'Gender and Sexuality',
        #          'Genetics', 'German Studies', 'Global Cultures', 'Global Middle East Studies', 'History',
        #          'Human Biology', 'Informatics', 'International Studies', 'Japanese Language and Literature',
        #          'Korean Literature and Culture', 'Literary Journalism', 'Materials Science Engineering',
        #          'Mathematics', 'Mechanical Engineering', 'Microbiology and Immunology', 'Music', 'Neurobiology',
        #          'Nursing Science', 'Pharmaceutical Sciences', 'Philosophy', 'Physics', 'Political Science',
        #          'Psychology', 'Psychology and Social Behavior', 'Public Health', 'Quantitative Economics',
        #          'Religious Studies', 'Social Ecology', 'Social Policy and Public Service', 'Sociology',
        #          'Software Engineering', 'Spanish', 'Urban Studies', 'Undeclared', 'Major not listed'],
        # doc="""Player's choice from list of UCI majors""",
        # widget=widgets.Select,
        blank=True,
    )

    explanation = models.StringField(
        doc="""Player's explanation of their choices""",
        widget=widgets.TextInput,
        blank=True,
    )

    def get_average_payoff(self):
        total = self.payoff
        for p in self.get_others_in_group():
            total += p.payoff
        return total/Constants.players_per_group

    def get_average_tax_paid(self):
        total = self.tax_paid
        for p in self.get_others_in_group():
            total += p.tax_paid
        return total/Constants.players_per_group

    def get_average_contribution(self):
        return self.contribution_share / Constants.MPCR_nonprofit / Constants.players_per_group


