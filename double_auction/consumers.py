import random
import json
import time
import math
import datetime
import logging
from channels import Group
from channels.sessions import channel_session

import otree.common_internal

from .models import Player, Group as OtreeGroup, Constants

from django.conf import settings

# This gets a controller? For... bets? What?
from .controllers.bets import clear_bet

from .tasks import automated_bid

from .helpers import handle_bid, get_player_from_code

# from channels.auth import channel_session_user, channel_session_user_from_http
# from channels.sessions import channel_session

# Get an instance of a logger
logger = logging.getLogger(__name__)

# When is 'connect' called? How are channels created?
def websocket_connect(connection, code):
    """
    the user connects to the socket. He is added to the group channel and receives the current state on his personal channel
    """
    logger.info("Participant %s connected", code )
    player = get_player_from_code(code)
    session_code = player.participant.session.code
    if 'is_bot' in player.participant.vars and player.participant.vars['is_bot']:
        player.is_bot = False
        # I don't actually know what save() does here
        player.save()
        player.participant.vars["is_bot"] = False
        player.participant.save()
        Group(session_code).send({
            "text": json.dumps({
                "type": "status",
                "status": '',
                "player_id": player.id
            })
        })
    logger.info("Player connected %s" % connection.reply_channel)
    Group(session_code).add(connection.reply_channel)
    Group("player-%s" % player.id).add(connection.reply_channel)
    # connection.reply_channel.send({"accept": True})

    messages = []
    for p in player.group.get_players():
        # if 'is_bot' in p.participant.vars and p.participant.vars['is_bot']:
        #     connection.reply_channel.send({
        #         "text": json.dumps({
        #             "type": "status",
        #             "status": "bot",
        #             "player_id": p.id
        #         })
        #     })
        if p.value is not None:
            if p.match_with is None:
                tokens = p.value
                quantity = p.quantity
                message = json.dumps({
                    "value": tokens,
                    "quantity": quantity,
                    "buyer_payoff": round(p.compute_value(quantity) - tokens, 2),
                    "seller_payoff": round(tokens - p.compute_cost(quantity), 2),
                    "type": p.participant.vars["role"],
                    "group": p.group.id_in_subsession,
                    "player_id": p.id,
                    "player_id_in_group": p.display_id,
                })
                messages.append(message)

    for message in messages:
        connection.reply_channel.send({"text": message})


# So the message is sent as a string, and then this code
# handles the event and parses the string.
# Connected to websocket.receive
def websocket_message(message, code):
    """
    check what the user message contains and react accordingly
    """
    jsonmessage = json.loads(message.content['text'])
    logger.info("Message received on socket. message:  %s", jsonmessage)

    player = get_player_from_code(code)
    logger.info(player.id)
    session_code = player.participant.session.code

    action_type = jsonmessage["type"]

# This 'clears' a bid, i.e. makes it happen
    if action_type == "clear":
        print("websocket_message, action_type is clear")
        responses = clear_bet(player.id)
    elif action_type == "seller" or action_type == "buyer":
        print("websocket_message, action_type is seller or buyer")
        bid_info = {
            'player': player,
            "value": jsonmessage["value"] if "value" in jsonmessage else None,
            "quantity": jsonmessage["quantity"] if "quantity" in jsonmessage else None,
            "group": jsonmessage["group"] if "group" in jsonmessage else None,
            "buyer_payoff": jsonmessage["buyer_payoff"] if "buyer_payoff" in jsonmessage else None,
            "seller_payoff": jsonmessage["seller_payoff"] if "seller_payoff" in jsonmessage else None,
            "optionalPlayerId": jsonmessage["optionalPlayerId"] if "optionalPlayerId" in jsonmessage else None
        }
        print(bid_info)
        responses = handle_bid(bid_info)

    # I don't understand what isinstance() is doing here
    # Really, I don't understand this part at all
    responses = [responses] if isinstance(responses, str) else responses
    for response in responses:
        Group(session_code).send({
            "text": response
        })

# This is called when you 'disconnect' from the socket, but when does that happen?
# Connected to websocket.disconnect
def websocket_disconnect(connection, code):
    logger.info('player disconnected {}'.format( code ))
    player = get_player_from_code(code)
    session_code = player.participant.session.code
    now = time.time()
    starttime = now if now > player.session.vars["starttime"] else player.session.vars["starttime"]
    endtime = player.session.vars["endtime"]
    remaining_seconds = endtime - starttime
    # if 1 < remaining_seconds < 3:
    #     player.participant.vars['is_bot'] = True
    #     player.participant.save()
    #     if not player.value:
    #         # Logic for the bots to bid automatically at the end
    #         if player.participant.session.config['bot_enable']:
    #             if otree.common_internal.USE_REDIS:
    #                 logger.info("automated bid now: %s", player.participant.code)
    #                 automated_bid(code, player.round_number)
    #             else:
    #                 logger.warning("you enabled bots but there will be no automated_bid if you don't enable redis (set REDIS_URL)")
    #     Group(session_code).send({
    #         "text": json.dumps({
    #             "type": "status",
    #             "status": "bot",
    #             "player_id": player.id
    #         })
    #     })
    # elif remaining_seconds >= 3:
    #     random_seconds = random.random() * ( endtime - 3 - starttime)
    #     random_timestamp = starttime + random_seconds
    #     random_time = datetime.datetime.fromtimestamp(random_timestamp)
    #     player.participant.vars['is_bot'] = True
    #     player.participant.save()
    #     player.is_bot = True
    #     player.save()
    #     if not player.value:
    #         # Logic for the bots to bid automatically at the end
    #         if player.participant.session.config['bot_enable']:
    #             if otree.common_internal.USE_REDIS:
    #                 logger.info("schedule automated bid: %s %s %s, now_or_starttime: %s", player.participant.code, random_seconds, random_time, starttime)
    #                 automated_bid.schedule(args=(code,player.round_number,), eta=random_time, convert_utc=True)
    #             else:
    #                 logger.warning("you enabled bots but there will be no automated_bid if you don't enable redis (set REDIS_URL)")
    #     Group(session_code).send({
    #         "text": json.dumps({
    #             "type": "status",
    #             "status": "bot",
    #             "player_id": player.id
    #         })
    #     })
    # else:
    print("end of auction at " + str(now) + " with " + str(remaining_seconds) + " seconds left.")

    Group(session_code).discard(connection.reply_channel)
    Group("player-%s" % player.id).discard(connection.reply_channel)

