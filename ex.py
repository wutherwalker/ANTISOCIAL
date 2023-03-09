#models
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    num_videos = 5
    payoff = 200
    players_per_group = None
    name_in_url = 'rating'
    num_rounds = 1

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    video_1_evaluation = models.PositiveIntegerField(choices=range(1, 11))
    video_2_evaluation = models.PositiveIntegerField(choices=range(1, 11))
    video_3_evaluation = models.PositiveIntegerField(choices=range(1, 11))
    video_4_evaluation = models.PositiveIntegerField(choices=range(1, 11))
    video_5_evaluation = models.PositiveIntegerField(choices=range(1, 11))

#pages
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Introduction(Page):
    pass

class VideoEvaluation(Page):
    form_model = 'player'
    form_fields = ['video_1_evaluation', 'video_2_evaluation', 'video_3_evaluation', 'video_4_evaluation', 'video_5_evaluation']

    def is_displayed(self):
        return self.subsession.round_number <= Constants.num_videos

class Results(Page):
    def is_displayed(self):
        return self.subsession.round_number > Constants.num_videos

    def vars_for_template(self):
        return {'payoff': Constants.payoff}

page_sequence = [
    Introduction,
    VideoEvaluation,
    Results,
]

#videoevaluation
{% extends "global/Page.html" %}
{% load otree %}

{% block content %}
  <h1>Video {{ player.round_number }}</h1>
  <iframe width="560" height="315" src="D:\BaiduNetdiskDownload\10-13.mp4\10-13.mp4" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  <form method="post">

    <div class="form-group">
      <label class="control-label">How do you rate this video?</label>
      {% for radio in form.video_1_evaluation %}
          <div class="form-check">
              {{ radio }}
              <label class="form-check-label">{{ radio.choice_label }}</label>
          </div>
      {% endfor %}
    </div>
    <br><br>
    {% submit_button %}
  </form>
{% endblock %}
