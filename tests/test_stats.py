from __future__ import annotations

import math
import unittest

from mathviz.stats import StatsError, build_histogram, render_histogram_svg


class HistogramTest(unittest.TestCase):
    def test_counts(self) -> None:
        result = build_histogram([1, 2, 2, 3, 3, 3], bins=3)
        self.assertEqual(result.counts, (1, 2, 3))
        self.assertEqual(len(result.edges), 4)

    def test_mean_and_median(self) -> None:
        result = build_histogram([1, 2, 2, 3, 3, 3], bins=3)
        self.assertAlmostEqual(result.mean, 14.0 / 6.0)
        self.assertAlmostEqual(result.median, 2.5)

    def test_equal_values(self) -> None:
        result = build_histogram([5, 5], bins=2)
        self.assertEqual(result.minimum, 5.0)
        self.assertEqual(result.maximum, 5.0)
        self.assertEqual(sum(result.counts), 2)

    def test_max_value_goes_to_last_bin(self) -> None:
        result = build_histogram([1, 10], bins=3)
        self.assertEqual(result.counts[-1], 1)
        self.assertEqual(result.counts[0], 1)

    def test_invalid(self) -> None:
        with self.assertRaises(StatsError):
            build_histogram([], 5)
        with self.assertRaises(StatsError):
            build_histogram([1, 2], 0)
        with self.assertRaises(StatsError):
            build_histogram([1, 2], 21)
        with self.assertRaises(StatsError):
            build_histogram([1, math.inf], 5)

    def test_svg(self) -> None:
        svg = render_histogram_svg(build_histogram([1, 2, 2, 3], bins=2))
        self.assertTrue(svg.startswith("<svg"))
        self.assertEqual(svg.count("<rect"), 2)
        self.assertIn("平均", svg)
        self.assertIn("频数分布直方图", svg)


if __name__ == "__main__":
    unittest.main()
