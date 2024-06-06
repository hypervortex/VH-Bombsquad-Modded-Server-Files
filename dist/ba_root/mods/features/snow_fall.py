import random
import ba

def snowfall_generator(activity, count=10, fall_speed=0.1, scale=0.3):
    def generate_snowfall():
        for _ in range(count):
            p = (-10 + (random.random() * 30), 15, -10 + (random.random() * 30))
            v = ((-5.0 + random.random() * 30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0 * fall_speed,
                 (-5.0 + random.random() * 30.0) * (-1.0 if p[0] > 0 else 1.0) * fall_speed)
            snowfall = ba.emitfx(position=p,
                                  velocity=v,
                                  count=10,
                                  scale=scale + random.random() * 0.1,  # Random scale between scale and scale + 0.1
                                  spread=0.0,
                                  chunk_type='ice')  # Emit particles that stick to surfaces
            if snowfall is not None:
                # Add a timer to delete the snowfall particles after falling
                ba.timer(random.uniform(1.0, 3.0), snowfall.delete)
                activity.snowfall_particles.append(snowfall)

    # Generate snowfall continuously
    ba.timer(0.3, generate_snowfall, repeat=True)

# Attach the snowfall_generator function to the Activity class
ba._activity.Activity.snowfall_generator = snowfall_generator
