from __future__ import annotations

import unittest

from mathviz.geometry import (
    GeometryError,
    render_pythagoras_svg,
    solve_pythagoras,
)


class PythagorasTest(unittest.TestCase):
    def test_three_four_five(self) -> None:
        result = solve_pythagoras(3, 4)
        self.assertAlmostEqual(result.c, 5.0)
        self.assertAlmostEqual(result.area_a, 9.0)
        self.assertAlmostEqual(result.area_b, 16.0)
        self.assertAlmostEqual(result.area_c, 25.0)
        self.assertAlmostEqual(result.area_a + result.area_b, result.area_c)

    def test_equal_legs(self) -> None:
        result = solve_pythagoras(1, 1)
        self.assertAlmostEqual(result.c, 2 ** 0.5)

    def test_invalid(self) -> None:
        with self.assertRaises(GeometryError):
            solve_pythagoras(0, 4)
        with self.assertRaises(GeometryError):
            solve_pythagoras(3, -4)
        with self.assertRaises(GeometryError):
            solve_pythagoras(2000, 4)

    def test_svg(self) -> None:
        svg = render_pythagoras_svg(solve_pythagoras(3, 4))
        self.assertTrue(svg.startswith("<svg"))
        self.assertEqual(svg.count("<polygon"), 4)
        self.assertIn("a² = 9", svg)
        self.assertIn("b² = 16", svg)
        self.assertIn("c² = 25", svg)
        self.assertIn("3² + 4² = 5²", svg)


if __name__ == "__main__":
    unittest.main()
