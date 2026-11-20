from __future__ import annotations

import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from mathviz.cli import main


class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.output = os.path.join(self._tmp.name, "math.html")

    def run_cli(self, args):
        stdout = StringIO()
        stderr = StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(args)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_linear(self) -> None:
        code, output, _ = self.run_cli(["linear", "-k", "2", "-b", "1"])
        self.assertEqual(code, 0)
        self.assertIn("y = 2x + 1", output)
        self.assertIn("-0.5", output)

    def test_linear_horizontal(self) -> None:
        code, output, _ = self.run_cli(["linear", "-k", "0", "-b", "3"])
        self.assertEqual(code, 0)
        self.assertIn("与 x 轴无交点", output)

    def test_quadratic(self) -> None:
        code, output, _ = self.run_cli(
            ["quadratic", "-a", "1", "-b", "-2", "-c", "-3"]
        )
        self.assertEqual(code, 0)
        self.assertIn("顶点：(1, -4)", output)
        self.assertIn("x = -1", output)
        self.assertIn("x = 3", output)

    def test_quadratic_no_roots(self) -> None:
        code, output, _ = self.run_cli(["quadratic", "-a", "1", "-c", "1"])
        self.assertEqual(code, 0)
        self.assertIn("无实数根", output)

    def test_quadratic_invalid(self) -> None:
        code, _, stderr = self.run_cli(["quadratic", "-a", "0"])
        self.assertEqual(code, 2)
        self.assertIn("不能为 0", stderr)

    def test_inverse(self) -> None:
        code, output, _ = self.run_cli(["inverse", "-k", "-6"])
        self.assertEqual(code, 0)
        self.assertIn("第二、四象限", output)

    def test_pythagoras(self) -> None:
        code, output, _ = self.run_cli(["pythagoras", "-a", "3", "-b", "4"])
        self.assertEqual(code, 0)
        self.assertIn("c = 5", output)
        self.assertIn("9 + 16 = 25", output)

    def test_pythagoras_invalid(self) -> None:
        code, _, stderr = self.run_cli(["pythagoras", "-a", "0", "-b", "4"])
        self.assertEqual(code, 2)

    def test_histogram(self) -> None:
        code, output, _ = self.run_cli(
            ["histogram", "1", "2", "2", "3", "--bins", "2"]
        )
        self.assertEqual(code, 0)
        self.assertIn("共 4 个数据", output)
        self.assertIn("1 ~ 2", output)

    def test_histogram_invalid(self) -> None:
        code, _, stderr = self.run_cli(["histogram", "1", "--bins", "0"])
        self.assertEqual(code, 2)

    def test_html(self) -> None:
        code, output, _ = self.run_cli(["html", "-o", self.output])
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists(self.output))
        self.assertIn("已生成", output)
        with open(self.output, encoding="utf-8") as handle:
            content = handle.read()
        self.assertIn("勾股定理", content)

    def test_html_write_failure(self) -> None:
        bad = os.path.join(self._tmp.name, "missing", "page.html")
        code, _, stderr = self.run_cli(["html", "-o", bad])
        self.assertEqual(code, 1)
        self.assertIn("写入文件失败", stderr)


if __name__ == "__main__":
    unittest.main()
