import json

# These seem to be using some built-in functionality for json messages
# where the expected function is getMessage() and the return value
# is a json.dumps() which takes a dictionary

# One type of message is a message indicating a match
class MatchMessage:
    def __init__(self, buyer, seller, value, quantity, buyer_payoff, seller_payoff):
        self.seller = seller
        self.buyer = buyer
        self.value = value
        self.quantity = quantity
        self.buyer_payoff = buyer_payoff
        self.seller_payoff = seller_payoff
        # self.group = group
    def getMessage(self):
        print("MatchMessage.getMessage")
        return json.dumps({
            "type": "match",
            "buyer": self.buyer,
            "seller": self.seller,
            "value": self.value,
            "quantity": self.quantity,
            "buyer_payoff": round(float(self.buyer_payoff), 2),
            "seller_payoff": round(float(self.seller_payoff), 2),
            # "group": self.group,
        })

# The other type of message is indicating a failed bid somehow
class FailBidMessage:
    def getMessage(self):
        print("FailBidMessage.getMessage")
        return json.dumps({
            "type": "error",
            "error": "BadBid"
        })
