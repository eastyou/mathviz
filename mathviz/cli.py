"""命令行入口：函数图像、勾股定理与直方图。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .functions import MathError, inverse, linear, quadratic
from .geometry import GeometryError, solve_pythagoras
from .report import render_page
from .stats import StatsError, build_histogram


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mathviz",
        description="初中数学可视化：函数图像、勾股定理、频数分布直方图",
    )
    parser.add_argument("--version", action="version", version="mathviz 0.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    linear_parser = subparsers.add_parser("linear", help="一次函数")
    linear_parser.add_argument("-k", type=float, required=True, help="斜率")
    linear_parser.add_argument("-b", type=float, default=0.0, help="截距")
    _add_range(linear_parser)

    quadratic_parser = subparsers.add_parser("quadratic", help="二次函数")
    quadratic_parser.add_argument("-a", type=float, required=True, help="二次项系数")
    quadratic_parser.add_argument("-b", type=float, default=0.0, help="一次项系数")
    quadratic_parser.add_argument("-c", type=float, default=0.0, help="常数项")
    _add_range(quadratic_parser)

    inverse_parser = subparsers.add_parser("inverse", help="反比例函数")
    inverse_parser.add_argument("-k", type=float, required=True, help="比例系数")
    _add_range(inverse_parser)

    pythagoras_parser = subparsers.add_parser("pythagoras", help="勾股定理")
    pythagoras_parser.add_argument("-a", type=float, required=True, help="直角边 a")
    pythagoras_parser.add_argument("-b", type=float, required=True, help="直角边 b")

    histogram_parser = subparsers.add_parser("histogram", help="频数分布直方图")
    histogram_parser.add_argument("values", nargs="+", type=float, help="数据")
    histogram_parser.add_argument("--bins", type=int, default=5, help="分组数")

    html_parser = subparsers.add_parser("html", help="生成示例可视化页面")
    html_parser.add_argument(
        "-o", "--output", default="mathviz.html", help="输出 HTML 路径"
    )
    html_parser.add_argument("--title", default="初中数学可视化", help="页面标题")
    return parser


def _add_range(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--xmin", type=float, default=-10.0, help="x 范围最小值")
    parser.add_argument("--xmax", type=float, default=10.0, help="x 范围最大值")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "linear":
            info = linear(args.k, args.b, args.xmin, args.xmax)
            print(info.plot.label)
            print("与 y 轴交点：(0, %s)" % _number(info.y_intercept))
            if info.x_intercept is None:
                print("与 x 轴无交点" if info.k == 0 else "与 x 轴交点在范围外")
            else:
                print("与 x 轴交点：(%s, 0)" % _number(info.x_intercept))
            return 0
        if args.command == "quadratic":
            info = quadratic(args.a, args.b, args.c, args.xmin, args.xmax)
            print(info.plot.label)
            print("顶点：(%s, %s)" % (_number(info.vertex[0]), _number(info.vertex[1])))
            if info.roots:
                print(
                    "与 x 轴交点："
                    + "、".join("x = %s" % _number(value) for value in info.roots)
                )
            else:
                print("与 x 轴无交点（无实数根）")
            return 0
        if args.command == "inverse":
            info = inverse(args.k, args.xmin, args.xmax)
            quadrant = "第一、三象限" if args.k > 0 else "第二、四象限"
            print(info.plot.label)
            print("图像位于%s，坐标轴是渐近线" % quadrant)
            return 0
        if args.command == "pythagoras":
            result = solve_pythagoras(args.a, args.b)
            print(
                "c = %s，%s² + %s² = %s²"
                % (
                    _number(result.c),
                    _number(result.a),
                    _number(result.b),
                    _number(result.c),
                )
            )
            print(
                "面积：%s + %s = %s"
                % (
                    _number(result.area_a),
                    _number(result.area_b),
                    _number(result.area_c),
                )
            )
            return 0
        if args.command == "histogram":
            result = build_histogram(args.values, args.bins)
            print(
                "共 %d 个数据，平均数 %s，中位数 %s"
                % (len(result.values), _number(result.mean), _number(result.median))
            )
            for index, count in enumerate(result.counts):
                print(
                    "  %s ~ %s：%d 个"
                    % (
                        _number(result.edges[index]),
                        _number(result.edges[index + 1]),
                        count,
                    )
                )
            return 0
        if args.command == "html":
            return _run_html(args)
    except (MathError, GeometryError, StatsError) as exc:
        print("错误: %s" % exc, file=sys.stderr)
        return 2
    return 2


def _run_html(args: argparse.Namespace) -> int:
    if not args.title.strip():
        print("错误: 页面标题不能为空", file=sys.stderr)
        return 2
    page = render_page(
        linear(2.0, 1.0),
        quadratic(1.0, -2.0, -3.0),
        inverse(6.0),
        solve_pythagoras(3.0, 4.0),
        build_histogram([72, 75, 78, 80, 80, 82, 85, 88, 90, 95], 5),
        args.title,
    )
    try:
        Path(args.output).write_text(page, encoding="utf-8")
    except OSError as exc:
        print("错误: 写入文件失败: %s" % exc, file=sys.stderr)
        return 1
    print("已生成 %s" % args.output)
    return 0


def _number(value: float) -> str:
    text = "%.2f" % value
    text = text.rstrip("0").rstrip(".")
    return text if text else "0"


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
