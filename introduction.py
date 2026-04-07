from manim import *
import numpy as np

class CavitySineWave(Scene):
    def construct(self):
        title = Text("Placeholder", font_size=72)
        title.to_edge(UP)
        self.play(Write(title))

        wire = Line(
            start=UP * 2,
            end=DOWN * 2,
            color=ORANGE,
            stroke_width=3   
        )

        Wirearrow = Arrow(
            start=RIGHT * 2,
            end=wire.get_right(),  # points to left edge of circle
            color=YELLOW,
            buff=0.1  # small gap between arrow tip and target
        )
        self.play(Create(wire),Create(Wirearrow))
        self.wait(5)
        self.play(FadeOut(Wirearrow))
        

        #  CAVITY 
        cavity = Rectangle(width=5, height=4,stroke_width=8,color=ORANGE)
        cavity.shift(LEFT * 4 + DOWN * 0.3)

        bField = VGroup()
        for x in np.linspace(-2, 2, 8):
            for y in np.linspace(-1.6, 1.6, 8):
                arr = Arrow(
                    start=cavity.get_center() + np.array([x, y, 0]),
                    end=cavity.get_center() + np.array([x, y + 0.25, 0]),
                    buff=0, color=BLUE, stroke_width=1.5,
                    max_tip_length_to_length_ratio=0.5,
                )
                bField.add(arr)

        # Arrow
        arrow = Arrow(
            start=RIGHT * 1+UP* 2,
            end=cavity.get_right() + UP *2,  # points to left edge of circle
            color=YELLOW,
            buff=0.1  # small gap between arrow tip and target
        )




        label = Text("CooperCavity", font_size=30).next_to(arrow, RIGHT)

        
        WavesA = Arrow(
            start=RIGHT * 1,
            end=cavity.get_right() + LEFT *2,  # points to left edge of circle
            color=YELLOW,
            buff=0.1  # small gap between arrow tip and target
        )
        WaveAlabel = Text("E + M Field", font_size= 20)
        
        
        cavitylabelA_group = VGroup()
        # cavitylabelA_group.add(arrow,label)
        

        # cavity_group = VGroup(cavity, arrows)
        self.play(Transform(wire,cavity),run_time = 2)
        self.play (Create(bField),Create(label), run_time = 2)
        self.play(FadeOut(label))
        self.play(Create(WavesA),Create(WaveAlabel))

      
        self.wait()
        # self.play(FadeIn(arrows),run_time=2)

        self.wait()