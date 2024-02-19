import ba
import random

# In snowfall.py
class SnowfallActivity(ba.Activity):
    def __init__(self, player=None, team=None, settings=None):
        super().__init__(settings=settings)
        # Your initialization code here


    def on_transition_in(self):
        super().on_transition_in()
        # Start snowfall effect when the activity transitions in
        self.snowfall_timer = ba.Timer(20, self._snowfall_tick, repeat=True)

    def _snowfall_tick(self):
        # Generate random position for snowfall
        p = (-10 + (random.random() * 30), 15, -10 + (random.random() * 30))
        # Generate random velocity for snowfall
        v = ((-5.0 + random.random() * 30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0, (-5.0 + random.random() * 30.0) * (-1.0 if p[0] > 0 else 1.0))
        # Emit snowfall effects
        ba.emitfx(position=p, velocity=v, count=10, scale=1 + random.random(), spread=0, chunk_type="spark")

# Entry point for the snowfall effect
def start_snowfall():
    # Start the snowfall activity directly within the HockeyStadium class
    SnowfallActivity()

