from manim import *
import time


class CavityScene(Scene):
    def construct(self):
        cavity = Rectangle(width=1, height=4)
        cavity.set_fill(WHITE, opacity=0.1)
        antenna = Rectangle(width=0.1, height=0.5)
        antenna.set_fill(YELLOW, opacity=1)
        antenna.align_to(cavity, UP)
        antenna.shift(LEFT * 0.2)
        circle = Circle(color=WHITE, radius=0.1)
        rod = Rectangle(width=0.1, height=0.5)
        rod.set_fill(ORANGE,opacity=100)
        rod.align_to(cavity, UP)
        circle.align_to(rod, DOWN)

        rod.shift(RIGHT * 0.2)
        circle.align_to(rod, DOWN)
        circle.move_to(RIGHT * 4)

        text = Text("Cavity", font_size=72)
        text.to_edge(UP)

        def cavity_field(pos):
            x, y, z = pos
            if abs(x) > 0.5 or abs(y) > 2:
                return np.array([0, 0, 0])
            strength = np.cos(np.pi * x / 1.0)
            return np.array([0, strength * 0.5, 0])

        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5,
            y_length=2,
            axis_config={"include_numbers": False},
        ).to_edge(RIGHT*.05)

        wave_graph = axes.plot(
            lambda x: np.sin(x),
            color=YELLOW,
            
        ).to_edge(RIGHT *.05)


        wave_label = Text("E(t)", font_size=24, color=BLUE)
        wave_label.next_to(wave_graph, UP + RIGHT)

        self.play(Write(text, run_time=1))

        field = ArrowVectorField(
            cavity_field,
            x_range=[-0.4, 0.4, 0.2],
            y_range=[-1.8, 1.8, 0.4],
            colors=[WHITE, WHITE, WHITE],
            opacity = .5
            
        )
        cavity_group = VGroup(cavity, antenna, rod,field)
        self.play(Create(cavity_group))
        time.sleep(1)
        self.play(cavity_group.animate.shift(LEFT * 2))
		

# Group the cavity with its components

# Create them

# Shift everything together smoothly

        # self.play(Create(field))
        self.play(Create(axes), Create(wave_graph), Write(wave_label))
        self.wait()

        self.play(
            rod.animate.stretch(2, dim=1, about_edge=UP),
            antenna.animate.stretch(1.2, dim=1, about_edge=UP),
            run_time=10,
        )