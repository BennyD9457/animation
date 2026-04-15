from manim import *
import numpy as np

class CavityScene(Scene):
    def construct(self):
        # --- TITLE ---
        title = Text("Cavity", font_size=72)
        title.to_edge(UP)
        # --- CAVITY COMPONENTS ---
        cavity = Rectangle(width=1, height=4)
        cavity.set_fill(WHITE, opacity=0.1)

        antenna = Rectangle(width=0.1, height=0.5)
        antenna.set_fill(YELLOW, opacity=1)
        antenna.align_to(cavity, UP)
        antenna.shift(LEFT * 0.2)

        rod = Rectangle(width=0.1, height=0.5)
        rod.set_fill(ORANGE, opacity=1)
        rod.align_to(cavity, UP)
        rod.shift(RIGHT * 0.2)

        # --- VECTOR FIELD ---
        def cavity_field(pos):
            x, y, z = pos
            if abs(x) > 0.5 or abs(y) > 2:
                return np.array([0, 0, 0])
            strength = np.cos(np.pi * x / 1.0)
            return np.array([0, strength * 0.5, 0])

        field = ArrowVectorField(
            cavity_field,
            x_range=[-0.4, 0.4, 0.2],
            y_range=[-1.8, 1.8, 0.4],
            colors=[WHITE, WHITE, WHITE],
            opacity=0.5,
        )

        # --- GROUP & ANIMATE CAVITY ---
        cavity_group = VGroup(cavity, antenna, rod, field)

        self.play(Write(title, run_time=1))
        self.play(Create(cavity_group))
        self.wait(1)  # ← use self.wait(), NOT time.sleep()
        self.play(cavity_group.animate.shift(LEFT * 3))

        # --- AXES & SINE WAVE ---
        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=3,
            axis_config={"include_tip": True},
        ).shift(RIGHT * 2)

        self.play(Create(axes))

        # --- ANIMATED SINE WAVE ---
        t = ValueTracker(0.001)
        amp = 1.5

        # Orange rod oscillates up/down
        def update_rod(mob):
            y_val = np.sin(t.get_value())
            mob.move_to(
                cavity.get_center()
                + RIGHT * 0.2
                + UP * y_val * 1.5
            )
            mob.align_to(cavity, UP)
            mob.shift(DOWN * (1 - y_val) * 0.5)

        # Growing sine wave
        sine_wave = always_redraw(
            lambda: axes.plot(
                lambda x: amp * np.sin(x),
                x_range=[0, min(t.get_value(), 4 * PI)],
                color=YELLOW,
                stroke_width=3,
            )
        )

        # Dot at the tip
        leading_dot = always_redraw(
            lambda: Dot(
                axes.c2p(t.get_value(), amp * np.sin(t.get_value())),
                color=ORANGE,
                radius=0.1,
            )
        )

        # Dashed connection line
        connect_line = always_redraw(
            lambda: DashedLine(
                rod.get_bottom(),
                axes.c2p(t.get_value(), amp * np.sin(t.get_value())),
                color=ORANGE,
                stroke_width=1.5,
            )
        )

        
        wave_label = Text("TM_E + TM_M", font_size=24, color=BLUE)
        wave_label.next_to(axes, UP + RIGHT*.2)

        self.add(sine_wave, leading_dot, connect_line)
        self.play(Write(wave_label))

        # --- PLAY THE ANIMATION ---
        # self.play(
        #     t.animate.set_value(4 * PI),
        #     run_time=8,
        #     rate_func=linear,
        # )
        self.play(
            t.animate.set_value(4 * PI),
            rod.animate.stretch(2, dim=1, about_edge=UP),
            antenna.animate.stretch(1.2, dim=1, about_edge=UP),
            run_time=8,
            rate_func=linear,
        )

        self.wait()