from manim import *
import numpy as np

class BouncingInBox(Scene):
    def construct(self):
        cavity = Square(side_length=4, color=ORANGE)
        cavity.set_fill(WHITE, opacity=0.1)

        rod = Rectangle(width=0.3, height=0.7, color=ORANGE)
        rod.set_fill(WHITE, opacity=0.1)
        rod.align_to(cavity, UP)
        rod.shift(RIGHT * 0.2)

        self.add(cavity, rod)

        for i in range(5):
            wave = FunctionGraph(
                lambda x: 1/4* np.sin(50 * x),
                x_range=[-.25, .25, 0.001],
                color=BLUE,
                stroke_opacity=0.5,
            )
            wave.rotate(90 * DEGREES)

            # Random starting position and velocity for each wave
            state = {
                "x": np.random.uniform(-0.8, 0.8),
                "y": np.random.uniform(-0.8, 0.8),
                "vx": np.random.uniform(-3, 3),
                "vy": np.random.uniform(-3, 3),
            }
            wall = 1.0

            def make_updater(s, w):
                def update(mob, dt):
                    s["x"] += s["vx"] * dt
                    s["y"] += s["vy"] * dt

                    if s["x"] >= wall:
                        w.rotate(90 * DEGREES)
                        s["x"] = wall
                        s["vx"] *= -1
                    elif s["x"] <= -wall:
                        w.rotate(90 * DEGREES)
                        s["x"] = -wall
                        s["vx"] *= -1

                    if s["y"] >= wall:
                        w.rotate(90 * DEGREES)
                        s["y"] = wall
                        s["vy"] *= -1
                    elif s["y"] <= -wall:
                        w.rotate(90 * DEGREES)
                        s["y"] = -wall
                        s["vy"] *= -1

                    mob.move_to([s["x"], s["y"], 0])
                return update

            wave.add_updater(make_updater(state, wave))
            self.add(wave)

        self.wait(10)