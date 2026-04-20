from manim import *
import numpy as np

class Resonance(Scene):
    def construct(self):
        title = Text("Set Up", font_size=48, color=WHITE).to_edge(UP)
       
        
        # VNA on the left
        VNA = Rectangle(width=4, height=4, stroke_width=8, color=WHITE)
        VNA.shift(LEFT * 3 + DOWN * 0.8)
        VNA_label = Text("VNA", font_size=24).next_to(VNA, UP, buff=0.1)
        
        # Cavity on the right
        cavity = Rectangle(width=5, height=2, stroke_width=8, color=ORANGE)
        cavity.shift(RIGHT * 3 + DOWN * 0.5)
        cavity_label = Text("Cavity", font_size=24, color=ORANGE).next_to(cavity, UP, buff=0.1)
        
        # Cables
        s1_start = VNA.get_right() + UP * 0.4
        s1_end = cavity.get_left() 
        S1 = Line(s1_start, s1_end, stroke_width=4, color=YELLOW)
        S1_label = Text("S1", font_size=20, color=YELLOW).next_to(S1, UP, buff=0.1)
        
        s2_start = VNA.get_right() + DOWN * 0.4
        s2_end = cavity.get_left() + DOWN * 0.8
        S2 = Line(s2_start, s2_end, stroke_width=4, color=BLUE)
        S2_label = Text("S2", font_size=20, color=BLUE).next_to(S2, DOWN, buff=0.1)
        
        # VNA internal divider + port labels
        Center_Line = Line(VNA.get_left(), VNA.get_right(), stroke_width=4, color=WHITE)
        S11_label = Text("S11", font_size=15, color=BLUE).next_to(Center_Line, UP, buff=0.05).shift(LEFT*0.9)
        S21_label = Text("S21", font_size=15, color=BLUE).next_to(Center_Line, DOWN, buff=0.05).shift(LEFT*0.9)
        
        
        
        # --- Noisy traces inside the VNA ---
        # Define the two trace windows inside the VNA rectangle
        # Top half (S11): between Center_Line and VNA top
        # Bottom half (S21): between Center_Line and VNA bottom
        
        def make_noisy_trace(y_center, x_left, x_right, amplitude=0.05, freq=30, noise=0.05, n_points=300, seed=0):
            """Build a noisy sine wave as a list of 3D points."""
            rng = np.random.default_rng(seed)
            xs = np.linspace(x_left, x_right, n_points)
            ys = y_center + amplitude * np.sin(freq * (xs - x_left)) + noise * rng.standard_normal(n_points)
            return [np.array([x, y, 0]) for x, y in zip(xs, ys)]



        # --- Pulse animation: off-resonance reflection ---

        def make_pulse(color=WHITE, radius=0.12):
            """A small glowing pulse — a dot with a faint outer glow."""
            inner = Dot(radius=radius, color=color, fill_opacity=1)
            outer = Dot(radius=radius*2, color=color, fill_opacity=0.25)
            return VGroup(outer, inner)

        # Caption for what's happening
        off_res_caption = Text("Off resonance: signal reflects back", font_size=24, color=WHITE).to_edge(DOWN)

        # Pulse 1: VNA → cavity along S1, then bounces back along S1
        pulse = make_pulse(color=YELLOW)
        pulse.move_to(s1_start)
        self.add(pulse)

     
        # Return trip — build a reversed line
        S1_return = Line(s1_end, s1_start)
        self.remove(pulse)
        self.wait(0.5)

    
        # Pulse travels VNA → cavity via S1, then cavity → VNA via S2
        pulse2 = make_pulse(color=YELLOW)
        pulse2.move_to(s1_start)
        self.add(pulse2)

        
        # Out through S2 (reversed, since S2 was drawn VNA→cavity but now we want cavity→VNA)
        S2_return = Line(s2_end, s2_start)
        pulse2.move_to(s2_end)
        self.remove(pulse2)

        # Restore cavity color
        self.wait(1)




        # Inner bounds of the VNA (inset from stroke)
        x_left = VNA.get_left()[0] + 0.15
        x_right = VNA.get_right()[0] - 0.15
        y_top_center = (Center_Line.get_center()[1] + VNA.get_top()[1]) / 2
        y_bot_center = (Center_Line.get_center()[1] + VNA.get_bottom()[1]) / 2
        
        s11_points = make_noisy_trace(y_top_center, x_left, x_right, seed=1)
        s21_points = make_noisy_trace(y_bot_center, x_left, x_right, seed=2)
        
        s11_trace = VMobject(stroke_width=2, color=YELLOW)
        s11_trace.set_points_as_corners(s11_points)
        
        s21_trace = VMobject(stroke_width=2, color=BLUE)
        s21_trace.set_points_as_corners(s21_points)
        


        #PLAY ORDER:
        self.play(Write(title))

        self.play(Create(VNA), Create(cavity), Create(Center_Line),
                  Write(VNA_label), Write(cavity_label),
                  Write(S11_label), Write(S21_label), run_time=2)
        self.play(Create(S1), Write(S1_label), Create(S2), Write(S2_label), run_time=2)
        self.wait(0.5)


        self.play(Create(s11_trace), Create(s21_trace), run_time=2)


        self.play(Write(off_res_caption))

           # Forward trip
        self.play(MoveAlongPath(pulse, S1), run_time=1.2, rate_func=linear)
        # Flash at the cavity port to show reflection
        self.play(Flash(s1_end, color=ORANGE, flash_radius=0.3, num_lines=12), run_time=0.4)

        self.play(MoveAlongPath(pulse, S1_return), run_time=1.2, rate_func=linear)



        self.play(Transform(off_res_caption,
            Text("On resonance: signal passes through to S2", font_size=24, color=ORANGE).to_edge(DOWN)))

        # Cavity lights up to signal we're at resonance
        self.play(cavity.animate.set_stroke(color=YELLOW, width=12), run_time=0.4)



        self.play(MoveAlongPath(pulse2, S1), run_time=1.2, rate_func=linear)
        # Brief "bouncing inside the cavity" moment — tiny pulse scale-up
        self.play(pulse2.animate.scale(1.5), run_time=0.3)
        self.play(pulse2.animate.scale(1/1.5), run_time=0.3)



        self.play(MoveAlongPath(pulse2, S2_return), run_time=1.2, rate_func=linear)

    
        self.play(cavity.animate.set_stroke(color=ORANGE, width=8), run_time=0.4)

        self.wait(2)


