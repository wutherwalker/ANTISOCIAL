from channels.routing import route
from .consumers import websocket_connect, websocket_message, websocket_disconnect
from otree.channels.routing import channel_routing
from channels.routing import include, route_class

# Okay, here's where it gets sticky.
# This defines the double_auction_routing variable
# It takes a list of three routes:
# websocket.connect, websocket.receive, and websocket.disconnect
# Each of these is then given a path which is defined by a regular expression,
# as well as a function to call, which was defined in consumers.py.
# The regular expressions are identical; let's interpret what they mean.
# r': this is a regular expression string in 'raw' notation, where backslashes aren't escapes,
# So that it can be FED to a regular expression parser where they WILL be escapes
# ^: first character
# /: Literal forward-slash /
#  ( start group
# ?P<code>: Name this group 'code' so we can use it later
# \w+: One or more word characters (i.e., letters, numbers, or underscores)
# end of group that will be named 'code'
# $: last character
# ': end string
double_auction_routing = [route("websocket.connect",
                websocket_connect,  path=r'^/(?P<code>\w+)$'),
                route("websocket.receive",
                websocket_message,  path=r'^/(?P<code>\w+)$'),
                route("websocket.disconnect",
                websocket_disconnect,  path=r'^/(?P<code>\w+)$'), ]
# This is ADDING (appending?) an include() statement
# which uses the double_auction_routing variable defined above
channel_routing += [
    include(double_auction_routing, path=r"^/double-auction"),
]
