from manim import *
import numpy as np

class BouncingInBox(Scene):
    def construct(self):
        cavity = Square(side_length=4, color=ORANGE)
        cavity.set_fill(WHITE, opacity=0.1)
        self.add(cavity)

        wall = 1.0

        def make_updater(s, w, life):
            s["life"] = life
            s["max_life"] = life
            def update(mob, dt):
                s["life"] -= dt
                if s["life"] <= 0:
                    mob.set_opacity(0)
                    return
                mob.set_stroke(opacity=s["life"] / s["max_life"])
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

        def spawn_waves(life, count=10):
            waves = []
            for i in range(count):
                wave = FunctionGraph(
                    lambda x: 1/4 * np.sin(50 * x),
                    x_range=[-0.25, 0.25, 0.001],
                    color=BLUE,
                    stroke_opacity=0.5,
                )
                wave.rotate(90 * DEGREES)
                state = {
                    "x": np.random.uniform(-0.8, 0.8),
                    "y": np.random.uniform(-0.8, 0.8),
                    "vx": np.random.uniform(-3, 3),
                    "vy": np.random.uniform(-3, 3),
                }
                wave.add_updater(make_updater(state, wave, life))
                self.add(wave)
                waves.append(wave)
            return waves

        # HIGH Q
        title = Text("High Q Factor", font_size=48, color=GREEN).to_edge(UP)
        self.play(Write(title))
        waves1 = spawn_waves(life=5)
        self.wait(6)

        # Clean up
        for w in waves1:
            w.clear_updaters()
            self.remove(w)
        self.play(FadeOut(title))

        # LOW Q
        title2 = Text("Low Q Factor", font_size=48, color=RED).to_edge(UP)
        self.play(Write(title2))
        waves2 = spawn_waves(life=1)
        self.wait(3)

        for w in waves2:
            w.clear_updaters()
            self.remove(w)
        self.play(FadeOut(title2))