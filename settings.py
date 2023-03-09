import os
import dj_database_url
import django_heroku
from dotenv import load_dotenv

from os import environ



# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

mturk_hit_settings = {
    'keywords': ['bonus', 'study'],
    'title': 'Short decision-making task',
    'description': 'Complete a short decision-making task as part of an experiment for the University of California, Irvine.',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 10,
    'expiration_hours': 7*24,  # 7 days
    # 'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        {
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}]
        },
    ]
}

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1.00,
    'participation_fee': 7.00,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}


SESSION_CONFIGS = [
    dict(
        name = 'identity',
        app_sequence = ['General_Instructions','Klee_Kandinsky','Klee_Kandinsky_discussion'],
        num_demo_participants = 10,
        assign_groups = True,
        Klee_group_proportion = 0.5,
        chat_time = 7,
        answer_value = 10,
    ),
    dict(
        name = 'rating',
        app_sequence = ['rating'],
        num_demo_participants = 5,
        video_id = True,
    )

    # {
    #     'name': 'chat',
    #     'display_name': 'chatrooms',
    #     'app_sequence': ['chat'],
    #     'num_demo_participants': 2,
    # },
    # 'name': 'Equal_WTP_Klee_WTP_Dictator_Trust',
    # {
    #     'name': 'Equal_WTP_Klee_WTP_Dictator_Trust',
    #     'display_name': 'Consumer Choice: Equal, Full Treatment',
    #     'app_sequence': ['General_Instructions', 'WTP', 'Klee_Kandinsky', 'Klee_Kandinsky_discussion',
    #                      'WTP2', 'Dictator_Game', 'Trust_Game', 'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 4,
    #     'Klee_group_proportion': 0.5,
    #     'real_world_currency_per_point': 0.10,
    #     'chat_time': 7,
    #     # Assign to groups based on painting choices if True;
    #     # otherwise just record painting choices
    #     'assign_groups': True,
    #     # True if other games are after, False otherwise
    #     'dictator_game': True,
    #     'trust_game': True,
    #     # True if WTP tasks are included, False otherwise
    #     'WTP_task': True,
    #     # Points for each correct response on the painting matching task
    #     'answer_value': 10,
    #     'object_type': "mug",
    #     # Maximum price to pay for the mug
    #     'max_price': 50,
    #     # Fake rounds always run before the real round
    #     'fake_rounds': 7,
    #     # Endowment in the dictator and trust games
    #     'endowment': 50,
    #     # Multiplier for the trust game
    #     'multiplier': 3,
    #     # To avoid deception, we need real data to calibrate these
    #     'group_proportion': None,
    # },
    # # 'name': 'Equal_WTP_Klee_WTP_Dictator',
    # {
    #     'name': 'Equal_WTP_Klee_WTP_Dictator',
    #     'display_name': 'Consumer Choice: Equal, Dictator',
    #     'app_sequence': ['General_Instructions', 'WTP', 'Klee_Kandinsky', 'Klee_Kandinsky_discussion',
    #                      'WTP2', 'Dictator_Game', 'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 4,
    #     'Klee_group_proportion': 0.5,
    #     'real_world_currency_per_point': 0.10,
    #     'chat_time': 7,
    #     # Assign to groups based on painting choices if True;
    #     # otherwise just record painting choices
    #     'assign_groups': True,
    #     # True if other games are after, False otherwise
    #     'dictator_game': True,
    #     'trust_game': False,
    #     # True if WTP tasks are included, False otherwise
    #     'WTP_task': True,
    #     # Points for each correct response on the painting matching task
    #     'answer_value': 10,
    #     'object_type': "mug",
    #     # Maximum price to pay for the mug
    #     'max_price': 50,
    #     # Fake rounds always run before the real round
    #     'fake_rounds': 7,
    #     # Endowment in the dictator and trust games
    #     'endowment': 50,
    #     # Multiplier for the trust game
    #     'multiplier': 3,
    #     # To avoid deception, we need real data to calibrate these
    #     'group_proportion': None,
    # },
    # # 'name': 'Equal_WTP_Klee_WTP_Trust',
    # {
    #     'name': 'Equal_WTP_Klee_WTP_Trust',
    #     'display_name': 'Consumer Choice: Equal, Trust',
    #     'app_sequence': ['General_Instructions', 'WTP', 'Klee_Kandinsky', 'Klee_Kandinsky_discussion',
    #                      'WTP2', 'Trust_Game', 'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 4,
    #     'Klee_group_proportion': 0.5,
    #     'real_world_currency_per_point': 0.10,
    #     'chat_time': 7,
    #     # Assign to groups based on painting choices if True;
    #     # otherwise just record painting choices
    #     'assign_groups': True,
    #     # True if other games are after, False otherwise
    #     'dictator_game': False,
    #     'trust_game': True,
    #     # True if WTP tasks are included, False otherwise
    #     'WTP_task': True,
    #     # Points for each correct response on the painting matching task
    #     'answer_value': 10,
    #     'object_type': "mug",
    #     # Maximum price to pay for the mug
    #     'max_price': 50,
    #     # Fake rounds always run before the real round
    #     'fake_rounds': 7,
    #     # Endowment in the dictator and trust games
    #     'endowment': 50,
    #     # Multiplier for the trust game
    #     'multiplier': 3,
    #     # To avoid deception, we need real data to calibrate these
    #     'group_proportion': None,
    # },
    # # 'name': 'Unequal_WTP_Klee_WTP_Dictator',
    # {
    #     'name': 'Unequal_WTP_Klee_WTP_Dictator',
    #     'display_name': 'Consumer Choice: Unequal, Dictator',
    #     'app_sequence': ['General_Instructions', 'WTP', 'Klee_Kandinsky', 'Klee_Kandinsky_discussion',
    #                      'WTP2', 'Dictator_Game', 'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 4,
    #     'Klee_group_proportion': 0.2,
    #     'real_world_currency_per_point': 0.10,
    #     'chat_time': 7,
    #     # Assign to groups based on painting choices if True;
    #     # otherwise just record painting choices
    #     'assign_groups': True,
    #     # True if other games are after, False otherwise
    #     'dictator_game': True,
    #     'trust_game': False,
    #     # True if WTP tasks are included, False otherwise
    #     'WTP_task': True,
    #     # Points for each correct response on the painting matching task
    #     'answer_value': 10,
    #     'object_type': "mug",
    #     # Maximum price to pay for the mug
    #     'max_price': 50,
    #     # Fake rounds always run before the real round
    #     'fake_rounds': 7,
    #     # Endowment in the dictator and trust games
    #     'endowment': 50,
    #     # Multiplier for the trust game
    #     'multiplier': 3,
    #     # To avoid deception, we need real data to calibrate these
    #     'group_proportion': None,
    # },
    # # 'name': 'Unequal_WTP_Klee_WTP_Trust',
    # {
    #     'name': 'Unequal_WTP_Klee_WTP_Trust',
    #     'display_name': 'Consumer Choice: Unequal, Trust',
    #     'app_sequence': ['General_Instructions', 'WTP', 'Klee_Kandinsky', 'Klee_Kandinsky_discussion',
    #                      'WTP2', 'Trust_Game', 'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 4,
    #     'Klee_group_proportion': 0.2,
    #     'real_world_currency_per_point': 0.10,
    #     'chat_time': 7,
    #     # Assign to groups based on painting choices if True;
    #     # otherwise just record painting choices
    #     'assign_groups': True,
    #     # True if other games are after, False otherwise
    #     'dictator_game': False,
    #     'trust_game': True,
    #     # True if WTP tasks are included, False otherwise
    #     'WTP_task': True,
    #     # Points for each correct response on the painting matching task
    #     'answer_value': 10,
    #     'object_type': "mug",
    #     # Maximum price to pay for the mug
    #     'max_price': 50,
    #     # Fake rounds always run before the real round
    #     'fake_rounds': 7,
    #     # Endowment in the dictator and trust games
    #     'endowment': 50,
    #     # Multiplier for the trust game
    #     'multiplier': 3,
    #     # To avoid deception, we need real data to calibrate these
    #     'group_proportion': None,
    # },
    # # 'name': 'Equal_WTP_Klee_WTP',
    # {
    #     'name': 'Equal_WTP_Klee_WTP',
    #     'display_name': 'Consumer Choice: Equal, Group Only',
    #     'app_sequence': ['General_Instructions', 'WTP', 'Klee_Kandinsky', 'Klee_Kandinsky_discussion',
    #                      'WTP2', 'Reveal_Purchase', 'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 4,
    #     'Klee_group_proportion': 0.5,
    #     'real_world_currency_per_point': 0.10,
    #     'chat_time': 7,
    #     # Assign to groups based on painting choices if True;
    #     # otherwise just record painting choices
    #     'assign_groups': True,
    #     # True if other games are after, False otherwise
    #     'dictator_game': False,
    #     'trust_game': False,
    #     # True if WTP tasks are included, False otherwise
    #     'WTP_task': True,
    #     # Points for each correct response on the painting matching task
    #     'answer_value': 10,
    #     'object_type': "mug",
    #     # Maximum price to pay for the mug
    #     'max_price': 50,
    #     # Fake rounds always run before the real round
    #     'fake_rounds': 7,
    #     # Endowment in the dictator and trust games
    #     'endowment': 50,
    #     # Multiplier for the trust game
    #     'multiplier': 3,
    #     # To avoid deception, we need real data to calibrate these
    #     'group_proportion': None,
    # },
    # # 'name': 'Unequal_WTP_Klee_WTP',
    # {
    #     'name': 'Unequal_WTP_Klee_WTP',
    #     'display_name': 'Consumer Choice: Equal, Group Only',
    #     'app_sequence': ['General_Instructions', 'WTP', 'Klee_Kandinsky', 'Klee_Kandinsky_discussion',
    #                      'WTP2', 'Reveal_Purchase', 'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 4,
    #     'Klee_group_proportion': 0.2,
    #     'real_world_currency_per_point': 0.10,
    #     'chat_time': 7,
    #     # Assign to groups based on painting choices if True;
    #     # otherwise just record painting choices
    #     'assign_groups': True,
    #     # True if other games are after, False otherwise
    #     'dictator_game': False,
    #     'trust_game': False,
    #     # True if WTP tasks are included, False otherwise
    #     'WTP_task': True,
    #     # Points for each correct response on the painting matching task
    #     'answer_value': 10,
    #     'object_type': "mug",
    #     # Maximum price to pay for the mug
    #     'max_price': 50,
    #     # Fake rounds always run before the real round
    #     'fake_rounds': 7,
    #     # Endowment in the dictator and trust games
    #     'endowment': 50,
    #     # Multiplier for the trust game
    #     'multiplier': 3,
    #     # To avoid deception, we need real data to calibrate these
    #     'group_proportion': None,
    # },
    # # 'name': 'WTP_nogroup_WTP',
    # {
    #     'name': 'WTP_nogroup_WTP',
    #     'display_name': 'Consumer Choice: WTP Only',
    #     'app_sequence': ['General_Instructions', 'WTP', 'Klee_Kandinsky', 'WTP2', 'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 4,
    #     'real_world_currency_per_point': 0.10,
    #     # Assign to groups based on painting choices if True;
    #     # otherwise just record painting choices
    #     'assign_groups': False,
    #     # True if other games are after, False otherwise
    #     'dictator_game': False,
    #     'trust_game': False,
    #     # True if WTP tasks are included, False otherwise
    #     'WTP_task': True,
    #     'object_type': "mug",
    #     # Maximum price to pay for the mug
    #     'max_price': 50,
    #     # Fake rounds always run before the real round
    #     'fake_rounds': 7,
    #     # To avoid deception, we need real data to calibrate these
    #     'group_proportion': None,
    # },
    # # 'name': 'Equal_Klee_Dictator_Trust',
    # {
    #     'name': 'Equal_Klee_Dictator_Trust',
    #     'display_name': 'Consumer Choice: Equal, Group Games Only',
    #     'app_sequence': ['General_Instructions', 'Klee_Kandinsky', 'Klee_Kandinsky_discussion',
    #                      'Dictator_Game', 'Trust_Game', 'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 4,
    #     'Klee_group_proportion': 0.5,
    #     'real_world_currency_per_point': 0.10,
    #     'chat_time': 7,
    #     # True if other games are after, False otherwise
    #     'dictator_game': True,
    #     'trust_game': True,
    #     # True if WTP tasks are included, False otherwise
    #     'WTP_task': False,
    #     # Assign to groups based on painting choices if True;
    #     # otherwise just record painting choices
    #     'assign_groups': True,
    #     # Points for each correct response on the painting matching task
    #     'answer_value': 10,
    #     # Endowment in the dictator and trust games
    #     'endowment': 50,
    #     # Multiplier for the trust game
    #     'multiplier': 3,
    #     # To avoid deception, we need real data to calibrate these
    #     'group_proportion': None,
    # },
    # # 'name': 'Unequal_Klee_Dictator_Trust',
    # {
    #     'name': 'Unequal_Klee_Dictator_Trust',
    #     'display_name': 'Consumer Choice: Unequal, Group Games Only',
    #     'app_sequence': ['General_Instructions', 'Klee_Kandinsky', 'Klee_Kandinsky_discussion',
    #                      'Dictator_Game', 'Trust_Game', 'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 4,
    #     'Klee_group_proportion': 0.2,
    #     'real_world_currency_per_point': 0.10,
    #     'chat_time': 7,
    #     # True if other games are after, False otherwise
    #     'dictator_game': True,
    #     'trust_game': True,
    #     # True if WTP tasks are included, False otherwise
    #     'WTP_task': False,
    #     # Assign to groups based on painting choices if True;
    #     # otherwise just record painting choices
    #     'assign_groups': True,
    #     # Points for each correct response on the painting matching task
    #     'answer_value': 10,
    #     # Endowment in the dictator and trust games
    #     'endowment': 50,
    #     # Multiplier for the trust game
    #     'multiplier': 3,
    #     # To avoid deception, we need real data to calibrate these
    #     'group_proportion': None,
    # },
    # {
    #     'name': 'WTP_Klee_WTP_Trust',
    #     'display_name': 'Trust Game Test',
    #     'app_sequence': ['WTP','Klee_Kandinsky', 'Klee_Kandinsky_discussion', 'WTP2', 'Trust_Game',
    #                     'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 40,
    #     'Klee_group_proportion': 0.5,
    #     'chat_time': 1,
    #     'fake_rounds': 1,
    #     'games': True,
    #     'WTP_task': True,
    #     'object_type': 'mug',
    #     'max_price': 50,
    #     'assign_groups': True,
    #     'answer_value': 10,
    #     'endowment': 50,
    #     'multiplier': 3,
    #     'group_proportion': None,
    #     'real_world_currency_per_point': 0.10,
    # },
    # {
    #     'name': 'WTP_Klee_WTP_Dictator',
    #     'display_name': 'Dictator Game Test',
    #     'app_sequence': ['WTP', 'Klee_Kandinsky', 'Klee_Kandinsky_discussion', 'WTP2', 'Dictator_Game',
    #                      'WTP_Survey', 'Final_Summary'],
    #     'num_demo_participants': 40,
    #     'Klee_group_proportion': 0.5,
    #     'chat_time': 1,
    #     'fake_rounds': 1,
    #     'games': True,
    #     'WTP_task': True,
    #     'object_type': 'mug',
    #     'max_price': 50,
    #     'assign_groups': True,
    #     'answer_value': 10,
    #     'endowment': 50,
    #     'multiplier': 3,
    #     'group_proportion': None,
    #     'real_world_currency_per_point': 0.10,
    # },
]
# see the end of this file for the inactive session configs

# # Channel routing for real-time interaction
CHANNEL_ROUTING = 'double_auction.routing.channel_routing'

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_DECIMAL_PLACES = 1

BROWSER_COMMAND = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"

ROOMS = [
    {
        'name': 'ESSL_experiment',
        'display_name': 'ESSL experiments',
    },
]

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# Consider '', None, and '0' to be empty/false
DEBUG = False

DEMO_PAGE_INTRO_HTML = """
Here are various games implemented with 
oTree. These games are open
source, and you can modify them as you wish.
"""

# don't share this with anybody.
SECRET_KEY = '4tab1edvsgs5bpl2%^ia_zawm=a0lpah#%exc+yxm5jflp0oi2'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')

# They said to use environment variables, but I couldn't get that to work
# Patrick Julius keys
# AWS_ACCESS_KEY_ID = 'AKIAJWG4LCDDT5CBH7LA'
# AWS_SECRET_ACCESS_KEY = '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'

# John Duffy keys
AWS_ACCESS_KEY_ID = 'AKIAJMQ4MWM6PBFEUULQ'
AWS_SECRET_ACCESS_KEY = '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'

CSRF_COOKIE_NAME = 'csrftoken'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'otree.context_processors.otree',
            ],
        },
    },
]
