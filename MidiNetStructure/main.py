from manim import *

### GLOBAL VARS ###
curr_path = "./curr.png"
prev_path = "./prev.png"
non_mono_path = "./non_mono.png"

# Load images.
prev = ImageMobject(prev_path, invert=True).scale(0.3)
curr = ImageMobject(curr_path, invert=True).scale(0.3)
non_mono = ImageMobject(non_mono_path, invert=True).scale(0.3)

### Helper functions ###
def create_circ(fill_opacity=0.5):
    return Circle(radius=0.05, stroke_width=1.5, color=WHITE, fill_color=WHITE, fill_opacity=fill_opacity)

def stack_circles(start_circle, count, shift=DOWN * 0.3):
    circles = VGroup(start_circle)
    for _ in range(count - 1):
        new_circ = create_circ()
        new_circ.move_to(circles[-1]).shift(shift)
        circles.add(new_circ)
    return circles


def create_rect(color):
    return Rectangle(width=0.5, stroke_width=1.5, height=0.5, fill_color=color, fill_opacity=1)

def stack_blocks(start_rect, count, shift=UP * 0.4 + LEFT * 0.4):
    blocks = VGroup(start_rect)
    for _ in range(count - 1):
        new_rect = create_rect(start_rect.fill_color)
        new_rect.move_to(blocks[-1]).shift(shift)
        blocks.add(new_rect)
    return blocks

def create_4_elbows_line(start, shift1, shift2, shift3, shift4, end):
    p1 = start + shift1
    p2 = p1    + shift2
    p3 = p2    + shift3 
    p4 = p3    + shift4
    line = VGroup(
        create_circ(fill_opacity=1).move_to(start), # Little circle con the start.
        DashedLine(start, p1, stroke_width=1),
        DashedLine(p1, p2, stroke_width=1),
        DashedLine(p2, p3, stroke_width=1),
        DashedLine(p3, p4, stroke_width=1),
        DashedLine(p4, end, stroke_width=1)
    )
    return line


## Scene Class ###
class MidiNet(Scene):

    def construct(self):
        self.generator()
        self.play(FadeOut(*self.mobjects))
        self.clear()
        self.discriminator()
        self.play(FadeOut(*self.mobjects))
        self.clear()

    def generator(self):

        # Set title.
        title = Title(r"Generator - Model v3", color=ORANGE)
        self.play(Write(title))
        self.wait(1)

        ### CONDITIONER ###
        # Input.
        prev.next_to(title, DOWN).shift(DOWN * 1.5 + LEFT * 6)
        prev_desc = VGroup(
            Tex("Previous melody bar", font_size=15).next_to(prev, UP * 0.5),
            Tex(r"$[1 \times 128 \times 16]$", font_size=15).next_to(prev, DOWN * 0.5),
        )
        self.play(
            Write(
                Tex(r"\textbf{Conditioner NN:}", font_size=25, color=BLUE).next_to(prev_desc, UP)
            ),
            FadeIn(prev), 
            Write(prev_desc)
        )
        self.wait(2)

        # Layer 1.
        cond_layer1 = VGroup()
        cond_layer1.add(rect for rect in stack_blocks(create_rect(BLUE), 3))

        cond_layer1.scale(0.2)
        for mob in cond_layer1:
            mob.stretch_to_fit_width(mob.width + 0.9)

        cond_layer1.next_to(prev).shift(RIGHT * 0.5)

        # Layer 2.
        cond_layer2 = cond_layer1.copy()

        for mob in cond_layer2:
            mob.stretch_to_fit_width(mob.width - 0.3)

        cond_layer2.next_to(cond_layer1, RIGHT).shift(RIGHT * 1.5)

        # Layer 3.
        cond_layer3 = cond_layer1.copy()

        for mob in cond_layer3:
            mob.stretch_to_fit_width(mob.width - 0.6)

        cond_layer3.next_to(cond_layer2, RIGHT).shift(RIGHT * 1.5)

        # Layer 4.
        cond_layer4 = cond_layer1.copy()

        for mob in cond_layer4:
            mob.stretch_to_fit_width(mob.width - 0.9)

        cond_layer4.next_to(cond_layer3, RIGHT).shift(RIGHT * 1.5)

        self.play(
            (Create(mob) for mob in reversed(cond_layer1)),
            (Create(mob) for mob in reversed(cond_layer2)),
            (Create(mob) for mob in reversed(cond_layer3)),
            (Create(mob) for mob in reversed(cond_layer4)),
        )
        self.wait(1)


        # Layers descriptions.
        cond_layers_desc = VGroup(
            Tex(r"Conv2D\\$[a \times 1 \times 16]$", font_size=15).next_to(cond_layer1.get_bottom()).shift(DOWN * 0.3 + LEFT * 0.5),
            Tex(r"Conv2D\\$[a\times 1\times 8]$", font_size=15).next_to(cond_layer2.get_bottom()).shift(DOWN * 0.3 + LEFT * 0.5),
            Tex(r"Conv2D\\$[a\times 1 \times 4]$", font_size=15).next_to(cond_layer3.get_bottom()).shift(DOWN * 0.3 + LEFT * 0.5),
            Tex(r"Conv2D\\$[a \times 1 \times 2]$", font_size=15).next_to(cond_layer4.get_bottom()).shift(DOWN * 0.3 + LEFT * 0.5)
        )
        self.play(Write(cond_layers_desc))
        self.wait(2)

        # Crate arrow between convolution.
        cond_arrows = VGroup(
                Arrow(
                    start=cond_layer1.get_right(),
                    end=cond_layer2.get_left(),
                    stroke_width=0.7,
                    tip_length=0.1,
                ),
                Arrow(
                    start=cond_layer2.get_right(),
                    end=cond_layer3.get_left(),
                    stroke_width=0.7,
                    tip_length=0.1,
                ),
                Arrow(
                    start=cond_layer3.get_right(),
                    end=cond_layer4.get_left(),
                    stroke_width=0.7,
                    tip_length=0.1,
                ),
                Arrow(
                    start=cond_layer4.get_right(),
                    end=cond_layer4.get_right() + RIGHT,
                    stroke_width=0.7,
                    tip_length=0.1,
                ),
        )
        self.play(FadeIn(cond_arrows))

        # BN + LeakyReLU descriptions.
        self.play(
            Write(
                Tex(r"\texttt{BN + LReLU}", font_size=12)
                .next_to(arrow, UP).shift(DOWN * 0.2)
            )
            for arrow in cond_arrows
        )
        self.wait(2)


        ### GENERATOR ###
        # Noise. 
        noise = Rectangle(width=0.1, height=1, fill_color=WHITE, fill_opacity=0.5)
        noise.to_edge(DOWN + LEFT).shift(RIGHT * 0.3)
        noise_desc = VGroup(
            Tex("Input noise", font_size=15).move_to(noise.get_top()).shift(UP * 0.2),
            Tex("100", font_size=15).move_to(noise.get_bottom()).shift(DOWN * 0.2)
        )
        # 1D condition.
        oneDcond = Rectangle(width=0.5, stroke_width=1.5, height=0.1, fill_color=ORANGE, fill_opacity=1,)
        oneDcond.next_to(noise_desc, UP * 1.5)
        oneDcond_desc = VGroup(
            Tex("Encoded Chord", font_size=15).move_to(oneDcond.get_top()).shift(UP * 0.1),
            Tex("13", font_size=15).move_to(oneDcond.get_bottom()).shift(DOWN * 0.1)
        )
        self.play(
            Write(
                Tex(r"\textbf{Generator:}", font_size=25, color="#FA8D7A").next_to(oneDcond, UP * 1.2)
            ),
            Create(noise),
            Write(noise_desc)
        )
        self.play(Create(oneDcond), Write(oneDcond_desc))
        self.wait(2)


        # fully-connected 1.
        full1 = VGroup()
        f1_start = create_circ()
        full1.add(circ for circ in stack_circles(f1_start, 5))

        full1.next_to(noise).shift(RIGHT * 0.3)
        self.play(Create(full1))

        # fully-connected 2.
        full2 = VGroup()
        f2_start = create_circ()
        full2.add(circ for circ in stack_circles(f2_start, 3))

        full2.next_to(full1).shift(RIGHT * 0.2)
        self.play(Create(full2))

        # Fully connected layer arrows.
        full_arrows = VGroup()

        for f1 in full1:
            for f2 in full2:
                arrow = Line(
                    start=f1.get_right(),
                    end=f2.get_left(),
                    stroke_width=0.5,
                )
                full_arrows.add(arrow)

        # Fully connected descriptions.
        fully_desc = VGroup(
            Tex("1024", font_size=15).next_to(full1, DOWN).shift(UP * 0.2),
            Tex("256", font_size=15).next_to(full2, DOWN).shift(UP * 0.2),
        )
        self.play(Create(full_arrows), Write(fully_desc))
        self.wait(2)

        # Define layer1 and build in levels
        layer1 = VGroup()

        # Level 1: PURPLE (3 blocks)
        purple_start = create_rect(PURPLE)
        layer1.add(rect for rect in stack_blocks(purple_start, 3))

        # Level 2: ORANGE (3 blocks)
        orange_start = create_rect(ORANGE)
        orange_start.move_to(layer1[-1]).shift(UP * 0.4 + LEFT * 0.4)
        layer1.add(rect for rect in stack_blocks(orange_start, 3))

        # Level 3: BLUE (3 blocks)
        blue_start = create_rect(BLUE)
        blue_start.move_to(layer1[-1]).shift(UP * 0.4 + LEFT * 0.4)
        layer1.add(rect for rect in stack_blocks(blue_start, 3))

        layer1.next_to(full2).shift(LEFT * 0.8)
        layer1.scale(0.2)


        # Layer 2.
        layer2 = layer1.copy()

        for i, mob in enumerate(layer2):
            mob.stretch_to_fit_width(mob.width + 0.3)

        layer2.next_to(layer1, RIGHT * 0.2)


        # Layer 3.
        layer3 = layer1.copy()

        for i, mob in enumerate(layer3):
            mob.stretch_to_fit_width(mob.width + 0.6)

        layer3.next_to(layer2, RIGHT * 2.2)

        # Layer 4.
        layer4 = layer1.copy()

        for i, mob in enumerate(layer4):
            mob.stretch_to_fit_width(mob.width + 0.9)

        layer4.next_to(layer3, RIGHT * 2)

        self.play(
            (Create(mob) for mob in reversed(layer1)),
            (Create(mob) for mob in reversed(layer2)),
            (Create(mob) for mob in reversed(layer3)),
            (Create(mob) for mob in reversed(layer4)),
        )
        self.wait(1)

        # Layers descriptions.
        layers_desc = VGroup(
            Tex(r"Reshape\\$[(a+13+128) \times 1 \times 2]$", font_size=15).next_to(layer1.get_bottom()).shift(DOWN * 0.3 + LEFT * 1.3),
            Tex(r"Trasp.Conv2D\\$[(a+13+128)\times 1\times 4]$", font_size=15).next_to(layer2.get_bottom()).shift(DOWN * 0.3 + LEFT * 0.5),
            Tex(r"Trasp.Conv2D\\$[(a+13+128)\times 1 \times 8]$", font_size=15).next_to(layer3.get_bottom()).shift(DOWN * 0.3 + LEFT * 0.5),
            Tex(r"Trasp.Conv2D\\$[(a+13+128)\times 1 \times 16]$", font_size=15).next_to(layer4.get_bottom()).shift(DOWN * 0.3 + LEFT * 0.5)
        )
        self.play(Write(layers_desc))
        self.wait(2)

        # Net output.
        non_mono.next_to(layer4).shift(RIGHT)
        non_mono_desc = VGroup(
            Tex(r"Non-monophonic\\output", font_size=15).next_to(non_mono, UP * 0.5),
            Tex(r"$[1 \times 128 \times 16]$", font_size=15).next_to(non_mono, DOWN * 0.5),
        )

        # Fake sample.
        fake = curr
        fake.next_to(non_mono).shift(RIGHT * 1.5)
        fake_desc = VGroup(
            Tex(r"Current (fake)\\melody bar", font_size=15).next_to(fake, UP * 0.5),
            Tex(r"$[1 \times 128 \times 16]$", font_size=15).next_to(fake, DOWN * 0.5),
        )

        # Monophonic.
        mono = Arrow(
                start=non_mono.get_right(),
                end=fake.get_left(),
                stroke_width=0.7,
                tip_length=0.1,
                buff=0.1
        )

        # Crate arrow between fully-connected and transp conv layers.
        gen_arrows = VGroup(
                Arrow(
                    start=full2.get_right(),
                    end=layer1.get_left(),
                    stroke_width=0.7,
                    tip_length=0.1,
                ),
                Arrow(
                    start=layer2.get_right(),
                    end=layer3.get_left(),
                    stroke_width=0.7,
                    tip_length=0.1,
                    buff=0
                ),
                Arrow(
                    start=layer3.get_right(),
                    end=layer4.get_left(),
                    stroke_width=0.7,
                    tip_length=0.1,
                    buff=0
                ),
                Arrow(
                    start=layer4.get_right(),
                    end=non_mono.get_left(),
                    stroke_width=0.7,
                    tip_length=0.1,
                    buff=0
                ),
        )
        self.play(FadeIn(gen_arrows))
        self.wait(1)

        # BN + LeakyReLU descriptions.
        self.play(
            Write(
                Tex(r"\texttt{BN + LReLU}", font_size=12)
                .next_to(arrow, UP).shift(DOWN * 0.2)
            )
            for arrow in gen_arrows
        )

        self.play(FadeIn(non_mono), Write(non_mono_desc))
        self.play(FadeIn(fake), Write(fake_desc))
        self.play(
            Create(mono),
            Write(
                Tex(r"Monophonic\\layer", font_size=15).move_to(mono.get_top()).shift(UP * 0.2)
            )
        )
        self.wait(3)

        ### CONNECTIONS ###
        dotted_lines = VGroup(
            create_4_elbows_line(
                start=cond_arrows[3].get_top() + UP * 0.2,
                end=layer1[-1].get_top(),
                shift1=UP * 0.2,
                shift2=RIGHT,
                shift3=DOWN * 1.5,
                shift4=LEFT * 8.9
            ),
            create_4_elbows_line(
                start=cond_arrows[2].get_top() + UP * 0.2,
                end=layer2[-1].get_top(),
                shift1=UP * 0.3,
                shift2=RIGHT * 3,
                shift3=DOWN * 1.8,
                shift4=LEFT * 8.3
            ),
            create_4_elbows_line(
                start=cond_arrows[1].get_top() + UP * 0.2,
                end=layer3[-1].get_top(),
                shift1=UP * 0.4,
                shift2=RIGHT * 5.7,
                shift3=DOWN * 2.1,
                shift4=LEFT * 7
            ),
            create_4_elbows_line(
                start=cond_arrows[0].get_top() + UP * 0.2,
                end=layer4[-1].get_top(),
                shift1=UP * 0.5,
                shift2=RIGHT * 8.7,
                shift3=DOWN * 2.4,
                shift4=LEFT * 5.4
            ),
        )
        self.play(Create(dotted_lines))
        self.wait(5)

    def discriminator(self):
        title = Title(r"Discriminator - Model v3", color=ORANGE)
        self.play(Write(title))

        # Input.
        input = Group(
            curr.next_to(title, DOWN).shift(LEFT * 3.8 + DOWN * 2),
        )
        for _ in range(3):
            new_rect = Rectangle(width=curr.width, stroke_width=1.5, height=curr.height, fill_color=ORANGE, fill_opacity=1)
            new_rect.move_to(input[-1]).shift(LEFT * 0.1 + UP * 0.1)
            input.add(new_rect)

        input_desc = VGroup(
            Tex(r"Input", font_size=15).next_to(input, UP * 0.5),
            Tex(r"$[(13 + 1)\times 128 \times 16]$", font_size=15)
            .next_to(input, DOWN * 0.5),
        )

        self.play(
                (FadeIn(mob) for mob in reversed(input)),
                Write(input_desc)
        )

        # 1D condition.
        oneDcond = Rectangle(width=0.5, stroke_width=1.5, height=0.1, fill_color=ORANGE, fill_opacity=1,)
        oneDcond.next_to(input_desc, UP * 1.5)
        oneDcond_desc = VGroup(
            Tex("Encoded Chord", font_size=15).move_to(oneDcond.get_top()).shift(UP * 0.1),
            Tex("13", font_size=15).move_to(oneDcond.get_bottom()).shift(DOWN * 0.1)
        )
        self.play(Create(oneDcond), Write(oneDcond_desc))
        self.wait(2)

        # Define layer1 and build in levels
        layer1 = VGroup()

        # Level 1 
        purple_start = create_rect(PURPLE)
        layer1.add(rect for rect in stack_blocks(purple_start, 3))

        # Level 3:
        blue_start = create_rect(ORANGE)
        blue_start.move_to(layer1[-1]).shift(UP * 0.4 + LEFT * 0.4)
        layer1.add(rect for rect in stack_blocks(blue_start, 3))

        layer1.next_to(curr)
        layer1.scale(0.2)
        for mob in layer1:
            mob.stretch_to_fit_width(mob.width + 0.9)


        # Layer 2.
        layer2 = layer1.copy()

        for i, mob in enumerate(layer2):
            mob.stretch_to_fit_width(mob.width - 0.3)

        layer2.next_to(layer1, RIGHT).shift(RIGHT)

        self.play(
            (Create(mob) for mob in reversed(layer1)),
            (Create(mob) for mob in reversed(layer2))
        )
        self.wait(1)

        # Layers descriptions.
        layers_desc = VGroup(
            Tex(r"Conv2D\\$[14 \times 1 \times 8]$", font_size=15).next_to(layer1.get_bottom()).shift(DOWN * 0.3 + LEFT * 0.5),
            Tex(r"Conv2D\\$[77\times 1 \times 3]$", font_size=15).next_to(layer2.get_bottom()).shift(DOWN * 0.3 + LEFT * 0.5),
        )
        self.play(Write(layers_desc))
        self.wait(2)

        # fully-connected 1.
        full1 = VGroup()
        f1_start = create_circ()
        full1.add(circ for circ in stack_circles(f1_start, 3))

        full1.next_to(layer2, RIGHT).shift(RIGHT * 1.5)
        self.play(Create(full1))

        # fully-connected 2.
        full2 = VGroup()
        f2_start = create_circ()
        full2.add(circ for circ in stack_circles(f2_start, 5))

        full2.next_to(full1).shift(RIGHT * 0.2)
        self.play(Create(full2))

        # fully-connected 3.
        full3 = create_circ()

        full3.next_to(full2).shift(RIGHT * 0.2)
        self.play(Create(full3))

        # Fully connected layer arrows.
        full_arrows = VGroup()

        for f1 in full1:
            for f2 in full2:
                arrow1 = Line(
                    start=f1.get_right(),
                    end=f2.get_left(),
                    stroke_width=0.5,
                )
                arrow2 = Line(
                    start=f2.get_right(),
                    end=full3,
                    stroke_width=0.5,
                )
                full_arrows.add(arrow1, arrow2)


        # Fully connected descriptions.
        fully_desc = VGroup(
            Tex("231", font_size=15).next_to(full1, DOWN).shift(UP * 0.2),
            Tex("1024", font_size=15).next_to(full2, DOWN).shift(UP * 0.2),
        )
        self.play(Create(full_arrows), Write(fully_desc))
        self.wait(2)

        # Crate arrow between fully-connected and transp conv layers.
        disc_arrows = VGroup(
                Arrow(
                    start=layer1.get_right(),
                    end=layer2.get_left(),
                    stroke_width=0.7,
                    tip_length=0.1,
                ),
                Arrow(
                    start=layer2.get_right(),
                    end=full1.get_left(),
                    stroke_width=0.7,
                    tip_length=0.1,
                ),
                Arrow(
                    start=full3.get_right(),
                    end=full3.get_right() + RIGHT,
                    stroke_width=0.7,
                    tip_length=0.1,
                ),
        )
        self.play(FadeIn(disc_arrows))

        # Dropout + LeakyReLU descriptions.
        self.play(
            Write(
                Tex(r"\texttt{LReLU + Dropout}", font_size=12)
                .next_to(disc_arrows[0], UP).shift(DOWN * 0.2)
            ),
            Write(
                Tex(r"\texttt{LReLU + Dropout, Flatten}", font_size=12)
                .next_to(disc_arrows[1], UP).shift(DOWN * 0.2)
            ),
            Write(
                Tex(r"\texttt{Sigmoid}", font_size=12)
                .next_to(disc_arrows[2], UP).shift(DOWN * 0.2)
            ),
            Write(
                Tex(r"$y\in[0,1]$", font_size=15)
                .next_to(disc_arrows[2], RIGHT)
            )
        )
        
        self.wait(5)
