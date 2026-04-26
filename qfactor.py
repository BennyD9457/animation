from manim import *
import numpy as np

class BouncingInBox(Scene):
    def construct(self):
        wall = 1.0

        def make_updater(s, w, life, boundary="square"):
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

                if boundary == "circle":
                    dist = np.sqrt(s["x"]**2 + s["y"]**2)
                    if dist >= wall:
                        # reflect off circular wall
                        nx, ny = s["x"] / dist, s["y"] / dist
                        dot = s["vx"] * nx + s["vy"] * ny
                        s["vx"] -= 2 * dot * nx
                        s["vy"] -= 2 * dot * ny
                        s["x"] = nx * wall * 0.99
                        s["y"] = ny * wall * 0.99
                        w.rotate(90 * DEGREES)
                else:
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

        def spawn_waves(life, count=10, boundary="square"):
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
                wave.add_updater(make_updater(state, wave, life, boundary))
                self.add(wave)
                waves.append(wave)
            return waves

        # --- HIGH Q (Circle) ---
        circleCav = Circle(radius=2, color=ORANGE)
        circleCav.set_fill(WHITE, opacity=0.1)
        self.add(circleCav)

        title = Text("High Q Factor", font_size=48, color=GREEN).to_edge(UP)
        self.play(Write(title))
        waves1 = spawn_waves(life=5, boundary="circle")
        self.wait(1)
        for w in waves1:
            w.clear_updaters()
            self.remove(w)
        self.play(FadeOut(title))

        # --- Transition: circle → square ---
        squareCav = Square(side_length=4, color=ORANGE)
        squareCav.set_fill(WHITE, opacity=0.1)
        self.play(ReplacementTransform(circleCav, squareCav))

        # --- LOW Q (Square) ---
        title2 = Text("Low Q Factor", font_size=48, color=RED).to_edge(UP)
        self.play(Write(title2))
        waves2 = spawn_waves(life=1, boundary="square")
        self.wait(1)
        for w in waves2:
            w.clear_updaters()
            self.remove(w)
        self.play(FadeOut(title2))