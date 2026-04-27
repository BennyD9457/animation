from manim import *
import numpy as np


class Resonance(Scene):

    # ══════════════════════════════════════════════════════════════
    #  TRACE HELPERS
    # ══════════════════════════════════════════════════════════════

    def _make_noisy_trace(self, y_center, x_left, x_right,
                          baseline=0.0,
                          amplitude=0.05, freq=30, noise=0.05,
                          n_points=300, seed=0):
        rng = np.random.default_rng(seed)
        xs = np.linspace(x_left, x_right, n_points)
        ys = (y_center + baseline
              + amplitude * np.sin(freq * (xs - x_left))
              + noise * rng.standard_normal(n_points))
        return [np.array([x, y, 0]) for x, y in zip(xs, ys)]

    def _make_lorentzian_trace(self, y_center, x_left, x_right,
                               peak_x,
                               baseline=0.0,
                               peak_sign=+1,
                               peak_height=0.6, hwhm=0.15,
                               noise=0.015, n_points=400, seed=0):
        """
        peak_height = 0  →  flat baseline (no resonance feature)
        peak_sign   = +1 →  upward peak (S21 transmission)
        peak_sign   = -1 →  downward dip (S11 reflection)
        """
        rng = np.random.default_rng(seed)
        xs = np.linspace(x_left, x_right, n_points)
        lorentz = peak_sign * peak_height * (hwhm ** 2) / ((xs - peak_x) ** 2 + hwhm ** 2)
        ys = y_center + baseline + lorentz + noise * rng.standard_normal(n_points)
        return [np.array([x, y, 0]) for x, y in zip(xs, ys)]

    # ══════════════════════════════════════════════════════════════
    #  PORT CONFIG — change S11/S21 visuals from one place
    # ══════════════════════════════════════════════════════════════
    S11_BASELINE  = +0.5
    S21_BASELINE  = -0.5
    S11_PEAK_SIGN = -1
    S21_PEAK_SIGN = +1
    PEAK_HEIGHT_MAX = 0.55     # default "full" peak/dip amplitude

    # ══════════════════════════════════════════════════════════════
    #  GENERAL HELPERS
    # ══════════════════════════════════════════════════════════════

    def _make_pulse(self, color=WHITE, radius=0.12):
        inner = Dot(radius=radius, color=color, fill_opacity=1)
        outer = Dot(radius=radius * 2, color=color, fill_opacity=0.25)
        return VGroup(outer, inner)

    def _polyline(self, points, color, stroke_width=4):
        m = VMobject(stroke_width=stroke_width, color=color)
        m.set_points_as_corners([np.array([p[0], p[1], 0]) for p in points])
        return m

    # ══════════════════════════════════════════════════════════════
    #  SINGLE TRACE FACTORY  ←  was two functions before
    # ══════════════════════════════════════════════════════════════

    def _new_trace_at(self, port, peak_x, amplitude):
        """
        Build a trace for the named port with a Lorentzian feature.
            port:      'S11' or 'S21'
            peak_x:    x-position of the peak/dip in scene coords
            amplitude: peak height (0 = flat trace, no feature)
        """
        if port == "S21":
            y_center  = self.trace_y_bot
            baseline  = self.S21_BASELINE
            peak_sign = self.S21_PEAK_SIGN
            color, seed = BLUE, 2
        elif port == "S11":
            y_center  = self.trace_y_top
            baseline  = self.S11_BASELINE
            peak_sign = self.S11_PEAK_SIGN
            color, seed = YELLOW, 1
        else:
            raise ValueError(f"unknown port {port!r}")

        new = VMobject(stroke_width=2, color=color)
        new.set_points_as_corners(
            self._make_lorentzian_trace(
                y_center, self.trace_x_left, self.trace_x_right,
                peak_x=peak_x,
                baseline=baseline,
                peak_sign=peak_sign,
                peak_height=amplitude, hwhm=0.12, seed=seed,
            )
        )
        return new

    # ══════════════════════════════════════════════════════════════
    #  BUILD
    # ══════════════════════════════════════════════════════════════

    def _build(self):
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
        self.cavity = Rectangle(width=2, height=5, stroke_width=8, color=ORANGE)
        self.cavity.shift(RIGHT * 3 + DOWN * 0.5)
        self.cavity_label = Text("Cavity", font_size=24, color=ORANGE)\
            .next_to(self.cavity, UP, buff=0.1)

        # ── Tuning rod ────────────────────────────────────────
        self.rod_height_full = 4.5
        self.rod = Rectangle(
            width=0.18, height=0.4,
            stroke_width=2, color=GRAY_B,
        )
        self.rod.set_fill(GRAY_B, opacity=1)
        cav_bottom_y = self.cavity.get_bottom()[1]
        rod_x = self.cavity.get_center()[0] + 0.3
        self.rod.move_to([rod_x, cav_bottom_y + self.rod.height / 2, 0])
        self.rod_label = Text("Tuning Rod", font_size=18, color=GRAY_B)\
            .next_to(self.cavity, DOWN, buff=0.2)

        # ── Cable routing ─────────────────────────────────────
        vna_right_x  = self.vna.get_right()[0]
        cavity_top_y = self.cavity.get_top()[1]
        rise_y = cavity_top_y + 0.2

        s1_exit_y = self.vna.get_center()[1] + 0.5
        s1_cav_x  = self.cavity.get_center()[0] - 0.4
        s1_rise   = rise_y + 0.1
        self.s1_start = np.array([vna_right_x, s1_exit_y, 0])
        self.s1_end   = np.array([s1_cav_x, cavity_top_y, 0])
        s1_pts = [
            self.s1_start,
            (vna_right_x + 0.3, s1_exit_y),
            (vna_right_x + 0.3, s1_rise),
            (s1_cav_x, s1_rise),
            self.s1_end,
        ]
        self.s1 = self._polyline(s1_pts, color=YELLOW)
        self.s1_label = Text("S1", font_size=20, color=YELLOW)\
            .move_to([(vna_right_x + 0.3 + s1_cav_x) / 2, s1_rise + 0.3, 0])

        s2_exit_y = self.vna.get_center()[1] - 0.5
        s2_cav_x  = self.cavity.get_center()[0] + 0.4
        s2_rise   = rise_y - 0.07
        self.s2_start = np.array([vna_right_x, s2_exit_y, 0])
        self.s2_end   = np.array([s2_cav_x, cavity_top_y, 0])
        s2_pts = [
            self.s2_start,
            (vna_right_x + 0.7, s2_exit_y),
            (vna_right_x + 0.7, s2_rise),
            (s2_cav_x, s2_rise),
            self.s2_end,
        ]
        self.s2 = self._polyline(s2_pts, color=BLUE)
        self.s2_label = Text("S2", font_size=20, color=BLUE)\
            .move_to([(vna_right_x + 0.7 + s2_cav_x) / 2, s2_rise - 0.3, 0])

        self.s1_return = self._polyline(list(reversed(s1_pts)), color=YELLOW)
        self.s2_return = self._polyline(list(reversed(s2_pts)), color=BLUE)

        # ── VNA traces (initial: dead/wavy, no peaks) ─────────
        self.trace_x_left  = self.vna.get_left()[0] + 0.15
        self.trace_x_right = self.vna.get_right()[0] - 0.15
        self.trace_y_top = (self.center_line.get_center()[1] + self.vna.get_top()[1]) / 2
        self.trace_y_bot = (self.center_line.get_center()[1] + self.vna.get_bottom()[1]) / 2

        self.s11_trace = VMobject(stroke_width=2, color=YELLOW)
        self.s11_trace.set_points_as_corners(
            self._make_noisy_trace(
                self.trace_y_top, self.trace_x_left, self.trace_x_right,
                baseline=self.S11_BASELINE, seed=1,
            )
        )
        self.s21_trace = VMobject(stroke_width=2, color=BLUE)
        self.s21_trace.set_points_as_corners(
            self._make_noisy_trace(
                self.trace_y_bot, self.trace_x_left, self.trace_x_right,
                baseline=self.S21_BASELINE, seed=2,
            )
        )

        # Default peak position used by section_on_resonance
        self.s21_peak_x_min = self.trace_x_left + 0.4
        self.s21_peak_x_max = self.trace_x_right - 0.4
        self.peak_x = self.s21_peak_x_min

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
        self.caption_scan = Text(
            "Tuning rod shifts cavity resonance",
            font_size=24, color=GRAY_B,
        ).to_edge(DOWN)

    # ══════════════════════════════════════════════════════════════
    #  SECTIONS
    # ══════════════════════════════════════════════════════════════

    def section_setup(self):
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
        self.play(Create(self.s11_trace), Create(self.s21_trace), run_time=1.5)
        self.wait(0.5)

    def section_off_resonance(self):
        self.play(Write(self.caption_off))
        self.pulse_off.move_to(self.s1_start)
        self.add(self.pulse_off)

        self.play(MoveAlongPath(self.pulse_off, self.s1),
                  run_time=1.2, rate_func=linear)
        self.play(Flash(self.s1_end, color=ORANGE,
                        flash_radius=0.3, num_lines=12), run_time=0.4)
        self.play(MoveAlongPath(self.pulse_off, self.s1_return),
                  run_time=1.2, rate_func=linear)

        self.remove(self.pulse_off)
        self.wait(0.5)

    def section_on_resonance(self):
        self.play(Transform(self.caption_off, self.caption_on))
        self.pulse_on.move_to(self.s1_start)
        self.add(self.pulse_on)

        self.play(MoveAlongPath(self.pulse_on, self.s1),
                  run_time=1.2, rate_func=linear)
        self.wait(1)
        self.play(
            self.cavity.animate.set_stroke(color=YELLOW, width=12),
            run_time=0.1,
        )
        self.play(self.pulse_on.animate.scale(1.5), run_time=0.3)
        self.play(self.pulse_on.animate.scale(1 / 1.5), run_time=0.3)

        self.pulse_on.move_to(self.s2_end)
        self.play(MoveAlongPath(self.pulse_on, self.s2_return),
                  run_time=1.2, rate_func=linear)
        self.remove(self.pulse_on)

        self.play(
            self.cavity.animate.set_stroke(color=ORANGE, width=8),
            run_time=0.4,
        )

        # Resonance feature appears on both traces.
        s21_peaked = self._new_trace_at("S21", self.peak_x, amplitude=self.PEAK_HEIGHT_MAX)
        s11_dipped = self._new_trace_at("S11", self.peak_x, amplitude=self.PEAK_HEIGHT_MAX)
        self.play(
            Transform(self.s21_trace, s21_peaked),
            Transform(self.s11_trace, s11_dipped),
            run_time=1.2,
        )
        self.wait(2)

    # ══════════════════════════════════════════════════════════════
    #  SCAN PRIMITIVES — small, composable, do one thing
    # ══════════════════════════════════════════════════════════════

    def _move_rod_to(self, frac, run_time=0.3):
        """Move the rod to fractional insertion `frac` (0 = bottom, 1 = full)."""
        cav_bottom_y = self.cavity.get_bottom()[1]
        # new_height = 0.4 + #frac * (self.rod_height_full - 0.4)
        new_height = .4 + frac * (self.rod_height_full - 4 )
        new_center = [self.rod.get_center()[0],
                      cav_bottom_y + new_height / 2, 0]
        rod_target = self.rod.copy()
        rod_target.stretch_to_fit_height(new_height)
        rod_target.move_to(new_center)
        self.play(Transform(self.rod, rod_target), run_time=run_time)

    def _send_scan_pulse_and_update(self, s11_target, s21_target,
                                    s1_time=0.35, s2_time=0.45):
        """Pulse VNA → cavity → S2 → VNA. Traces morph during the return."""
        pulse = self._make_pulse(color=YELLOW)
        pulse.move_to(self.s1_start)
        self.add(pulse)

        self.play(MoveAlongPath(pulse, self.s1),
                  run_time=s1_time, rate_func=linear)
        self.play(self.cavity.animate.set_stroke(color=YELLOW, width=12),
                  run_time=0.08)
        self.play(
            MoveAlongPath(pulse, self.s2_return),
            Transform(self.s21_trace, s21_target),
            Transform(self.s11_trace, s11_target),
            run_time=s2_time, rate_func=linear,
        )
        self.play(self.cavity.animate.set_stroke(color=ORANGE, width=8),
                  run_time=0.08)
        self.remove(pulse)

    def _measure_at(self, peak_x, amplitude):
        """Take a measurement: send pulse, update both traces with new peak state."""
        s21_target = self._new_trace_at("S21", peak_x, amplitude)
        s11_target = self._new_trace_at("S11", peak_x, amplitude)
        self.peak_x = peak_x
        self._send_scan_pulse_and_update(s11_target, s21_target)

    def _scan_step(self, rod_frac, peak_x, amplitude):
        """One step: move rod, then measure."""
        self._move_rod_to(rod_frac)
        self._measure_at(peak_x, amplitude)

    # ══════════════════════════════════════════════════════════════
    #  ROD SCAN — driven by an editable plan
    # ══════════════════════════════════════════════════════════════

    def section_rod_scan(self):
        self.play(
            Transform(self.caption_off, self.caption_scan),
            FadeIn(self.rod),
            Write(self.rod_label),
            run_time=1.0,
        )
        self.wait(0.3)

        x1 = self.peak_x
        x2 = x1 + 1

        scan_plan = [
            # rod_frac, peak_x, amplitude
            (0.10,  x1, 0.55),
            (0.20,  x1, 0.45),
            (0.30,  x1, 0.30),
            (0.40,  x1, 0.15),
            (0.50,  x1, 0.00),
            (0.60,  x2, 0.10),
            (0.70,  x2, 0.25),
            (0.80,  x2, 0.40),
            (0.90,  x2, 0.50),
            (1.00,  x2, 0.55),
        ]

        # ── First scan: just show the peak shifting ──
        for rod_frac, peak_x, amplitude in scan_plan:
            self._scan_step(rod_frac, peak_x, amplitude)
            self.wait(0.15)

        self.wait(2)

        # Reset rod to bottom for second pass
        self._move_rod_to(0.0)

        # ── Build the mode map ──
        mode_map = Rectangle(
            width=3,
            height=self.cavity.height,
            stroke_width=3,
            color=WHITE,
            fill_color=BLACK,
            fill_opacity=1.0,
        ).next_to(self.cavity, RIGHT, buff=0.1)
        self.play(Create(mode_map))

        # Geometry references for the scan loop
        cell_size = 0.2
        ul = mode_map.get_corner(UL)
        baseline_y = self.trace_y_bot + self.S21_BASELINE

        # Spread the two peak rows across the tall map's height
        n_rows = 2
        row_spacing = mode_map.height / (n_rows + 1)

        # ── Second scan: same plan, this time record each measurement ──
        for i, (rod_frac, peak_x, amplitude) in enumerate(scan_plan):
            self._scan_step(rod_frac, peak_x, amplitude)
            self.wait(0.15)

            # Line at the peak's actual position on the trace
            amp_line = Line(
                start=[peak_x, baseline_y, 0],
                end=[peak_x, baseline_y + amplitude, 0],
                color=YELLOW,
                stroke_width=4,
            )

            # Pixel destination: column = scan step index, row = which peak
            col = i
            row = 0 if peak_x == x1 else 1
            pixel_y_offset = row_spacing * (row + 1)
            pixel_pos = ul + RIGHT * (cell_size * (col + 0.5)) + DOWN * pixel_y_offset

            # Brightness scales with amplitude
            brightness = amplitude / self.PEAK_HEIGHT_MAX
            pixel = Square(
                side_length=cell_size,
                stroke_width=0,
                fill_color=interpolate_color(BLACK, GREEN, brightness),
                fill_opacity=1.0,
            ).move_to(pixel_pos)

            self.play(Create(amp_line), run_time=0.3)
            self.play(Transform(amp_line, pixel), run_time=0.5)

        self.wait(2)

        # Target pixel on the mode map (0.2 x 0.2, solid green)
   

    # def _record_scan(self, rod_frac, peak_x, amplitude):
    #     pass

    # ══════════════════════════════════════════════════════════════
    def construct(self):
        self._build()
        self.section_setup()
        self.section_off_resonance()
        self.section_on_resonance()
        self.section_rod_scan()