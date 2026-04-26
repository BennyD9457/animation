from manim import *
import numpy as np


class Resonance(Scene):

    # ══════════════════════════════════════════════════════════════
    #  HELPERS
    # ══════════════════════════════════════════════════════════════

    def _make_noisy_trace(self, y_center, x_left, x_right,
                          amplitude=0.05, freq=30, noise=0.05,
                          n_points=300, seed=0):
        rng = np.random.default_rng(seed)
        xs = np.linspace(x_left, x_right, n_points)
        ys = (y_center
              + amplitude * np.sin(freq * (xs - x_left))
              + noise * rng.standard_normal(n_points))
        return [np.array([x, y, 0]) for x, y in zip(xs, ys)]

    def _make_pulse(self, color=WHITE, radius=0.12):
        inner = Dot(radius=radius, color=color, fill_opacity=1)
        outer = Dot(radius=radius * 2, color=color, fill_opacity=0.25)
        return VGroup(outer, inner)

    # ══════════════════════════════════════════════════════════════
    #  BUILD ALL MOBJECTS (called once, stored on self)
    # ══════════════════════════════════════════════════════════════

    def _build(self):
        # ── Title ─────────────────────────────────────────────
        self.title = Text("Set Up", font_size=48, color=WHITE).to_edge(UP)

        # ── VNA ───────────────────────────────────────────────
        self.vna = Rectangle(width=4, height=4, stroke_width=8, color=WHITE)
        self.vna.shift(LEFT * 3 + DOWN * 0.8)
        self.vna_label = Text("VNA", font_size=24).next_to(self.vna, UP, buff=0.1)

        self.center_line = Line(
            self.vna.get_left(), self.vna.get_right(),
            stroke_width=4, color=WHITE,
        )
        self.s11_label = Text("S11", font_size=15, color=BLUE)\
            .next_to(self.center_line, UP, buff=0.05).shift(LEFT * 0.9)
        self.s21_label = Text("S21", font_size=15, color=BLUE)\
            .next_to(self.center_line, DOWN, buff=0.05).shift(LEFT * 0.9)

        # ── Cavity ────────────────────────────────────────────
        self.cavity = Rectangle(width=5, height=2, stroke_width=8, color=ORANGE)
        self.cavity.shift(RIGHT * 3 + DOWN * 0.5)
        self.cavity_label = Text("Cavity", font_size=24, color=ORANGE)\
            .next_to(self.cavity, UP, buff=0.1)

        # ── Cables ────────────────────────────────────────────
        self.s1_start = self.vna.get_right() + UP * 0.4
        self.s1_end   = self.cavity.get_left()
        self.s1       = Line(self.s1_start, self.s1_end, stroke_width=4, color=YELLOW)
        self.s1_label = Text("S1", font_size=20, color=YELLOW)\
            .next_to(self.s1, UP, buff=0.1)

        self.s2_start = self.vna.get_right() + DOWN * 0.4
        self.s2_end   = self.cavity.get_left() + DOWN * 0.8
        self.s2       = Line(self.s2_start, self.s2_end, stroke_width=4, color=BLUE)
        self.s2_label = Text("S2", font_size=20, color=BLUE)\
            .next_to(self.s2, DOWN, buff=0.1)

        self.s1_return = Line(self.s1_end, self.s1_start)
        self.s2_return = Line(self.s2_end, self.s2_start)

        # ── VNA traces ────────────────────────────────────────
        x_left  = self.vna.get_left()[0] + 0.15
        x_right = self.vna.get_right()[0] - 0.15
        y_top   = (self.center_line.get_center()[1] + self.vna.get_top()[1]) / 2
        y_bot   = (self.center_line.get_center()[1] + self.vna.get_bottom()[1]) / 2

        self.s11_trace = VMobject(stroke_width=2, color=YELLOW)
        self.s11_trace.set_points_as_corners(
            self._make_noisy_trace(y_top, x_left, x_right, seed=1)
        )
        self.s21_trace = VMobject(stroke_width=2, color=BLUE)
        self.s21_trace.set_points_as_corners(
            self._make_noisy_trace(y_bot, x_left, x_right, seed=2)
        )

        # ── Pulses ────────────────────────────────────────────
        self.pulse_off = self._make_pulse(color=YELLOW)
        self.pulse_on  = self._make_pulse(color=YELLOW)

        # ── Captions ──────────────────────────────────────────
        self.caption_off = Text(
            "Off resonance: signal reflects back",
            font_size=24, color=WHITE,
        ).to_edge(DOWN)
        self.caption_on = Text(
            "On resonance: signal passes through to S2",
            font_size=24, color=ORANGE,
        ).to_edge(DOWN)

    # ══════════════════════════════════════════════════════════════
    #  SECTIONS
    # ══════════════════════════════════════════════════════════════

    def section_setup(self):
        """Draw VNA, cavity, cables, labels."""
        self.play(Write(self.title))
        self.play(
            Create(self.vna), Create(self.cavity), Create(self.center_line),
            Write(self.vna_label), Write(self.cavity_label),
            Write(self.s11_label), Write(self.s21_label),
            run_time=2,
        )
        self.play(
            Create(self.s1), Write(self.s1_label),
            Create(self.s2), Write(self.s2_label),
            run_time=2,
        )
        self.wait(0.5)

    def section_off_resonance(self):
        """Pulse reflects back along S1 (off resonance)."""
        self.play(Write(self.caption_off))

        self.pulse_off.move_to(self.s1_start)
        self.add(self.pulse_off)

        # VNA → cavity
        self.play(MoveAlongPath(self.pulse_off, self.s1),
                  run_time=1.2, rate_func=linear)
        self.play(Flash(self.s1_end, color=ORANGE,
                        flash_radius=0.3, num_lines=12), run_time=0.4)
        # Bounce back
        self.play(MoveAlongPath(self.pulse_off, self.s1_return),
                  run_time=1.2, rate_func=linear)

        self.remove(self.pulse_off)
        self.play(Create(self.s11_trace), Create(self.s21_trace), run_time=2)
        self.wait(0.5)

    def section_on_resonance(self):
        """Pulse passes through cavity and exits via S2."""
        self.play(Transform(self.caption_off, self.caption_on))
        

        self.pulse_on.move_to(self.s1_start)
        self.add(self.pulse_on)




        # VNA → cavity
        self.play(MoveAlongPath(self.pulse_on, self.s1),
                  run_time=1.2, rate_func=linear)
        
        self.wait(1)
        # Cavity lights up
        self.play(
            self.cavity.animate.set_stroke(color=YELLOW, width=12),
            run_time=0.1,
        )
        
        
        # Rattle inside cavity
        self.play(self.pulse_on.animate.scale(1.5), run_time=0.3)
        self.play(self.pulse_on.animate.scale(1 / 1.5), run_time=0.3)
        # Cavity → VNA via S2
        self.pulse_on.move_to(self.s2_end)
        self.play(MoveAlongPath(self.pulse_on, self.s2_return),
                  run_time=1.2, rate_func=linear)

        self.remove(self.pulse_on)

        # Restore cavity
        self.play(
            self.cavity.animate.set_stroke(color=ORANGE, width=8),
            run_time=0.4,
        )
        self.wait(2)

    # ══════════════════════════════════════════════════════════════
    #  PLAY ORDER — rearrange / comment out here
    # ══════════════════════════════════════════════════════════════

    def construct(self):
        self._build()

        self.section_setup()            # 1 — draw VNA + cavity + cables
        self.section_off_resonance()    # 2 — pulse bounces back
        self.section_on_resonance()     # 3 — pulse passes through
        # self.section_next_thing()     # 4 — add more here …