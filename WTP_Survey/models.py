from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Patrick Julius'

## KNOWN ISSUES ##
# Real-time calculations are not displayed properly
# Sequence ending logic is faulty
# It's possible to massively underconsume and end up with huge negative payoffs

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'WTP_Survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # These questions are for everyone
    age = models.IntegerField(
        label="What is your age?",
    )
    gender = models.StringField(
        label="What is your gender?",
        choices=["Male", "Female", "Other"],
        widget=widgets.RadioSelectHorizontal,
    )
    major = models.StringField(
        label="What is your academic major?",
    )
    student = models.StringField(
        choices=["Undergraduate", "Graduate", "Other"],
    )
    year = models.IntegerField(
        label="What year are you in your program?",
    )
    past_studies = models.BooleanField(
        label="Have you participated in economics or psychology studies previously?",
    )
    race = models.StringField(
        label="What is your race?",
        choices=["White", "Black", "Asian", "Hispanic", "Mixed", "Other"]
    )
    charity = models.IntegerField(
        label="How much have you donated to charity in the past 12 months? $"
    )
    volunteer = models.IntegerField(
        label="How many hours of volunteer work have you done in the past 12 months?"
    )
    paintings_Klee = models.IntegerField(
        label="On a scale from 0 (not at all) to 10 (completely), " + \
              "please rate how familiar you were with the paintings made by " + \
              "Klee, before this experiment.",
        min=0,
        max=10,
    )
    paintings_Kandinsky = models.IntegerField(
        label="On a scale from 0 (not at all) to 10 (completely), " + \
              "please rate how familiar you were with the paintings made by " + \
              "Kandinsky, before this experiment.",
        min=0,
        max=10,
    )

    #These are specific to the group prime
    artist = models.StringField(
        label="Which group were you assigned to?",
        choices=["Klee", "Kandinsky"],
    )
    group_mug = models.BooleanField(
        label="Did you choose your group mug to bid on?",
    )
    bought_mug = models.BooleanField(
        label="Did you purchase the mug you big on?",
    )
    group_help = models.IntegerField(
        label="On a scale from 0 (not at all) to 10 (completely), " + \
              "please rate how much you think " + \
              "communicating with your group members helped in the painting " + \
              "matching task.",
        min=0,
        max=10,
    )
    group_identity = models.IntegerField(
        label="On a scale from 0 (not at all) to 10 (completely), " + \
              "please rate how attached you felt to your group.",
        min=0,
        max=10,
    )

    # Rate how much you agree from 0 (completely unimportant) to 10 (top priority).
    why_bought_identity = models.IntegerField(
        label="I wanted to show my affiliation with the group.",
        min=0,
        max=10,
    )
    why_bought_ostracism = models.IntegerField(
        label="I wanted to avoid being punished in later tasks.",
        min=0,
        max=10,
    )
    why_bought_reward = models.IntegerField(
        label="I wanted to get rewarded in later tasks.",
        min=0,
        max=10,
    )
    why_bought_preference = models.IntegerField(
        label="How much I liked the mug and wanted to have it.",
        min=0,
        max=10,
    )
    why_bought_different = models.IntegerField(
        label="Some other motivation (explain below):",
        min=0,
        max=10,
    )
    why_bought_explain = models.LongStringField(
        label="Other motivation: ",
        blank=True,
    )

    dictator_self = models.IntegerField(
        label="I wanted to earn as much money as possible for myself.",
        min=0,
        max=10,
    )
    dictator_other = models.IntegerField(
        label="I wanted to earn as much money as possible for the other player.",
        min=0,
        max=10,
    )
    dictator_fair = models.IntegerField(
        label="I wanted to make a fair split between myself and the other player.",
        min=0,
        max=10,
    )
    dictator_envy = models.IntegerField(
        label="I wanted to earn more than the other player.",
        min=0,
        max=10,
    )
    dictator_group_mug = models.IntegerField(
        label="I wanted to reward those who bought their group mug, " + \
              "regardless of which group they were in.",
        min=0,
        max=10,
    )
    dictator_own_group = models.IntegerField(
        label="I wanted to reward those in my own group, " + \
              "regardless of whether they bought the group mug.",
        min=0,
        max=10,
    )
    dictator_own_group_mug = models.IntegerField(
        label="I wanted to reward those in my own group who bought the group mug. ",
        min=0,
        max=10,
    )
    dictator_different = models.IntegerField(
        label="Some other motivation (explain below):",
        min=0,
        max=10,
    )
    dictator_explain = models.LongStringField(
        label="Other motivation: ",
        blank=True,
    )

    sender_self = models.IntegerField(
        label="I wanted to earn as much money as possible for myself.",
        min=0,
        max=10,
    )
    sender_other = models.IntegerField(
        label="I wanted to earn as much money as possible for the other player.",
        min=0,
        max=10,
    )
    sender_fair = models.IntegerField(
        label="I wanted to make a fair split between myself and the other player.",
        min=0,
        max=10,
    )
    sender_envy = models.IntegerField(
        label="I wanted to earn more than the other player.",
        min=0,
        max=10,
    )
    sender_group_mug = models.IntegerField(
        label="I wanted to reward those who bought their group mug, " + \
              "regardless of which group they were in.",
        min=0,
        max=10,
    )
    sender_own_group = models.IntegerField(
        label="I wanted to reward those in my own group, " + \
              "regardless of whether they bought the group mug.",
        min=0,
        max=10,
    )
    sender_own_group_mug = models.IntegerField(
        label="I wanted to reward those in my own group who bought the group mug. ",
        min=0,
        max=10,
    )
    sender_different = models.IntegerField(
        label="Some other motivation (explain below):",
        min=0,
        max=10,
    )
    sender_explain = models.LongStringField(
        label="Other motivation: ",
        blank=True,
    )

    general_loyal = models.IntegerField(
        label="I was more likely to be nice to another player " + \
              "who bought my group's mug if they were in my group.",
        min=-10,
        max=10,
    )
    general_traitor = models.IntegerField(
        label="I was more likely to be nice to another player who didn't " + \
              "buy my group's mug if they were in my group.",
        min=-10,
        max=10,
    )
    general_other_loyal = models.IntegerField(
        label="I was more likely to be nice to another player " + \
              "who bought my group's mug if they were not in my group.",
        min=-10,
        max=10,
    )
    general_other_traitor = models.IntegerField(
        label="I was more likely to be nice to another player who didn't " + \
              "buy my group's mug if they were not in my group.",
        min=-10,
        max=10,
    )

