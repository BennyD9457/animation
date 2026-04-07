from manim import *
import numpy as np

class CavitySineWave(Scene):
    def construct(self):
        title = Text("How Cavity Modes Form", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        # ── Wire → Cavity transition (your original idea) ───────────
        wire = Line(start=UP * 2, end=DOWN * 2, color=ORANGE, stroke_width=3)
        self.play(Create(wire))
        self.wait(0.5)

        cavity = Rectangle(width=5, height=4, stroke_width=8, color=ORANGE)
        cavity.shift(LEFT * 4 + DOWN * 0.3)
        self.play(Transform(wire, cavity), run_time=2)

        conductor_label = Text("Conducting Cavity Wall", font_size=20, color=ORANGE)
        conductor_label.next_to(cavity, DOWN, buff=0.2)
        self.play(FadeIn(conductor_label))
        self.wait(1)
        self.play(FadeOut(conductor_label))

        # ── Slide 1: Random CIRCLES (representing E-field) ──────────
        self.play(Transform(title, Text("Electric Field (random)", font_size=36).to_edge(UP)))

        e_dots = VGroup()
        # store random sizes so we can reference them later
        e_sizes = {}
        for x in np.linspace(-2, 2, 7):
            for y in np.linspace(-1.6, 1.6, 7):
                rand_size = np.random.uniform(0.03, 0.18)
                pos = cavity.get_center() + np.array([x, y, 0])
                dot = Dot(point=pos, radius=rand_size, color=TEAL_B)
                e_dots.add(dot)
                e_sizes[(x, y)] = rand_size

        self.play(FadeIn(e_dots, lag_ratio=0.02), run_time=2)
        self.wait(1.5)

        # ── Slide 2: Random ARROWS (representing B-field) ───────────
        # Shift cavity copy to the right for side-by-side
        cavity2 = Rectangle(width=5, height=4, stroke_width=8, color=ORANGE)
        cavity2.shift(RIGHT * 3 + DOWN * 0.3)

        self.play(
            Transform(title, Text("Magnetic Field (random)", font_size=36).to_edge(UP)),
            Create(cavity2),
            run_time=1.5,
        )

        b_arrows = VGroup()
        b_sizes = {}
        for x in np.linspace(-2, 2, 7):
            for y in np.linspace(-1.6, 1.6, 7):
                rand_len = np.random.uniform(0.1, 0.45)
                pos = cavity2.get_center() + np.array([x, y, 0])
                arr = Arrow(
                    start=pos,
                    end=pos + UP * rand_len,
                    buff=0, color=YELLOW, stroke_width=1.5,
                    max_tip_length_to_length_ratio=0.5,
                )
                b_arrows.add(arr)
                b_sizes[(x, y)] = rand_len

        self.play(FadeIn(b_arrows, lag_ratio=0.02), run_time=2)
        self.wait(1.5)

        # ── Slide 3: COMBINE — move both into one cavity ────────────
        self.play(
            Transform(title, Text("Combined: Where are both strongest?", font_size=34).to_edge(UP)),
        )

        # fade out the second cavity box, move arrows into first cavity
        shift_vec = cavity.get_center() - cavity2.get_center()
        self.play(
            FadeOut(cavity2),
            b_arrows.animate.shift(shift_vec),
            run_time=1.5,
        )
        self.wait(1)

        # ── Highlight the spots where BOTH are biggest ──────────────
        highlights = VGroup()
        threshold_e = 0.12   # only big dots
        threshold_b = 0.30   # only big arrows

        for x in np.linspace(-2, 2, 7):
            for y in np.linspace(-1.6, 1.6, 7):
                es = e_sizes.get((x, y), 0)
                bs = b_sizes.get((x, y), 0)
                if es > threshold_e and bs > threshold_b:
                    pos = cavity.get_center() + np.array([x, y, 0])
                    ring = Circle(radius=0.3, color=GREEN, stroke_width=3)
                    ring.move_to(pos)
                    highlights.add(ring)

        # if no spots pass both thresholds, just highlight the biggest combo
        if len(highlights) == 0:
            best_score = 0
            best_pos = cavity.get_center()
            for x in np.linspace(-2, 2, 7):
                for y in np.linspace(-1.6, 1.6, 7):
                    score = e_sizes.get((x, y), 0) + b_sizes.get((x, y), 0)
                    if score > best_score:
                        best_score = score
                        best_pos = cavity.get_center() + np.array([x, y, 0])
            ring = Circle(radius=0.3, color=GREEN, stroke_width=3)
            ring.move_to(best_pos)
            highlights.add(ring)

        self.play(Create(highlights), run_time=1.5)

        callout = Text("← Mode lives here!", font_size=24, color=GREEN)
        callout.next_to(highlights, RIGHT, buff=0.3)
        self.play(FadeIn(callout))
        self.wait(2)

        # ── Slide 4: Transition to real mode map ────────────────────
        self.play(
            FadeOut(e_dots), FadeOut(b_arrows), FadeOut(highlights),
            FadeOut(callout), FadeOut(cavity2),
            run_time=1,
        )
        self.play(
            Transform(title, Text("The Real Mode Map", font_size=42).to_edge(UP)),
        )

        # Placeholder for your actual mode map image
        # Replace "mode_map.png" with your real file
        placeholder = Text(
            "[ Insert your mode map image here ]\n"
            "e.g. ImageMobject('mode_map.png')",
            font_size=22, color=GREY_B,
        )
        placeholder.move_to(cavity.get_center())
        self.play(FadeIn(placeholder))
        self.wait(3)