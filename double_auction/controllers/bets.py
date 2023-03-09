from channels import Group
from ..models import Player
import json

# Why is this function all the way over here in a separate folder!?
def clear_bet(user_id):
    player = Player.objects.get(id=user_id)
    player.value = None
    # These two statements are important, but I don't understand them
    player.save()
    return [json.dumps({
        "player_id": player.id,
        "type": "clear"
    })]
