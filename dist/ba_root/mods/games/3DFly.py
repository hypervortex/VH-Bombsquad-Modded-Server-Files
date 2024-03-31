
"""
Join BCS: https://discord.gg/ucyaesh

================

3DFlyCMDV2 (1.7 update)
by Jetz

Whats New:
- Added arguments
- Can now use 3dflying for other players by putting their activity ID in the argument
"""

# ba_meta require api 7
from __future__ import annotations
from typing import TYPE_CHECKING

import ba
import _ba

if TYPE_CHECKING:
  from typing import Union, Sequence


def flying(actor: ba.Actor):
  if actor.node.exists():
    actor.node.handlemessage(
      'impulse', actor.node.position[0], actor.node.position[1], actor.node.position[2],
      0.0, 0.0, 0.0, 200.0, 200.0, 0.0, 0.0, 0.0, 1.0, 0.0)


old_message = _ba.chatmessage
def new_message(message: Union[str, ba.Lstr],
              clients: Sequence[float] = None,
              sender_override: str = None):
  old_message(message, clients, sender_override)
  m = message.split(' ')[0]
  a = message.split(' ')[1:]
  foreground_act = _ba.get_foreground_host_activity()
  with ba.Context(foreground_act):
    if m == '/3dfly':
      if a == []:
        ba.screenmessage('/3dfly all or /3dfly [player ID]',
                         color=(1.0, 1.0, 0.0))
      else:
        if a[0] == 'all':
          foreground_act.players.assigninput(ba.InputType.JUMP_PRESS,
                                             ba.Call(flying, foreground_act.players.actor))
        else:
          pID = int(a[0])
          foreground_act.players[pID].assigninput(ba.InputType.JUMP_PRESS,
                                                  ba.Call(flying, foreground_act.players[pID].actor))


# ba_meta export plugin
class byJetz(ba.Plugin):
  def __init__(self):
    _ba.chatmessage = new_message