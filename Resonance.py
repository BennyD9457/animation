from manim import *
import numpy as np

class Resonance(Scene):
    def construct(self):
        title = Text("Set Up", font_size=48, color=WHITE).to_edge(UP)
        self.play(Write(title))
        
        # VNA on the left
        VNA = Rectangle(width=3, height=2, stroke_width=8, color=WHITE)
        VNA.shift(LEFT * 3 + DOWN * 0.8)
        VNA_label = Text("VNA", font_size=24).next_to(VNA, UP, buff=0.1)
        
        # Cavity on the right
        cavity = Rectangle(width=5, height=4, stroke_width=8, color=ORANGE)
        cavity.shift(RIGHT * 3 + DOWN * 0.3)
        cavity_label = Text("Cavity", font_size=24, color=ORANGE).next_to(cavity, UP, buff=0.1)
        
        # S1 cable: top of VNA right edge → top of cavity left edge
        s1_start = VNA.get_right() + UP * 0.4
        s1_end = cavity.get_left() 
        S1 = Line(s1_start, s1_end, stroke_width=4, color=YELLOW)
        S1_label = Text("S1", font_size=20, color=YELLOW).next_to(S1, UP, buff=0.1)
        
        # S2 cable: bottom of VNA right edge bottom of cavity left edge
        s2_start = VNA.get_right() + DOWN * 0.4
        s2_end = cavity.get_left() + DOWN * 0.8
        S2 = Line(s2_start, s2_end, stroke_width=4, color=BLUE)
        S2_label = Text("S2", font_size=20, color=BLUE).next_to(S2, DOWN, buff=0.1)
        
        #Center Line: Cut VNA in half
        Center_LineS = VNA.get_right() 
        Center_LineE = VNA.get_left() 
        Center_Line = Line(Center_LineS, Center_LineE, stroke_width=4, color=WHITE)

        S1_label2 = Text("S1S1", font_size=15, color=BLUE).next_to(Center_Line, UP, buff=0.1)

        S2_label2 = Text("S1S2", font_size=15, color=BLUE).next_to(Center_Line, DOWN, buff=0.1)

        



        # Draw everything
        self.play(Create(VNA), Create(cavity), Create(Center_Line),Write(VNA_label), Write(cavity_label), Write(S1_label2),Write(S2_label2),Wrun_time=3)
        self.play(Create(S1), Write(S1_label), Create(S2), Write(S2_label), run_time=3)
        self.wait(1)