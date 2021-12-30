from manim import *

# Frame infomations
frame_width = config["frame_width"]
frame_height = config["frame_height"]


class MatrixExample(Scene):
    def construct(self):

        text1 = Tex("What is the point about matrix multiplication?").shift(UP * 0.1)
        text2 = Tex("Why the definition is somewhat weird?").next_to(
            text1, DOWN, buff=0.2
        )

        self.play(Write(text1))
        self.wait()
        self.play(Write(text2))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))
        self.wait()

        ###################################################
        # slideshows which shows how this video will play #
        ###################################################
        # A ratio of shrinking
        slide_frame_width = (frame_width - 1.2) / 3
        width_ratio = slide_frame_width / frame_width

        kwargs = {
            "corner_radius": 0.5,
            "stroke_color": YELLOW_C,
            "stroke_width": 2,
            "width": frame_width,
            "height": frame_height,
        }

        ######### MINI FRAME 1 ####
        matrix_explain_frame = RoundedRectangle(**kwargs)
        matrix_explain_inner = MatrixFrame()
        first_title = MatrixFrame()
        matrix_explain = (
            VGroup(matrix_explain_frame, matrix_explain_inner)
            .scale(width_ratio)
            .to_edge(UL, buff=0.1)
        )
        matrix_explain_inner.recorded_center = matrix_explain.get_center()
        move_val = matrix_explain_inner.move_val
        opacity_val = matrix_explain_inner.opacity_val

        ######### MINI FRAME 2 ####
        transform_frame = RoundedRectangle(**kwargs)
        transform_inner = LinearTransfromExplain()
        transform_explain = (
            VGroup(transform_frame, transform_inner)
            .scale(width_ratio)
            .to_edge(UP, buff=0.1)
        )
        transform_inner.recorded_center = transform_explain.get_center()
        transform_inner.render_ratio = width_ratio
        move_point = transform_inner.move_point

        ######### MINI FRAME 3 ####
        visual_frame = RoundedRectangle(**kwargs)
        visual_inner = LinearVisualization()
        visual_explain = (
            VGroup(visual_frame, visual_inner).scale(width_ratio).to_edge(UR, buff=0.1)
        )

        intro_text = (
            Tex("These give the reason why the matrix multiplication is defined")
            .scale(0.7)
            .to_edge(DOWN, buff=2)
        )

        arrow1 = Arrow(start=intro_text.get_top(), end=matrix_explain.get_bottom())
        arrow2 = Arrow(start=intro_text.get_top(), end=transform_explain.get_bottom())
        arrow3 = Arrow(start=intro_text.get_top(), end=visual_explain.get_bottom())
        arrows = VGroup(arrow1, arrow2, arrow3)

        self.play(
            LaggedStart(
                Create(matrix_explain),
                Create(transform_explain),
                Create(visual_explain),
                Write(intro_text),
                Create(arrows),
            ),
            run_time=4,
            lag_ratio=0.7,
        )
        self.play(
            move_val.animate.set_value(0.43),
            opacity_val.animate.set_value(1),
            move_point.animate.set_value(1),
        )
        self.wait(2)

        self.play(
            FadeOut(transform_explain),
            FadeOut(visual_explain),
            FadeOut(intro_text),
            FadeOut(arrows),
            ReplacementTransform(matrix_explain, first_title),
        )
        self.wait()


class MatrixFrame(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Value Trackers
        move_val = ValueTracker(0)
        opacity_val = ValueTracker(0)

        # Make Objects
        matrix_explain_text = Tex("Matrix Multiplication").to_edge(UP, buff=1)
        matrix_mul = MathTex(
            r"\begin{bmatrix}1&2\\3&4\\\end{bmatrix}\begin{bmatrix}5&6\\7&8\end{bmatrix}"
        )
        equality = MathTex("=", fill_opacity=0.0).next_to(matrix_mul, buff=0.1)
        output_matrix = MathTex(
            r"\begin{bmatrix}19&22\\43&50\\\end{bmatrix}", fill_opacity=0.0
        ).next_to(equality, buff=0.1)

        # Record the initial location of matrix_mul
        recorded_center = matrix_mul.get_center()

        # Assign Updater
        matrix_mul.add_updater(
            lambda mob: mob.move_to(
                [
                    self.recorded_center[0] - self.move_val.get_value(),
                    self.recorded_center[1],
                    0,
                ]
            )
        )
        equality.add_updater(
            lambda mob: mob.set_opacity(self.opacity_val.get_value()).next_to(
                matrix_mul, buff=0.1
            )
        )
        output_matrix.add_updater(
            lambda mob: mob.set_opacity(self.opacity_val.get_value()).next_to(
                equality, buff=0.1
            )
        )

        vts = Group(move_val, opacity_val)
        self.move_val = move_val
        self.opacity_val = opacity_val
        self.recorded_center = recorded_center
        self.add(matrix_explain_text, equality, matrix_mul, output_matrix)


class LinearTransfromExplain(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Value Tracker
        move_point = ValueTracker(0)  # 0 <= move_point <= 1

        # Make Objects
        transform_def_explain_text = Tex(
            "A definition of the linear transform"
        ).to_edge(UP, buff=1)
        def_of_transform = MathTex(r"T: \mathbb{R}^m\to\mathbb{R}^n").next_to(
            transform_def_explain_text, DOWN, buff=0.5
        )
        axes = (
            Axes(
                x_range=[-2, 2],
                x_length=3,
                y_range=[-2, 2],
                y_length=3,
                tips=False,
            )
            .add_coordinates()
            .move_to(RIGHT * 2.5 + DOWN * 1)
        )
        number_line = NumberLine(
            x_range=[-2, 2],
            length=3,
            include_numbers=True,
        ).move_to(LEFT * 2.5 + DOWN * 1.2)
        a_dot = Dot(LEFT * 3 + DOWN * 1, color=GREEN_B)

        # Record the initial location of a_dot
        recorded_center = a_dot.get_center()

        # Assign Updater
        a_dot.add_updater(
            lambda mob: mob.move_to(
                [
                    self.recorded_center[0]
                    + (-3 + 6 * self.move_point.get_value() ** 2) * self.render_ratio,
                    self.recorded_center[1]
                    + (
                        -1
                        + 2 * self.move_point.get_value()
                        - self.move_point.get_value() ** 2
                    )
                    * self.render_ratio,
                    0,
                ]
            )
        )

        self.render_ratio = 1
        self.move_point = move_point
        self.recorded_center = recorded_center
        self.add(transform_def_explain_text, def_of_transform, number_line, axes, a_dot)


class LinearVisualization(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Make Objects
        visual_text = Tex("Visualization of Matrix Multiplication").to_edge(
            UL, buff=0.2
        )
        axes = Axes(
            x_range=[-5, 5], x_length=10, y_range=[-3, 3], y_length=6
        ).add_coordinates()
        helper_lines = VGroup()
        for i in range(-5, 6):
            helper_lines += Line(
                start=[i, -3, 0], end=[i, 3, 0], stroke_color=BLUE_C, stroke_width=0.5
            )
        for i in range(-3, 4):
            helper_lines += Line(
                start=[-5, i, 0], end=[5, i, 0], stroke_color=BLUE_C, stroke_width=0.5
            )

        self.add(visual_text, axes, helper_lines)
