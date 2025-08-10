from manim import *
import math

# Helper functions.

def make_title(title):
    return Title(title, color=ORANGE)


class ACS(Scene):

    def __init__(self):
        Scene.__init__(self)

        # Declare the latex formulas.
        mip_latex = (
            r"\begin{cases}"
                r"\min c^Tx\\"
                r"Ax = b\\"
                r"l \leq x \leq u"
                r"\\ x_i \in \mathbb Z"
                r"\quad \forall i\in I"
            r"\end{cases}"
        )

        fmip_latex = (
            r"\begin{cases}"
                r"\min \sum\limits_{i=0}^{m-1} \Delta_i^+ + \Delta_i^- \\"
                r"Ax + I_m \Delta^+ - I_m \Delta^- = b \\"
                r"x_i = \tilde x_i \quad \forall i \in F \\"
                r"l \leq x \leq u\\"
                r"x_i \in \mathbb{Z} \quad \forall i \in I\\"
                r"\Delta^+ \geq 0,\quad \Delta^- \geq 0"
            r"\end{cases}"
        )

        omip_latex = (
            r"\begin{cases}"
                r"\min c^Tx\\"
                r"Ax + I_m \Delta^+ - I_m \Delta^- = b \\"
                r"\sum\limits_{i=0}^{m-1} \Delta^+_i + \Delta^-_i \leq \sum\limits_{i=0}^{m-1} \hat \Delta^+_i + \hat \Delta^-_i\\"
                r"x_i = \hat x_i \quad \forall i \in F \\"
                r"l \leq x \leq u\\"
                r"x_i \in \mathbb Z \quad \forall i\in I\\"
                r"\Delta^+ \geq 0,\quad \Delta^- \geq 0"
            r"\end{cases}"
        )


        # Define the equations.
        self.eq_dic = {
                "mip":  MathTex(mip_latex, font_size=40),
                "fmip": MathTex(fmip_latex, font_size=30),
                "omip": MathTex(omip_latex, font_size=30)
        }

        # Define the label for each equation.
        self.label_dic = {
                "mip": Tex(r"\textbf{Input MIP}", font_size=30, color=ORANGE),
                "fmip": Tex(r"\textbf{FMIP}", font_size=30, color=ORANGE),
                "omip": Tex(r"\textbf{OMIP}", font_size=30, color=ORANGE),
        }


    def construct(self):
        self.intro()
        self.submip_description()
        self.acs_algorithm()
        self.convergence()


    def intro(self):
        # Plot the title.
        title = make_title("Alternating Criteria Search")
        self.play(Write(title))
        self.wait(1)

        # Plot MIP formulation.
        self.eq_dic["mip"].next_to(title, DOWN)
        self.label_dic["mip"].next_to(self.eq_dic["mip"], DOWN, buff=0.3)
        self.play(Write(self.label_dic["mip"]), Write(self.eq_dic["mip"]))
        #self.add(index_labels(self.eq_dic["mip"][0]))
        self.wait(2)

        # Plot the FMIP formulation.
        self.eq_dic["fmip"].to_edge(DOWN).to_edge(LEFT)
        self.label_dic["fmip"].next_to(self.eq_dic["fmip"], UP, buff=0.3)
        self.play(Write(self.label_dic["fmip"]), Write(self.eq_dic["fmip"]))
        #self.add(index_labels(self.eq_dic["fmip"][0]))
        self.wait(2)

        # Plot the OMIP formulation.
        self.eq_dic["omip"].to_edge(DOWN).to_edge(RIGHT)
        self.label_dic["omip"].next_to(self.eq_dic["omip"], UP, buff=0.3)
        self.play(Write(self.label_dic["omip"]), Write(self.eq_dic["omip"]))
        #self.add(index_labels(self.eq_dic["omip"][0]))
        self.wait(2)

        # Highlight the constrains using the boxes.
        self.higlights_constraints()

        self.play(FadeOut(title))


    def higlights_constraints(self):
        # Define box specs: (label, index range, color, wait time)
        box_specs = [
            # Bounds + integrality
            ("mip",  slice(19, 32), GREEN, 1),
            ("fmip", slice(64, 77), GREEN, 0.5),
            ("omip", slice(88,101), GREEN, 0.5),

            # Constraints
            ("mip",  slice(15, 19), BLUE, 1),
            ("fmip", slice(40, 42), BLUE, 0.5),
            ("fmip", slice(52, 54), BLUE, 0),
            ("omip", slice(33, 35), BLUE, 0.5),
            ("omip", slice(45, 47), BLUE, 0.5),

            # Objective functions
            ("mip",  slice(9, 15), PURPLE, 1),
            ("omip", slice(27, 33), PURPLE, 0.5),
        ]

        # Draw the boxes.
        boxes = VGroup()
        for key, span, color, wait_time in box_specs:
            mobj = self.eq_dic[key][0][span]
            box = SurroundingRectangle(mobj, color=color)
            boxes.add(box)

            self.play(Create(box))
            if wait_time > 0:
                self.wait(wait_time)

        # Fade out all the boxes.
        self.play(FadeOut(box) for box in boxes)
        self.wait(2)

    
    def submip_description(self):
        # Fade out MIP formulation.
        self.play(
            FadeOut(self.eq_dic["mip"]),
            FadeOut(self.label_dic["mip"]),
        )

        # Update title.
        title = make_title("The auxiliary MIP problems: FMIP, OMIP")
        self.play(Write(title))
        self.wait(1.5)

        # Higlight slacks variables.
        box_specs = [
            # Slack variables
            ("fmip", slice(43, 52), GREEN),
            ("fmip", slice(77, 86), GREEN),
            ("omip", slice(36, 45), GREEN),
            ("omip", slice(101, 110), GREEN),

            # Variable fixing
            ("fmip", slice(54, 64), BLUE),
            ("omip", slice(78, 88), BLUE),
        ]

        boxes = VGroup()
        for key, span, color in box_specs:
            mobj = self.eq_dic[key][0][span]
            box = SurroundingRectangle(mobj, color=color)
            boxes.add(box)
            self.play(Create(box))
        
        # Introduce slack and var fixing.
        descriptions = VGroup(
            Tex(r"Add the slack variables $\Delta^+, \Delta^-$", color=GREEN),
            Tex(r"Fix some of the integer vairables", color=BLUE)
        )
        descriptions[0].next_to(title, DOWN, buff=0.3)
        descriptions[1].next_to(descriptions[0], DOWN, buff=0.3)
        self.play(Write(descriptions))
        self.wait(4)

        # Fade out everything.
        self.play(FadeOut(descriptions))
        self.play(FadeOut(box) for box in boxes)
        self.play(FadeOut(title))


    def acs_algorithm(self):
        title = make_title("ACS steps")
        self.play(Write(title))

        # Describe steps of the algorithm.
        steps = VGroup(
            Tex(r"\textbf{For each iteration:}", font_size=25),
            Tex("1 - Solve FMIP: minimize infeasibility", font_size=23),
            Tex("2 - Fix random integer variables in OMIP and set infeasibility upperbound", font_size=23),
            Tex("3 - Solve OMIP: optimize original objective", font_size=23),
            Tex("4 - Fix random integer variables in FMIP", font_size=23)
        )

        steps[0].next_to(title, DOWN, buff=0.3)
        for i in range(1, len(steps)):
            steps[i].next_to(steps[i-1], DOWN, buff=0.3)
        self.play(FadeIn(steps))
        self.wait(3)

        # - Step 1 -
        self.play(Indicate(steps[1], color=YELLOW))
        self.wait(1)
        self.play(Indicate(self.eq_dic["fmip"]))
        self.wait(1)

        # Draw the arrow.
        fmip_arrow = CurvedArrow(
            self.eq_dic["fmip"].get_right(),
            self.eq_dic["omip"].get_left(),
            angle=-PI/2,
            stroke_width=2
        ).shift(UP * 0.3)
        self.play(Create(fmip_arrow))
        self.wait(1)

        fmip_sol = MathTex(r"\hat\Delta^+, \hat\Delta^-, \hat x", font_size=30)
        fmip_sol.next_to(fmip_arrow, UP)
        self.play(Write(fmip_sol))
        self.wait(1)

        # - Step 2 -
        self.play(Indicate(steps[2], color=YELLOW))
        self.wait(1)
        self.play(
            steps[2].animate.set_color(GREEN),
            fmip_sol.animate.set_color(GREEN),
            self.eq_dic["omip"][0][62:88].animate.set_color(GREEN),
            fmip_arrow.animate.set_color(GREEN),
            run_time=2
        )
        self.wait(2)

        # - Step 3 -
        self.play(Indicate(steps[3], color=YELLOW))
        self.wait(1)
        self.play(Indicate(self.eq_dic["omip"]))
        self.wait(1)

        # Draw the arrow.
        omip_arrow = CurvedArrow(
            self.eq_dic["omip"].get_left(),
            self.eq_dic["fmip"].get_right(),
            angle=-PI/2,
            stroke_width=2
        ).shift(DOWN * 0.3)
        self.play(Create(omip_arrow))
        self.wait(1)

        omip_sol = MathTex(r"\tilde x", font_size=30)
        omip_sol.next_to(omip_arrow, DOWN)
        self.play(Write(omip_sol))
        self.wait(1)

        # Step 4
        self.play(Indicate(steps[4], color=YELLOW))
        self.wait(1)
        self.play(
            steps[4].animate.set_color(BLUE),
            omip_sol.animate.set_color(BLUE),
            self.eq_dic["fmip"][0][54:64].animate.set_color(BLUE),
            omip_arrow.animate.set_color(BLUE),
            run_time=2
        )
        self.wait(2)

        # Indicate all the steps, iteratively.
        for _ in range(3):
            # Step 1
            self.play(
                Indicate(steps[1], color=YELLOW),
                Indicate(self.eq_dic["fmip"]),
            )

            # Step 2
            self.play(
                Indicate(steps[2], color=YELLOW),
                Indicate(fmip_arrow),
                Indicate(fmip_sol),
                Indicate(self.eq_dic["omip"][0][62:88]),
            )

            # Step 3
            self.play(
                Indicate(steps[3], color=YELLOW),
                Indicate(self.eq_dic["omip"])
            )

            # Step 4
            self.play(
                Indicate(steps[4], color=YELLOW),
                Indicate(omip_arrow),
                Indicate(omip_sol),
                Indicate(self.eq_dic["fmip"][0][54:64])
            )

        # Fade out arrows and solutions.
        self.play(FadeOut(title))
        self.play(
            FadeOut(fmip_arrow),
            FadeOut(fmip_sol),
            FadeOut(omip_arrow),
            FadeOut(omip_sol),
        )

        # Restore colors.
        self.play(
            self.eq_dic["omip"][0][62:88].animate.set_color(WHITE),
            self.eq_dic["fmip"][0][54:64].animate.set_color(WHITE)
        )

        # Fade out steps. 
        self.play(FadeOut(steps))

    
    def convergence(self):
        title = make_title("When does the algorithm stops?")
        self.play(Write(title))
        self.wait(1.5)

        descriptions = VGroup(
            Tex(r"""
                When the infeasibility 
                $\sum_{i=0}^{m-1} \hat \Delta_i^+ + \hat \Delta_i^-$,
                reaches the value 0 it means that we have found a feasible
                solution for MIP. In such situation the algorithm stops.
                """,
                font_size=25
            ),
            Tex(r"""
                MIP and OMIP have the same objective function and the same constraints.
                The variables fixed in OMIP are feasible for the MIP by construction.
                """,
                font_size=25
            ),
            Tex(r"""
                Therefore the solution provided by solving OMIP when
                the infeasibility is zero, provide a \textit{feasible}
                solution for MIP.
                """,
                font_size=25
            ),
            Tex(r"""
                By construction, the infeasibility decreases towards zero
                iteration by iteration, however the 
                \textbf{convergence is not guaranteed!}
                Therefore we must define also another stopping 
                rule (e.g. max number of iterations).
                """,
                font_size=25
            )
        )

        # Pre-define the position of the text.
        descriptions[0].next_to(title, DOWN)
        descriptions[1].next_to(descriptions[0], DOWN)
        descriptions[2].next_to(descriptions[1], DOWN)
        descriptions[3].next_to(descriptions[0], DOWN)

        # Now procede step by step.
        self.play(Write(descriptions[0]))
        self.wait(4)

        # Draw the arrow from fmip to omip and show solution.
        fmip_arrow = CurvedArrow(
            self.eq_dic["fmip"].get_right(),
            self.eq_dic["omip"].get_left(),
            angle=-PI/2,
            stroke_width=2
        ).shift(UP * 0.3)
        self.play(FadeIn(fmip_arrow))
        self.wait(2)

        fmip_sol = MathTex(
            r"\hat\Delta^+ = \hat\Delta^- = \vec{0},\,\,\hat x",
            font_size=30
        )
        fmip_sol.next_to(fmip_arrow, UP)
        self.play(FadeIn(fmip_sol))
        self.wait(3)

        # Transform the omip.
        omip_cons = VGroup(
            self.eq_dic["omip"][0][35:45],
            self.eq_dic["omip"][0][62:78]
        )
        self.play(FadeOut(omip_cons))

        self.play( # Move the "= b" to get "Ax = b".
            self.eq_dic["omip"][0][45:47].animate.next_to(self.eq_dic["omip"][0][34]),
            run_time=1.5
        )

        zero = MathTex(
            "0",
            font_size=self.eq_dic["omip"].font_size
        ).move_to(omip_cons[1].get_left()).shift(RIGHT * 0.2)

        self.play( # Set upperbound to zero
             FadeIn(zero),
             run_time=1.5
        )
        self.wait(3)

        omip_deltas = VGroup(
            zero,
            self.eq_dic["omip"][0][47:62],
            self.eq_dic["omip"][0][101:110],
        )
        self.play(Indicate(omip_deltas))
        self.wait(1.5)
        self.play(FadeOut(omip_deltas))

        # Fade out FMIP and related arrows and solution.
        self.play(
            FadeOut(fmip_arrow),
            FadeOut(fmip_sol),
            FadeOut(self.eq_dic["fmip"]),
            FadeOut(self.label_dic["fmip"]),
            run_time=1
        )
        self.wait(1)

        # Bring back MIP.
        self.eq_dic["mip"].move_to(self.eq_dic["fmip"].get_center())
        self.label_dic["mip"].next_to(self.eq_dic["mip"], UP)
        self.play(
            FadeIn(self.eq_dic["mip"]),
            FadeIn(self.label_dic["mip"]),
        )

        # Write last descriptions.
        descriptions[1].next_to(descriptions[0], DOWN)
        self.play(Write(descriptions[1]))
        self.wait(3)

        descriptions[2].next_to(descriptions[1], DOWN)
        self.play(Write(descriptions[2]))
        self.wait(5)

        self.play(
            FadeOut(descriptions[1]),
            FadeOut(descriptions[2]),
        )
        self.wait(0.5)

        descriptions[3].next_to(descriptions[0], DOWN)
        self.play(Write(descriptions[3]))
        self.wait(5)
