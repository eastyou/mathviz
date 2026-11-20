from __future__ import annotations

import unittest

from mathviz.functions import inverse, linear, quadratic
from mathviz.geometry import solve_pythagoras
from mathviz.report import render_page
from mathviz.stats import build_histogram


class ReportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.page = render_page(
            linear(2, 1),
            quadratic(1, -2, -3),
            inverse(6),
            solve_pythagoras(3, 4),
            build_histogram([1, 2, 2, 3, 3, 3], 3),
            "数学复习",
        )

    def test_sections(self) -> None:
        for title in ("一次函数", "二次函数", "反比例函数", "勾股定理", "频数分布直方图"):
            self.assertIn(title, self.page)
        self.assertIn("数学复习", self.page)

    def test_key_values(self) -> None:
        self.assertIn("y = 2x + 1", self.page)
        self.assertIn("(1, -4)", self.page)
        self.assertIn("x = -1", self.page)
        self.assertIn("a² + b² = c²", self.page)
        self.assertIn("平均", self.page)

    def test_self_contained(self) -> None:
        self.assertTrue(self.page.startswith("<!doctype html>"))
        self.assertIn("<style>", self.page)
        self.assertNotIn("<link", self.page)
        self.assertNotIn("<script", self.page)

    def test_title_escaped(self) -> None:
        page = render_page(
            linear(1, 0),
            quadratic(1, 0, 1),
            inverse(-1),
            solve_pythagoras(1, 1),
            build_histogram([1], 1),
            "<img src=x>",
        )
        self.assertNotIn("<img src=x>", page)
        self.assertIn("&lt;img", page)


if __name__ == "__main__":
    unittest.main()
