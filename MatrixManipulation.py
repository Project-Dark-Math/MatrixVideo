from manim import *
import numpy as np
from itertools import product


pMatrix = lambda mat, *args, **kwargs: Matrix(
    mat, *args, **kwargs, left_bracket="(", right_bracket=")"
)


class ShowMatrix(Scene):
    def construct(self):
        mat = pMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

        self.play(Write(mat), run_time=2)
        self.wait()
        self.play(Indicate(mat))
        self.wait()


class MatrixComponents(Scene):
    def construct(self):
        mat = pMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        brakets = mat.get_brackets()
        rows = mat.get_rows()
        columns = mat.get_columns()

        self.play(FadeIn(mat))
        self.wait()
        for entry in mat[0]:
            self.play(Indicate(entry), run_time=0.5)
        self.wait()
        self.play(Indicate(brakets[0]))
        self.play(Indicate(brakets[1]))
        self.wait()
        self.play(Indicate(rows[0]))
        self.play(Indicate(rows[1]))
        self.play(Indicate(rows[2]))
        self.wait()
        self.play(Indicate(columns[0]))
        self.play(Indicate(columns[1]))
        self.play(Indicate(columns[2]))
        self.wait()


class MatrixTranspose(Scene):
    def construct(self):
        # dimension of matrix : n * m
        n, m = 4, 5

        npmat = np.array([[(i + 1) ** j for j in range(m)] for i in range(n)])

        mat1 = pMatrix(npmat)
        mat2 = pMatrix(npmat.T)

        x1 = mat1[0][0].get_x()
        x2 = mat2[0][0].get_x()
        y1 = mat1[0][0].get_y()
        y2 = mat2[0][0].get_y()

        xm = (x1 + x2) / 2
        ym = (y1 + y2) / 2

        mat1.shift(RIGHT * (xm - x1) + UP * (ym - y1))
        mat2.shift(RIGHT * (xm - x2) + UP * (ym - y2))

        # self.add(mat1, mat2)
        # self.wait()
        self.play(FadeIn(mat1))
        self.wait()
        self.play(FadeOut(mat1[1]), run_time=0.5)
        self.play(FadeOut(mat1[2]), run_time=0.5)
        self.wait()

        transposeAnimations = [
            ReplacementTransform(mat1.get_rows()[i][j], mat2.get_rows()[j][i])
            for i, j in product(range(n), range(m))
        ]
        self.play(*transposeAnimations, run_time=2)
        self.wait()
        self.play(FadeIn(mat2[1]), run_time=0.5)
        self.play(FadeIn(mat2[2]), run_time=0.5)
        self.wait()


class MatrixMultiplication(Scene):
    def construct(self):
        n, k, m = 3, 5, 4
        np.random.seed(0)
        npmat1 = np.random.randint(-10, 10, size=(n, k))
        npmat2 = np.random.randint(-10, 10, size=(k, m))
        npmat3 = npmat1 @ npmat2

        mat1, mat2, mat3 = pMatrix(npmat1), pMatrix(npmat2), pMatrix(npmat3)
        mat1.scale(0.6)
        mat2.scale(0.6)
        mat3.scale(0.6)

        eq = VGroup(mat1, mat2, MathTex("="), mat3)
        eq.arrange(RIGHT)

        rowRectangles = [
            BackgroundRectangle(
                row, color=YELLOW, fill_opacity=0.5, corner_radius=0.05, buff=0.1
            )
            for row in mat1.get_rows()
        ]
        columnRectangles = [
            BackgroundRectangle(
                column, color=YELLOW, fill_opacity=0.5, corner_radius=0.05, buff=0.1
            )
            for column in mat2.get_columns()
        ]

        tmpmat1, tmpmat2 = mat1.copy(), mat2.copy()
        tmpgroup = VGroup(tmpmat1, tmpmat2)
        tmpgroup.arrange(RIGHT)

        self.play(Create(tmpgroup), run_time=2)
        self.wait()
        self.play(
            ReplacementTransform(tmpmat1, mat1), ReplacementTransform(tmpmat2, mat2)
        )
        self.wait()
        self.play(Create(eq[2]))
        self.play(FadeIn(eq[3][1]))
        self.play(FadeIn(eq[3][2]))
        self.wait()

        for i, j in product(range(n), range(m)):
            self.play(
                FadeIn(rowRectangles[i]), FadeIn(columnRectangles[j]), run_time=0.5
            )
            self.play(Write(mat3.get_rows()[i][j]))
            self.play(
                FadeOut(rowRectangles[i]), FadeOut(columnRectangles[j]), run_time=0.5
            )
            self.wait(0.1)
        self.wait()


class ElementaryRowOps(Scene):
    def construct(self):
        n,m = 4,5
        np.random.seed(0)

        

