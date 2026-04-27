from manim import *

class ModeMapStep(Scene):
    def construct(self):
        # Wave on the left
        axes = Axes(x_range=[0, 4*PI], y_range=[-2, 2], x_length=5, y_length=3).shift(LEFT*3)
        amplitude = 1.5
        wave = axes.plot(lambda x: amplitude * np.sin(x), color=BLUE)

        peak_x = PI / 2
        amp_line = Line(
            start=axes.c2p(peak_x, 0),
            end=axes.c2p(peak_x, amplitude),
            color=YELLOW,
            stroke_width=4,
        )

        # Mode map on the right
        ModeMap = Square(
            side_length=3,
            stroke_width=3,
            color=WHITE,
            fill_color=WHITE,
            fill_opacity=1.0,
        ).shift(RIGHT*3)

        # Pixel positioned RELATIVE to the mode map.
        # get_corner(UL) gives the upper-left corner; offset in by half a pixel
        # so the square sits inside the cell instead of straddling the edge.
        cell_size = 0.2
        col, row = 0, 0  # grid indices into the map
        ul = ModeMap.get_corner(UL)
        pixel_pos = ul + RIGHT*(cell_size*(col + 0.4)) + DOWN*(cell_size*(row + 0.5))

        pixel = Square(
            side_length=cell_size,
            stroke_width=0,
            fill_color=GREEN,
            fill_opacity=1.0,
        ).move_to(pixel_pos)

        self.play(Create(ModeMap))
        self.play(Create(wave))
        self.play(Create(amp_line))
        self.play(Transform(amp_line, pixel))
        self.wait()