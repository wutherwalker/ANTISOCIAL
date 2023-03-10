from huey.contrib.djhuey import task
# from channels import Group
import json

# This is what all that logging stuff is about
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

from .helpers import get_player_from_code, handle_bid
from .messages import MatchMessage

# This generates automated bids
@task()
def automated_bid(code, round_number):
    player = get_player_from_code(code)
    session_code = player.participant.session.code
    logging_info = 'automated_bid: round_number: {}, player_id: {}, code: {}, value: {}, display_id: {}, call_round_number: {}, is_bot: {}'.format(player.round_number, player.id, code, player.value, player.display_id, round_number, player.participant.vars['is_bot'])
    logger.info(logging_info)
    if 'is_bot' in player.participant.vars and player.participant.vars['is_bot'] and player.match_with is None and player.value is None and player.round_number is round_number:
        player.is_bot = True
        player.save()

        bid_info = {
            "player": player,
            "value": player.money if player.participant.vars["role"] == "buyer" else player.cost,
            "optionalPlayerId": None
        }
        responses = handle_bid(bid_info, is_bot=True)
        responses = [responses] if isinstance(responses, str) else responses
        for response in responses:
            Group(session_code).send({
                "text": response
            })

        logger.info("automated bid for %s", code)
