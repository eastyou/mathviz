"""把函数图像、勾股定理与直方图汇总成一份可打印页面。"""

from __future__ import annotations

import html
from typing import Iterable, List

from .functions import (
    InverseInfo,
    LinearInfo,
    QuadraticInfo,
    render_plot_svg,
)
from .geometry import PythagorasResult, render_pythagoras_svg
from .stats import HistogramResult, render_histogram_svg

PAGE_CSS = """
  @page { size: A4 portrait; margin: 12mm; }
  * { box-sizing: border-box; }
  body {
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
    color: #202124;
    margin: 0;
    padding: 12mm;
    background: #f7f8fa;
  }
  h1 { font-size: 23px; margin: 0 0 4px; }
  .subtitle { color: #5f6368; font-size: 13px; margin: 0 0 18px; }
  h2 { font-size: 17px; margin: 26px 0 8px; border-left: 4px solid #1a73e8; padding-left: 8px; }
  .card {
    background: #fff; border: 1px solid #e0e3e8; border-radius: 8px;
    padding: 12px 14px; margin-bottom: 14px;
  }
  .card p.desc { font-size: 13px; color: #5f6368; line-height: 1.8; margin: 0 0 8px; }
  .card svg { max-width: 100%; height: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 6px; }
  th, td { border: 1px solid #d0d5dd; padding: 6px 8px; text-align: center; }
  th { background: #f1f3f4; font-weight: 600; }
  .note { color: #5f6368; font-size: 12px; line-height: 1.8; margin-top: 16px; }
  @media print {
    body { background: #fff; padding: 0; }
    .card { break-inside: avoid; }
  }
"""


def render_page(
    linear_info: LinearInfo,
    quadratic_info: QuadraticInfo,
    inverse_info: InverseInfo,
    pythagoras: PythagorasResult,
    histogram: HistogramResult,
    title: str = "初中数学可视化",
) -> str:
    """生成单文件 HTML 报告。"""
    linear_table = _table(
        ["斜率 k", "截距 b", "与 x 轴交点"],
        [[
            _number(linear_info.k),
            _number(linear_info.b),
            "无" if linear_info.x_intercept is None else _number(linear_info.x_intercept),
        ]],
    )

    roots = "、".join("x = %s" % _number(value) for value in quadratic_info.roots)
    quadratic_table = _table(
        ["顶点", "与 x 轴交点", "开口方向"],
        [[
            "(%s, %s)" % (_number(quadratic_info.vertex[0]), _number(quadratic_info.vertex[1])),
            roots if roots else "无实数根",
            "向上" if quadratic_info.a > 0 else "向下",
        ]],
    )

    inverse_table = _table(
        ["比例系数 k", "图像所在象限", "渐近线"],
        [[
            _number(inverse_info.k),
            "第一、三象限" if inverse_info.k > 0 else "第二、四象限",
            "x 轴与 y 轴",
        ]],
    )

    pythagoras_table = _table(
        ["直角边 a", "直角边 b", "斜边 c", "a² + b²", "c²"],
        [[
            _number(pythagoras.a),
            _number(pythagoras.b),
            _number(pythagoras.c),
            _number(pythagoras.area_a + pythagoras.area_b),
            _number(pythagoras.area_c),
        ]],
    )

    histogram_table = _table(
        ["数据个数", "平均数", "中位数", "最小值", "最大值"],
        [[
            str(len(histogram.values)),
            _number(histogram.mean),
            _number(histogram.median),
            _number(histogram.minimum),
            _number(histogram.maximum),
        ]],
    )

    body = (
        "<h1>%s</h1>"
        '<p class="subtitle">函数图像 · 勾股定理 · 频数分布 · 全部图形在本机生成</p>'
        "<h2>一次函数</h2>"
        '<div class="card">'
        '<p class="desc">一次函数 y = kx + b 的图像是一条直线。k 决定倾斜方向与程度，'
        "b 是直线与 y 轴交点的纵坐标。</p>"
        "%s%s</div>"
        "<h2>二次函数</h2>"
        '<div class="card">'
        '<p class="desc">二次函数 y = ax² + bx + c 的图像是抛物线。'
        "顶点坐标可由配方法或公式得到，a 的符号决定开口方向。</p>"
        "%s%s</div>"
        "<h2>反比例函数</h2>"
        '<div class="card">'
        '<p class="desc">反比例函数 y = k / x 的图像是双曲线，'
        "两支分别位于相对的象限，坐标轴是它的渐近线。</p>"
        "%s%s</div>"
        "<h2>勾股定理</h2>"
        '<div class="card">'
        '<p class="desc">直角三角形两条直角边的平方和等于斜边的平方。'
        "把三边分别向外作正方形，两个小正方形的面积之和正好等于大正方形的面积。</p>"
        "%s%s</div>"
        "<h2>频数分布直方图</h2>"
        '<div class="card">'
        '<p class="desc">把数据分成若干组，用矩形高度表示每组的频数。'
        "直方图适合观察数据集中在哪个区间、是否对称。</p>"
        "%s%s</div>"
        '<p class="note">本页为示例数据与示意图，适合课堂讲解或打印。'
        "函数图像使用统一的坐标比例，勾股图与直方图仅表示数量关系。</p>"
        % (
            html.escape(title),
            render_plot_svg(linear_info.plot),
            linear_table,
            render_plot_svg(quadratic_info.plot),
            quadratic_table,
            render_plot_svg(inverse_info.plot),
            inverse_table,
            render_pythagoras_svg(pythagoras),
            pythagoras_table,
            render_histogram_svg(histogram),
            histogram_table,
        )
    )

    return (
        "<!doctype html>\n"
        '<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
        "<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n%s\n</body>\n</html>\n"
        % (html.escape(title), PAGE_CSS, body)
    )


def _table(headers: Iterable[str], rows: Iterable[Iterable[str]]) -> str:
    head = "".join("<th>%s</th>" % html.escape(str(item)) for item in headers)
    body = "".join(
        "<tr>%s</tr>"
        % "".join("<td>%s</td>" % html.escape(str(cell)) for cell in row)
        for row in rows
    )
    return "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (head, body)


def _number(value: float) -> str:
    text = "%.2f" % value
    text = text.rstrip("0").rstrip(".")
    return text if text else "0"


__all__ = ["render_page"]
