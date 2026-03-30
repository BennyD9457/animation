from manim import *

from manim_physics import *

# class CavityScene(Scene):
#     def construct(self):
#         cavity = Rectangle(width=1, height=4)
#         cavity.set_fill(WHITE, opacity=0.5)
#         antenna = Rectangle(width=0.1, height=.5)
#         antenna.set_fill(YELLOW, opacity=1)
#         antenna.align_to(cavity, UP)
#         antenna.shift(LEFT *.2)
#         circle = Circle(color=WHITE,radius=.1)
#         rod = Rectangle(width=0.1, height=.5)
#         rod.set_fill(ORANGE, opacity=1)
#         rod.align_to(cavity, UP)
#         circle.align_to(rod, DOWN)
        

#         rod.shift(RIGHT * 0.2)
    
        
#         circle.align_to(rod,DOWN)
#         circle.move_to(RIGHT * 4)


#         text = Text("Cavity", font_size=72)
#         text.to_edge(UP)
        
#         # Replace the MagneticField block with something like:
#         # wire = Wire(Circle(radius=2).rotate(PI / 2, UP))
        
        
#         # Create the magnetic field around the wire
#         rect_wire = Wire(cavity)
        
#         # 2. Generate the magnetic field from the wire
      
        
    

#         self.play(
#             Write(text,run_time=3)


#         )

        
#         self.play(Create(cavity))
#         self.play(Create(antenna))
#         self.play(Create(rod))
#         self.play(Create(circle))
        
#         self.play(
#             rod.animate.stretch(2, dim=1, about_edge=UP),
#             antenna.animate.stretch(1.2, dim=1, about_edge=UP),
#             run_time=10
#         )        
        

class CavityScene(Scene):
    def construct(self):
        cavity = Rectangle(width=1, height=4)
        cavity.set_fill(WHITE, opacity=0.1)
        antenna = Rectangle(width=0.1, height=.5)
        antenna.set_fill(YELLOW, opacity=1)
        antenna.align_to(cavity, UP)
        antenna.shift(LEFT *.2)
        circle = Circle(color=WHITE,radius=.1)
        rod = Rectangle(width=0.1, height=.5)
        rod.set_fill(ORANGE, opacity=1)
        rod.align_to(cavity, UP)
        circle.align_to(rod, DOWN)
        

        rod.shift(RIGHT * 0.2)
    
        
        circle.align_to(rod,DOWN)
        circle.move_to(RIGHT * 4)


        text = Text("Cavity", font_size=72)
        text.to_edge(UP)
        def cavity_field(pos):
            x, y, z = pos
            # only show inside cavity bounds
            if abs(x) > 0.5 or abs(y) > 2:
                return np.array([0, 0, 0])
            # vertical E-field, strongest at center, fading toward walls
            strength = np.cos(np.pi * x / 1.0)  # falloff toward x-walls
            return np.array([0, strength * 0.5, 0])
      

    
        graph(LinearWave)
        self.play(
            Write(text,run_time=3)


        )
        # TM010-like field: E_z ~ J_0(r), approximate as cosine falloff from center
      

        field = ArrowVectorField(
            cavity_field,
            x_range=[-0.4, 0.4, 0.2],
            y_range=[-1.8, 1.8, 0.4],
            colors=[BLUE, RED, GREEN],
        )
       

        self.play(Create(cavity))
        self.play(Create(field))
        self.wait()
        
        self.play(
            rod.animate.stretch(2, dim=1, about_edge=UP),
            antenna.animate.stretch(1.2, dim=1, about_edge=UP),
            run_time=10
        )  