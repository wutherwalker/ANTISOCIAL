from .models import Player, Transaction
from otree.models import Participant
# from channels import Group
import json
import logging

from .messages import MatchMessage, FailBidMessage

logger = logging.getLogger(__name__)

# Generates bids for the bots
# def update_value(player, value, is_bot):
def update_value(player, value, quantity):
    print("update_value(" + str(player) + "," + str(value) + "," + str(quantity) + ")")
    # Why is this here? It's not called later. Is it to store data?
    new_bid = Transaction.objects.create(
        user = player,
        value = value,
        quantity = quantity,
        buyer_payoff = round(player.compute_value(quantity) - value, 2),
        seller_payoff = round(value - player.compute_cost(quantity), 2),
        # bot=is_bot
    )
    new_bid.save()
    player.value = value
    player.quantity = quantity
    # player.transaction_log += "Quantity: " + str(quantity) + " Tokens: " + str(value)
    player.save()
    print("Player value: " + str(player.value))
    print("Player quantity: " + str(player.quantity))
    return json.dumps({
        "player_id": player.id,
        "player_id_in_group": player.display_id,
        "value": value,
        "quantity": quantity,
        "group": player.group.id_in_subsession,
        "buyer_payoff": new_bid.buyer_payoff,
        "seller_payoff": new_bid.seller_payoff,
        "type": player.participant.vars["role"]
    })


# Once players are matched, compare bids
# The return value is a message; is it send through the socket layer?
def handle_bid(bid_info, is_bot=False):
    print("handle_bid(" + str(bid_info) + ")")
    player = bid_info["player"]
    new_value = bid_info["value"]
    new_quantity = bid_info["quantity"]
    player_role = player.participant.vars["role"]
    other_role = "buyer" if player_role == "seller" else "seller"
    optional_player_id = bid_info["optionalPlayerId"]
    messages = []

    if player.match_with is not None:
        print("Player already matched with: " + str(player.match_with))
    else:
        print("No current match; generating match")
    if player.match_with is None and new_value is not None:

        players = player.get_others_in_group()
        print("Self: " + str(player) + " Others in group: " + str(players))
        # other_role_players = [p for p in players if p.participant.vars["role"] == other_role]

        other_player = find_match_and_get_other_player(new_value, new_quantity, player_role, optional_player_id, players)
        print("Other player: " + str(other_player))

        if other_player is not None:
            if new_value != other_player.value:
                new_value = other_player.value

            if new_quantity != other_player.quantity:
                new_quantity = other_player.quantity

            # update_message = update_value(player, new_value, is_bot)
            print("Generating update message")
            update_message = update_value(player, new_value, new_quantity)
            messages.append(update_message)
            print("Generating match message")
            match_message = handle_match(player, new_value, new_quantity, other_player, player.id)
            messages.append(match_message)
        else:
            # update_message = update_value(player, new_value, is_bot)
            print("Generating update message, no match")
            update_message = update_value(player, new_value, new_quantity)
            messages.append(update_message)

        logger.info(messages)
        print(messages)
        # Log into oTree so we can see it later
        player.transaction_log += "Quantity: " + str(new_quantity) + " Tokens: " + str(new_value) + "; "
        player.save()
        return messages


# I'm not sure what 'code' is, but this is just grabbing a player based on it
def get_player_from_code(code):
    participant = Participant.objects.get(code=code);
    return Player.objects.filter(participant=participant, round_number=participant._round_number).first()

# This only returns players of the opposite role
def filter_other_players(other_role_players):
    return [ p for p in other_role_players if p.value and p.match_with is None]

# This checks whether the other player's value matches 'new_value'
# Is 'new_value' the agreed-upon value?
def check_match_with(other_player, new_value):
    print("check_match_with(" + str(other_player) + "," + str(new_value) + ")")
    return other_player.value == new_value and other_player.match_with is None

# This gets called when two players get matched
def handle_match(player, value, quantity, other_player, player_id):
    print("handle_match(" + str(player) + "," + str(value) + "," + str(quantity) + "," + str(other_player) + "," + str(player_id) + ")")
    """ When a match happens, this functions handles it """

    buyer = player if player.participant.vars["role"] == "buyer" else other_player
    seller = player if player.participant.vars["role"] == "seller" else other_player

    buyer_id = int(player_id) if player.participant.vars["role"] == "buyer" else other_player.id
    seller_id = int(player_id) if player.participant.vars["role"] == "seller" else other_player.id

    logger.info("seller %s and buyer %s match", seller_id, buyer_id)
    # logger.info("player %s and other_player %s match", player.value, other_player.value)

    if buyer.group == seller.group:
        buyer.match_with = seller
        seller.match_with = buyer
        buyer.value = value
        seller.value = value
        buyer.quantity = quantity
        seller.quantity = quantity
        buyer.benefit = buyer.compute_value(buyer.quantity)
        seller.cost = seller.compute_cost(seller.quantity)
        print("Buyer quantity: " + str(buyer.quantity))
        print("Buyer price: " + str(buyer.value))
        print("Buyer benefit: " + str(buyer.benefit))
        print("Seller quantity: " + str(seller.quantity))
        print("Seller price: " + str(seller.value))
        print("Seller cost: " + str(seller.cost))
        buyer.payoff = round(buyer.benefit - buyer.value, 2)
        seller.payoff = round(seller.value - seller.cost, 2)
        other_player.save()
        player.save()

        match = MatchMessage(buyer_id, seller_id, player.value, player.quantity, buyer.payoff, seller.payoff)
        return match.getMessage()
    else:
        print("Attempted to match buyer " + str(buyer) + " in group " + str(buyer.group) + " with seller " + \
              str(seller) + " in group " + str(seller.group.id_in_subsession))
        return False

# The functions below I want to eventually remove
# Cycles through players of the opposite role; I may not need this function
def get_other_player(other_player_id, other_role_players):
    logger.info("optionalPlayerId set")
    return next((player for player in other_role_players if player.id == other_player_id), None)


# As far as I can tell this function is never used
# # Compares the current bid with alternatives that might be better
# def get_better_bids(players, player_role, new_value):
#     """ Check if there are better bids from other users """
#     for p in players:
#         if p.value:
#             if player_role == "seller" and p.value < new_value and not p.match_with or player_role == "buyer" and p.value > new_value and not p.match_with:
#                 yield p

# Finds other players with bids compatible to yours
def find_matching_player(player_role, new_value, new_quantity, other_role_players):
    filtered_other_players = filter_other_players(other_role_players)
    for other_player in filtered_other_players:
        if new_quantity == other_player.quantity and (player_role == "buyer" and other_player.value <= new_value or player_role == "seller" and other_player.value >= new_value):
                logger.info("match!")
                return other_player
    return None

def find_match_and_get_other_player(new_value, new_quantity, player_role, optional_player_id, other_role_players):
    print("find_match_and_get_other_player(" + str(new_value) + "," + str(new_quantity) + "," + player_role + "," + str(optional_player_id) + "," + str(other_role_players) + ")")
    if optional_player_id:
        other_player_id = optional_player_id
        other_player = get_other_player(other_player_id, other_role_players)

        if check_match_with(other_player, new_value):
            return other_player

    else:
        return find_matching_player(player_role, new_value, new_quantity, other_role_players)
