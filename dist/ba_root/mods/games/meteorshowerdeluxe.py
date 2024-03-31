# ba_meta require api 7

import random
import ba
from bastd.game.meteorshower import MeteorShowerGame
from bastd.actor.bomb import Bomb


class NewMeteorShowerGame(MeteorShowerGame):
    @classmethod
    def get_supported_maps(cls, sessiontype: type[ba.Session]) -> list[str]:
        return ba.getmaps('melee')

    def _drop_bomb_cluster(self) -> None:
        # Drop several bombs in series.
        delay = 0.0
        bounds = list(self._map.get_def_bound_box('map_bounds'))
        for _i in range(random.randrange(1, 3)):
            # Drop them somewhere within our bounds with velocity pointing
            # toward the opposite side.
            pos = (
                random.uniform(bounds[0], bounds[3]),
                bounds[4],
                random.uniform(bounds[2], bounds[5]),
            )
            dropdirx = -1 if pos[0] > 0 else 1
            dropdirz = -1 if pos[2] > 0 else 1
            forcex = bounds[0] - bounds[3] if bounds[0] - bounds[3] > 0 else -(bounds[0] - bounds[3])
            forcez = bounds[2] - bounds[5] if bounds[2] - bounds[5] > 0 else -(bounds[2] - bounds[5])
            vel = (
                (-5 + random.random() * forcex) * dropdirx,
                random.uniform(-3.066, -4.12),
                (-5 + random.random() * forcez) * dropdirz,
            )
            ba.timer(delay, ba.Call(self._drop_bomb, pos, vel))
            delay += 0.1
        self._set_meteor_timer()


# ba_meta export plugin
class byEra0S(ba.Plugin):
    MeteorShowerGame.get_supported_maps = NewMeteorShowerGame.get_supported_maps
    MeteorShowerGame._drop_bomb_cluster = NewMeteorShowerGame._drop_bomb_cluster
