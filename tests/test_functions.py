from __future__ import annotations

import math
import unittest

from mathviz.functions import (
    MathError,
    inverse,
    linear,
    quadratic,
    render_plot_svg,
)


class LinearTest(unittest.TestCase):
    def test_basic(self) -> None:
        info = linear(2, 1)
        self.assertEqual(info.plot.label, "y = 2x + 1")
        self.assertAlmostEqual(info.x_intercept or 0.0, -0.5)
        self.assertAlmostEqual(info.y_intercept, 1.0)
        self.assertEqual(len(info.plot.segments[0]), 81)

    def test_horizontal_line(self) -> None:
        info = linear(0, 3)
        self.assertEqual(info.plot.label, "y = 3")
        self.assertIsNone(info.x_intercept)

    def test_through_origin(self) -> None:
        info = linear(-1, 0)
        self.assertEqual(info.plot.label, "y = -x")

    def test_invalid_range(self) -> None:
        with self.assertRaises(MathError):
            linear(1, 0, 10, -10)
        with self.assertRaises(MathError):
            linear(1, 0, -10000, 10000)
        with self.assertRaises(MathError):
            linear(1, 0, -math.inf, 10)


class QuadraticTest(unittest.TestCase):
    def test_vertex_and_roots(self) -> None:
        info = quadratic(1, -2, -3)
        self.assertEqual(info.plot.label, "y = x² - 2x - 3")
        self.assertAlmostEqual(info.vertex[0], 1.0)
        self.assertAlmostEqual(info.vertex[1], -4.0)
        self.assertEqual(len(info.roots), 2)
        self.assertAlmostEqual(info.roots[0], -1.0)
        self.assertAlmostEqual(info.roots[1], 3.0)

    def test_no_real_roots(self) -> None:
        info = quadratic(1, 0, 1)
        self.assertEqual(info.roots, ())

    def test_double_root(self) -> None:
        info = quadratic(1, -2, 1)
        self.assertEqual(len(info.roots), 1)
        self.assertAlmostEqual(info.roots[0], 1.0)

    def test_zero_quadratic_coefficient(self) -> None:
        with self.assertRaises(MathError):
            quadratic(0, 1, 1)

    def test_label_with_plus(self) -> None:
        info = quadratic(1, 1, 1)
        self.assertEqual(info.plot.label, "y = x² + x + 1")


class InverseTest(unittest.TestCase):
    def test_basic(self) -> None:
        info = inverse(6)
        self.assertEqual(info.plot.label, "y = 6 / x")
        self.assertEqual(len(info.plot.segments), 2)
        self.assertEqual(info.plot.vertical_asymptote, 0.0)
        self.assertEqual(info.plot.horizontal_asymptote, 0.0)

    def test_single_branch(self) -> None:
        info = inverse(6, 1, 10)
        self.assertEqual(len(info.plot.segments), 1)
        self.assertIsNone(info.plot.vertical_asymptote)

    def test_zero_k(self) -> None:
        with self.assertRaises(MathError):
            inverse(0)


class PlotSvgTest(unittest.TestCase):
    def test_linear_svg(self) -> None:
        svg = render_plot_svg(linear(2, 1).plot)
        self.assertTrue(svg.startswith("<svg"))
        self.assertIn("y = 2x + 1", svg)
        self.assertEqual(svg.count("<polyline"), 1)
        self.assertIn("与 y 轴交点", svg)

    def test_quadratic_svg(self) -> None:
        svg = render_plot_svg(quadratic(1, -2, -3).plot)
        self.assertIn("顶点", svg)

    def test_inverse_svg(self) -> None:
        svg = render_plot_svg(inverse(6).plot)
        self.assertEqual(svg.count("<polyline"), 2)
        self.assertIn("stroke-dasharray", svg)


if __name__ == "__main__":
    unittest.main()
