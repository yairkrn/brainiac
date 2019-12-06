import datetime as dt

from .thought import Thought
from .utils import Connection


def upload_thought(address, user_id, thought):
    """
    Send a Thought object to a given server address.
    
    Args:
        address ((str, int)): host/ip server address and port.
        user_id (int): the user sending the data.
        thought (Thought): the Thought object to send to server.
    """
    thought_obj = Thought(user_id=user_id,
                          timestamp=dt.datetime.now(),
                          thought=thought)
    with Connection.connect(host=address[0], port=address[1]) as connection:
        connection.send(thought_obj.serialize())
