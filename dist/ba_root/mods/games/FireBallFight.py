# Released under the MIT License. See LICENSE for details.
"""FireBall Fight game and support classes."""

# FireBall Fight game
# This was Originally made by MattZ45986
# I ported this to 1.6 and added some new things
# This is only version 1, there are more version to come yet.
# so till then, enjoy this and suggest what to add.
# ba_meta require api 7
# (see https://ballistica.net/wiki/meta-tag-system)

from __future__ import annotations

from typing import TYPE_CHECKING
import ba, random, base64
from bastd.gameutils import SharedObjects
from bastd.actor.playerspaz import PlayerSpaz
from bastd.actor.scoreboard import Scoreboard

if TYPE_CHECKING:
    from typing import Any, Union, Sequence, Optional

# encoding this code because it's messy, so it's better if you don't decode this.
exec(base64.b64decode("Y2xhc3MgRmlyZUJhbGxGYWN0b3J5KG9iamVjdCk6CiAgICBkZWYgX19pbml0X18oc2VsZik6CiAgICAgICAgc2VsZi5sYXN0X3Nob3RfdGltZSA9IDAKICAgICAgICBzaGFyZWQgPSBTaGFyZWRPYmplY3RzLmdldCgpCiAgICAgICAgc2VsZi5iYWxsX21hdGVyaWFsID0gYmEuTWF0ZXJpYWwoKQogICAgICAgIHNlbGYuYmFsbF9tYXRlcmlhbC5hZGRfYWN0aW9ucyhjb25kaXRpb25zID0gKCgoIndlX2FyZV95b3VuZ2VyX3RoYW4iLCA1KSwgIm9yIiwgKCJ0aGV5X2FyZV95b3VuZ2VyX3RoYW4iLCA1MCkpLCAiYW5kIiwgKCJ0aGV5X2hhdmVfbWF0ZXJpYWwiLCBzaGFyZWQub2JqZWN0X21hdGVyaWFsKSksIGFjdGlvbnMgPSAoIm1vZGlmeV9ub2RlX2NvbGxpc2lvbiIsICdjb2xsaWRlJywgRmFsc2UpKQogICAgICAgIHNlbGYuYmFsbF9tYXRlcmlhbC5hZGRfYWN0aW9ucygKICAgICAgICAgICAgY29uZGl0aW9ucz0oJ3RoZXlfaGF2ZV9tYXRlcmlhbCcsIHNoYXJlZC5waWNrdXBfbWF0ZXJpYWwpLAogICAgICAgICAgICBhY3Rpb25zPSgnbW9kaWZ5X3BhcnRfY29sbGlzaW9uJywgJ3VzZV9ub2RlX2NvbGxpZGUnLCBGYWxzZSksCiAgICAgICAgICAgICkKICAgICAgICBzZWxmLmJhbGxfbWF0ZXJpYWwuYWRkX2FjdGlvbnMoCiAgICAgICAgICAgIGFjdGlvbnMgPSAoIm1vZGlmeV9wYXJ0X2NvbGxpc2lvbiIsICJmcmljdGlvbiIsIDApCiAgICAgICAgICAgICkKICAgICAgICBzZWxmLmJhbGxfbWF0ZXJpYWwuYWRkX2FjdGlvbnMoCiAgICAgICAgICAgIGNvbmRpdGlvbnMgPSAoInRoZXlfaGF2ZV9tYXRlcmlhbCIsIHNoYXJlZC5wbGF5ZXJfbWF0ZXJpYWwpLAogICAgICAgICAgICBhY3Rpb25zID0gKCgibW9kaWZ5X3BhcnRfY29sbGlzaW9uIiwgInBoeXNpY2FsIiwgRmFsc2UpLAogICAgICAgICAgICAoJ21lc3NhZ2UnLCAnb3VyX25vZGUnLCAnYXRfY29ubmVjdCcsIFRvdWNoZWRTcGF6KCkpKSwKICAgICAgICAgICAgKQogICAgICAgIHNlbGYuYmFsbF9tYXRlcmlhbC5hZGRfYWN0aW9ucygKICAgICAgICAgICAgY29uZGl0aW9ucyA9ICgoInRoZXlfZG9udF9oYXZlX21hdGVyaWFsIiwgc2hhcmVkLnBsYXllcl9tYXRlcmlhbCksICdhbmQnLAogICAgICAgICAgICAoInRoZXlfaGF2ZV9tYXRlcmlhbCIsIHNoYXJlZC5vYmplY3RfbWF0ZXJpYWwpKSwKICAgICAgICAgICAgYWN0aW9ucyA9ICgnbWVzc2FnZScsICdvdXJfbm9kZScsICdhdF9jb25uZWN0JywgVG91Y2hlZE9iamVjdCgpKSwKICAgICAgICAgICAgKQogICAgICAgIHNlbGYuYmFsbF9tYXRlcmlhbC5hZGRfYWN0aW9ucygKICAgICAgICAgICAgY29uZGl0aW9ucyA9ICgoInRoZXlfZG9udF9oYXZlX21hdGVyaWFsIiwgc2hhcmVkLnBsYXllcl9tYXRlcmlhbCksICdhbmQnLAogICAgICAgICAgICAoInRoZXlfaGF2ZV9tYXRlcmlhbCIsIHNoYXJlZC5mb290aW5nX21hdGVyaWFsKSksCiAgICAgICAgICAgIGFjdGlvbnMgPSAoJ21lc3NhZ2UnLCAnb3VyX25vZGUnLCAnYXRfY29ubmVjdCcsIFRvdWNoZWRGb290aW5nTWF0ZXJpYWwoKSksCiAgICAgICAgICAgICkKICAgIAogICAgZGVmIGdyYW50X2ZpcmVfYmFsbChzZWxmLCBzcGF6OiBiYS5BY3RvcikgLT4gTm9uZToKICAgICAgICBzcGF6LnB1bmNoX2NhbGxiYWNrID0gc2VsZi5zaG90X2ZpcmVfYmFsbAogICAgICAgIHNlbGYubGFzdF9zaG90X3RpbWUgPSBiYS50aW1lKHRpbWV0eXBlPWJhLlRpbWVUeXBlLkJBU0UsIHRpbWVmb3JtYXQ9YmEuVGltZUZvcm1hdC5NSUxMSVNFQ09ORFMpCiAgICAKICAgIGRlZiBzaG90X2ZpcmVfYmFsbChzZWxmLCBzcGF6OiBiYS5BY3RvcikgLT4gTm9uZToKICAgICAgICBzaG90X3RpbWUgPSBiYS50aW1lKHRpbWV0eXBlPWJhLlRpbWVUeXBlLkJBU0UsIHRpbWVmb3JtYXQ9YmEuVGltZUZvcm1hdC5NSUxMSVNFQ09ORFMpCiAgICAgICAgaWYgc2hvdF90aW1lIC0gc2VsZi5sYXN0X3Nob3RfdGltZSA+IDkwMDoKICAgICAgICAgICAgcG9zaXRpb24xID0gc3Bhei5ub2RlLnBvc2l0aW9uX2NlbnRlcgogICAgICAgICAgICBwb3NpdGlvbjIgPSBzcGF6Lm5vZGUucG9zaXRpb25fZm9yd2FyZAogICAgICAgICAgICBiYWxsX2RpcmVjdGlvbiA9IChwb3NpdGlvbjFbMF0gLSBwb3NpdGlvbjJbMF0sIDAuMCwgcG9zaXRpb24xWzJdIC0gcG9zaXRpb24yWzJdKQogICAgICAgICAgICBtYWduaXR1ZGUgPSAxMC4wIC8gYmEuVmVjMygqYmFsbF9kaXJlY3Rpb24pLmxlbmd0aCgpCiAgICAgICAgICAgIHZlbG9jaXR5ID0gW3YgKiBtYWduaXR1ZGUgZm9yIHYgaW4gYmFsbF9kaXJlY3Rpb25dCiAgICAgICAgICAgIEZpcmVCYWxsKHBvc2l0aW9uID0gc3Bhei5ub2RlLnBvc2l0aW9uLCB2ZWxvY2l0eSA9ICh2ZWxvY2l0eVswXSoyLCB2ZWxvY2l0eVsxXSoyLCB2ZWxvY2l0eVsyXSoyKSwgb3duZXIgPSBzcGF6LmdldHBsYXllcihwbGF5ZXJ0eXBlID0gYmEuUGxheWVyKSwgc291cmNlX3BsYXllciA9IHNwYXouZ2V0cGxheWVyKHBsYXllcnR5cGUgPSBiYS5QbGF5ZXIpKS5hdXRvcmV0YWluKCkKCmNsYXNzIFRvdWNoZWRTcGF6KG9iamVjdCk6CiAgICBwYXNzCgpjbGFzcyBUb3VjaGVkT2JqZWN0KG9iamVjdCk6CiAgICBwYXNzCgpjbGFzcyBUb3VjaGVkRm9vdGluZ01hdGVyaWFsKG9iamVjdCk6CiAgICBwYXNzCgpjbGFzcyBGaXJlQmFsbChiYS5BY3Rvcik6CiAgICBkZWYgX19pbml0X18oc2VsZiwgcG9zaXRpb24gPSAoMCwgNSwgMCksIHZlbG9jaXR5ID0gKDAsIDUsIDApLCBvd25lciA9IE5vbmUsIHNvdXJjZV9wbGF5ZXIgPSBOb25lKSAtPiBOb25lOgogICAgICAgIGJhLkFjdG9yLl9faW5pdF9fKHNlbGYpCiAgICAgICAgZmFjdG9yeSA9IHNlbGYuZ2V0X2ZhY3RvcnkoKQogICAgICAgIHNoYXJlZCA9IFNoYXJlZE9iamVjdHMuZ2V0KCkKICAgICAgICBzZWxmLm5vZGUgPSBiYS5uZXdub2RlKCJwcm9wIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGF0dHJzID0gewogICAgICAgICAgICAgICAgICAgICAgICAgICAgJ3Bvc2l0aW9uJzogcG9zaXRpb24sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAndmVsb2NpdHknOiB2ZWxvY2l0eSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICdtb2RlbCc6IGJhLmdldG1vZGVsKCJpbXBhY3RCb21iIiksCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAnYm9keSc6ICdzcGhlcmUnLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgJ2NvbG9yX3RleHR1cmUnOiBiYS5nZXR0ZXh0dXJlKCJidW5ueUNvbG9yIiksCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAnbW9kZWxfc2NhbGUnOiAwLjIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAnaXNfYXJlYV9vZl9pbnRlcmVzdCc6IFRydWUsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAnYm9keV9zY2FsZSc6IDAuOCwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICdtYXRlcmlhbHMnOiBbc2hhcmVkLm9iamVjdF9tYXRlcmlhbCwgZmFjdG9yeS5iYWxsX21hdGVyaWFsXQogICAgICAgICAgICAgICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRlbGVnYXRlID0gc2VsZikKICAgICAgICBzZWxmLnNvdXJjZV9wbGF5ZXIgPSBzb3VyY2VfcGxheWVyCiAgICAgICAgc2VsZi5vd25lciA9IG93bmVyCiAgICAgICAgc2VsZi5saWdodCA9IGJhLm5ld25vZGUoImxpZ2h0IiwgYXR0cnMgPSB7ImNvbG9yIjogKDEsIDAuNiwgMC40KSwgImhlaWdodF9hdHRlbnVhdGVkIjogRmFsc2UsICJyYWRpdXMiOiAwLjN9KQogICAgICAgIHNlbGYubm9kZS5jb25uZWN0YXR0cigicG9zaXRpb24iLCBzZWxmLmxpZ2h0LCAicG9zaXRpb24iKQogICAgICAgIGJhLmFuaW1hdGUoc2VsZi5saWdodCwgImludGVuc2l0eSIsIHswOiAxLjMsIDI1MDogMS44LCA1MDA6IDEuM30sIGxvb3AgPSBUcnVlLCB0aW1ldHlwZSA9IGJhLlRpbWVUeXBlLlNJTSwgdGltZWZvcm1hdD1iYS5UaW1lRm9ybWF0Lk1JTExJU0VDT05EUykKICAgICAgICBzZWxmLmZpcmVfYmFsbF9saWZlX3RpbWVyID0gYmEuVGltZXIoMSwgYmEuV2Vha0NhbGwoc2VsZi5kaWUpKQogICAgICAgIHNlbGYuZW1pdF90aW1lciA9IGJhLlRpbWVyKDAuMDE1LCBiYS5XZWFrQ2FsbChzZWxmLmVtaXQpLCByZXBlYXQgPSBUcnVlKQogICAgCiAgICBkZWYgZW1pdChzZWxmKSAtPiBOb25lOgogICAgICAgIGJhLmVtaXRmeChwb3NpdGlvbiA9IHNlbGYubm9kZS5wb3NpdGlvbiwgdmVsb2NpdHkgPSBzZWxmLm5vZGUudmVsb2NpdHksIHNjYWxlID0gNSwgc3ByZWFkID0gMC4xLCBjaHVua190eXBlID0gInN3ZWF0IikKICAgIAogICAgZGVmIGRpZShzZWxmKSAtPiBOb25lOgogICAgICAgIHNlbGYubGlnaHQuZGVsZXRlKCkKICAgICAgICBzZWxmLm5vZGUuaGFuZGxlbWVzc2FnZShiYS5EaWVNZXNzYWdlKCkpCiAgICAKICAgIEBjbGFzc21ldGhvZAogICAgZGVmIGdldF9mYWN0b3J5KGNscyk6CiAgICAgICAgYWN0aXZpdHkgPSBiYS5nZXRhY3Rpdml0eSgpCiAgICAgICAgaWYgYWN0aXZpdHkgaXMgTm9uZTogcmFpc2UgRXhjZXB0aW9uKCJubyBjdXJyZW50IGFjdGl2aXR5IGZvdW5kISIpCiAgICAgICAgdHJ5OiByZXR1cm4gYWN0aXZpdHkuX2ZpcmVCYWxsRmFjdG9yeQogICAgICAgIGV4Y2VwdDoKICAgICAgICAgICAgZiA9IGFjdGl2aXR5Ll9maXJlQmFsbEZhY3RvcnkgPSBGaXJlQmFsbEZhY3RvcnkoKQogICAgICAgICAgICByZXR1cm4gZgoKICAgIGRlZiBoYW5kbGVtZXNzYWdlKHNlbGYsIG1zZyk6CiAgICAgICAgc3VwZXIoc2VsZi5fX2NsYXNzX18sIHNlbGYpLmhhbmRsZW1lc3NhZ2UobXNnKQogICAgICAgIGlmIGlzaW5zdGFuY2UobXNnLCBUb3VjaGVkT2JqZWN0KToKICAgICAgICAgICAgbm9kZSA9IGJhLmdldGNvbGxpc2lvbigpLm9wcG9zaW5nbm9kZQogICAgICAgICAgICBpZiBub2RlIGFuZCBub2RlLmV4aXN0cygpOgogICAgICAgICAgICAgICAgdiA9IHNlbGYubm9kZS52ZWxvY2l0eQogICAgICAgICAgICAgICAgbSA9IGJhLlZlYzMoKnYpLmxlbmd0aCgpICogNDAKICAgICAgICAgICAgICAgIG5vZGUuaGFuZGxlbWVzc2FnZSgKICAgICAgICAgICAgICAgICAgICBiYS5IaXRNZXNzYWdlKHBvcyA9IHNlbGYubm9kZS5wb3NpdGlvbiwKICAgICAgICAgICAgICAgICAgICB2ZWxvY2l0eSA9IHYsCiAgICAgICAgICAgICAgICAgICAgbWFnbml0dWRlID0gbSwKICAgICAgICAgICAgICAgICAgICB2ZWxvY2l0eV9tYWduaXR1ZGUgPSBtLAogICAgICAgICAgICAgICAgICAgIHJhZGl1cyA9IDAsCiAgICAgICAgICAgICAgICAgICAgc3Jjbm9kZSA9IHNlbGYubm9kZSwKICAgICAgICAgICAgICAgICAgICBzb3VyY2VfcGxheWVyID0gc2VsZi5zb3VyY2VfcGxheWVyLAogICAgICAgICAgICAgICAgICAgIGZvcmNlX2RpcmVjdGlvbiA9IHNlbGYubm9kZS52ZWxvY2l0eSkKICAgICAgICAgICAgICAgICAgICApCiAgICAgICAgICAgIHNlbGYubm9kZS5oYW5kbGVtZXNzYWdlKGJhLkRpZU1lc3NhZ2UoKSkKICAgICAgICAKICAgICAgICBlbGlmIGlzaW5zdGFuY2UobXNnLCBiYS5EaWVNZXNzYWdlKToKICAgICAgICAgICAgCiAgICAgICAgICAgIGlmIHNlbGYubm9kZS5leGlzdHMoKToKICAgICAgICAgICAgICAgIHZlbG9jaXR5ID0gc2VsZi5ub2RlLnZlbG9jaXR5CiAgICAgICAgICAgICAgICBleHBsb3Npb24gPSBiYS5uZXdub2RlKCJleHBsb3Npb24iLAogICAgICAgICAgICAgICAgYXR0cnMgPSB7J3Bvc2l0aW9uJzogc2VsZi5ub2RlLnBvc2l0aW9uLAogICAgICAgICAgICAgICAgJ3ZlbG9jaXR5JzogKHZlbG9jaXR5WzBdLCBtYXgoLTEuMCwgdmVsb2NpdHlbMV0pLCB2ZWxvY2l0eVsyXSksCiAgICAgICAgICAgICAgICAncmFkaXVzJzogMiwKICAgICAgICAgICAgICAgICdiaWcnOiBGYWxzZQogICAgICAgICAgICAgICAgfSkKICAgICAgICAgICAgICAgIGJhLnBsYXlzb3VuZChzb3VuZCA9IGJhLmdldHNvdW5kKHJhbmRvbS5jaG9pY2UoWydpbXBhY3RIYXJkJywgJ2ltcGFjdEhhcmQyJywgJ2ltcGFjdEhhcmQzJ10pKSwgcG9zaXRpb24gPSBzZWxmLm5vZGUucG9zaXRpb24pCiAgICAgICAgICAgICAgICBzZWxmLm5vZGUuZGVsZXRlKCkKICAgICAgICAgICAgICAgIHNlbGYuZW1pdF90aW1lciA9IE5vbmUKICAgICAgICAKICAgICAgICBlbGlmIGlzaW5zdGFuY2UobXNnLCBiYS5PdXRPZkJvdW5kc01lc3NhZ2UpOgogICAgICAgICAgICBzZWxmLm5vZGUuaGFuZGxlbWVzc2FnZShiYS5EaWVNZXNzYWdlKCkpCiAgICAgICAgCiAgICAgICAgZWxpZiBpc2luc3RhbmNlKG1zZywgYmEuSGl0TWVzc2FnZSk6CiAgICAgICAgICAgIHNlbGYubm9kZS5oYW5kbGVtZXNzYWdlKCJpbXB1bHNlIiwKICAgICAgICAgICAgbXNnLnBvc1swXSwgbXNnLnBvc1sxXSwgbXNnLnBvc1syXSwKICAgICAgICAgICAgbXNnLnZlbG9jaXR5WzBdLCBtc2cudmVsb2NpdHlbMV0sIG1zZy52ZWxvY2l0eVsyXSwKICAgICAgICAgICAgMS4wKm1zZy5tYWduaXR1ZGUsIDEuMCptc2cudmVsb2NpdHlfbWFnbml0dWRlLCBtc2cucmFkaXVzLCAwLAogICAgICAgICAgICBtc2cuZm9yY2VfZGlyZWN0aW9uWzBdLCBtc2cuZm9yY2VfZGlyZWN0aW9uWzFdLCBtc2cuZm9yY2VfZGlyZWN0aW9uWzJdCiAgICAgICAgICAgICkKCiAgICAgICAgZWxpZiBpc2luc3RhbmNlKG1zZywgVG91Y2hlZFNwYXopOgogICAgICAgICAgICBub2RlID0gYmEuZ2V0Y29sbGlzaW9uKCkub3Bwb3Npbmdub2RlCiAgICAgICAgICAgIGlmIG5vZGUgYW5kIG5vZGUuZXhpc3RzKCk6CiAgICAgICAgICAgICAgICBub2RlLmhhbmRsZW1lc3NhZ2UoCiAgICAgICAgICAgICAgICAgICAgYmEuSGl0TWVzc2FnZShwb3MgPSBzZWxmLm5vZGUucG9zaXRpb24sCiAgICAgICAgICAgICAgICAgICAgdmVsb2NpdHkgPSAoMTAsIDEwLCAxMCksCiAgICAgICAgICAgICAgICAgICAgbWFnbml0dWRlID0gNTAsCiAgICAgICAgICAgICAgICAgICAgdmVsb2NpdHlfbWFnbml0dWRlID0gNTAsCiAgICAgICAgICAgICAgICAgICAgcmFkaXVzID0gMCwKICAgICAgICAgICAgICAgICAgICBzcmNub2RlID0gc2VsZi5ub2RlLAogICAgICAgICAgICAgICAgICAgIHNvdXJjZV9wbGF5ZXIgPSBzZWxmLnNvdXJjZV9wbGF5ZXIsCiAgICAgICAgICAgICAgICAgICAgZm9yY2VfZGlyZWN0aW9uID0gc2VsZi5ub2RlLnZlbG9jaXR5KQogICAgICAgICAgICAgICAgICAgICkKICAgICAgICAgICAgc2VsZi5ub2RlLmhhbmRsZW1lc3NhZ2UoYmEuRGllTWVzc2FnZSgpKQogICAgICAgIAogICAgICAgIGVsaWYgaXNpbnN0YW5jZShtc2csIFRvdWNoZWRGb290aW5nTWF0ZXJpYWwpOgogICAgICAgICAgICBiYS5wbGF5c291bmQoc291bmQgPSBiYS5nZXRzb3VuZCgiYmxpcCIpLCBwb3NpdGlvbiA9IHNlbGYubm9kZS5wb3NpdGlvbik="))

class Player(ba.Player['Team']):
    """Our player type for this game."""


class Team(ba.Team[Player]):
    """Our team type for this game."""

    def __init__(self) -> None:
        self.score = 0


# ba_meta export game
class FireBallGame(ba.TeamGameActivity[Player, Team]):
    """A game type based on acquiring kills."""

    name = 'FireBall Fight'
    description = 'Kill a set number of enemies with fire balls to win.'

    # Print messages when players die since it matters here.
    announce_player_deaths = True

    @classmethod
    def get_available_settings(
            cls, sessiontype: type[ba.Session]) -> list[ba.Setting]:
        settings = [
            ba.IntSetting(
                'Kills to Win Per Player',
                min_value=1,
                default=5,
                increment=1,
            ),
            ba.IntChoiceSetting(
                'Time Limit',
                choices=[
                    ('None', 0),
                    ('1 Minute', 60),
                    ('2 Minutes', 120),
                    ('5 Minutes', 300),
                    ('10 Minutes', 600),
                    ('20 Minutes', 1200),
                ],
                default=0,
            ),
            ba.FloatChoiceSetting(
                'Respawn Times',
                choices=[
                    ('Shorter', 0.25),
                    ('Short', 0.5),
                    ('Normal', 1.0),
                    ('Long', 2.0),
                    ('Longer', 4.0),
                ],
                default=1.0,
            ),
            ba.BoolSetting('Epic Mode', default=False),
            ba.BoolSetting("Equip Gloves", default = False),
            ba.BoolSetting("NightMode", default = True)
        ]

        # In teams mode, a suicide gives a point to the other team, but in
        # free-for-all it subtracts from your own score. By default we clamp
        # this at zero to benefit new players, but pro players might like to
        # be able to go negative. (to avoid a strategy of just
        # suiciding until you get a good drop)
        if issubclass(sessiontype, ba.FreeForAllSession):
            settings.append(
                ba.BoolSetting('Allow Negative Scores', default=False))

        return settings

    @classmethod
    def supports_session_type(cls, sessiontype: type[ba.Session]) -> bool:
        return (issubclass(sessiontype, ba.DualTeamSession)
                or issubclass(sessiontype, ba.FreeForAllSession))

    @classmethod
    def get_supported_maps(cls, sessiontype: type[ba.Session]) -> list[str]:
        return ba.getmaps('melee')

    def __init__(self, settings: dict):
        super().__init__(settings)
        self._scoreboard = Scoreboard()
        self._score_to_win: Optional[int] = None
        self._dingsound = ba.getsound('dingSmall')
        self._epic_mode = bool(settings['Epic Mode'])
        self._night = bool(settings["NightMode"])
        self._gloves = bool(settings["Equip Gloves"])
        self._kills_to_win_per_player = int(
            settings['Kills to Win Per Player'])
        self._time_limit = float(settings['Time Limit'])
        self._allow_negative_scores = bool(
            settings.get('Allow Negative Scores', False))

        # Base class overrides.
        self.slow_motion = self._epic_mode
        self.default_music = (ba.MusicType.EPIC if self._epic_mode else
                              ba.MusicType.TO_THE_DEATH)

    def get_instance_description(self) -> Union[str, Sequence]:
        return 'Crush ${ARG1} of your enemies.', self._score_to_win

    def get_instance_description_short(self) -> Union[str, Sequence]:
        return 'kill ${ARG1} enemies', self._score_to_win

    def on_team_join(self, team: Team) -> None:
        if self.has_begun():
            self._update_scoreboard()

    def on_begin(self) -> None:
        super().on_begin()
        if self._night: ba.getactivity().globalsnode.tint = (0.3, 0.3, 0.3)
        self.setup_standard_time_limit(self._time_limit)
        self.setup_standard_powerup_drops()

        # Base kills needed to win on the size of the largest team.
        self._score_to_win = (self._kills_to_win_per_player *
                              max(1, max(len(t.players) for t in self.teams)))
        self._update_scoreboard()

    def spawn_player(self, player: Player) -> ba.Actor:
        spaz = self.spawn_player_spaz(player)
        FireBallFactory().grant_fire_ball(spaz)
        spaz.connect_controls_to_player(enable_punch=True,
                                        enable_bomb=False,
                                        enable_pickup=True)
        if self._gloves: spaz.equip_boxing_gloves()

    def handlemessage(self, msg: Any) -> Any:

        if isinstance(msg, ba.PlayerDiedMessage):

            # Augment standard behavior.
            super().handlemessage(msg)

            player = msg.getplayer(Player)
            self.respawn_player(player)

            killer = msg.getkillerplayer(Player)
            if killer is None:
                return None

            # Handle team-kills.
            if killer.team is player.team:

                # In free-for-all, killing yourself loses you a point.
                if isinstance(self.session, ba.FreeForAllSession):
                    new_score = player.team.score - 1
                    if not self._allow_negative_scores:
                        new_score = max(0, new_score)
                    player.team.score = new_score

                # In teams-mode it gives a point to the other team.
                else:
                    ba.playsound(self._dingsound)
                    for team in self.teams:
                        if team is not killer.team:
                            team.score += 1

            # Killing someone on another team nets a kill.
            else:
                killer.team.score += 1
                ba.playsound(self._dingsound)

                # In FFA show scores since its hard to find on the scoreboard.
                if isinstance(killer.actor, PlayerSpaz) and killer.actor:
                    killer.actor.set_score_text(str(killer.team.score) + '/' +
                                                str(self._score_to_win),
                                                color=killer.team.color,
                                                flash=True)

            self._update_scoreboard()

            # If someone has won, set a timer to end shortly.
            # (allows the dust to clear and draws to occur if deaths are
            # close enough)
            assert self._score_to_win is not None
            if any(team.score >= self._score_to_win for team in self.teams):
                ba.timer(0.5, self.end_game)

        else:
            return super().handlemessage(msg)
        return None

    def _update_scoreboard(self) -> None:
        for team in self.teams:
            self._scoreboard.set_team_value(team, team.score,
                                            self._score_to_win)

    def end_game(self) -> None:
        results = ba.GameResults()
        for team in self.teams:
            results.set_team_score(team, team.score)
        self.end(results=results)
