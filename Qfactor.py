from manim import *
import numpy as np
import math
class CavitySineWave(Scene):
    def construct(self):
        cavity = Rectangle(ORANGE,width=4, height=4)
        cavity.set_fill(WHITE, opacity=0.1)
       
        pythonpulse = FunctionGraph(
        lambda x: 1/5*np.sin(20*x),
        x_range=[-3, 3, 0.01],
        color=BLUE,
        )       
        Rotate(pythonpulse)
        self.play(
            Create(cavity),
            Create(pythonpulse),
            run_time=3,
        )
        self.wait(3)
