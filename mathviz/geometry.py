"""勾股定理的图形演示。"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Tuple


class GeometryError(ValueError):
    """几何参数不合法。"""


@dataclass(frozen=True)
class PythagorasResult:
    """直角三角形三边与三个正方形的面积。"""

    a: float
    b: float
    c: float
    area_a: float
    area_b: float
    area_c: float


def solve_pythagoras(a: float, b: float) -> PythagorasResult:
    """已知两条直角边，计算斜边与三个正方形的面积。"""
    if not math.isfinite(a) or not math.isfinite(b):
        raise GeometryError("边长必须是有限数字")
    if a <= 0 or b <= 0:
        raise GeometryError("直角边必须大于 0")
    if a > 1000 or b > 1000:
        raise GeometryError("边长过大，请控制在 1000 以内")
    c = math.hypot(a, b)
    return PythagorasResult(a, b, c, a * a, b * b, c * c)


def render_pythagoras_svg(
    result: PythagorasResult, width: int = 640, height: int = 400
) -> str:
    """画「三个正方形围住直角三角形」的经典图。"""
    a, b, c = result.a, result.b, result.c
    x_min, x_max = -b, a + b
    y_min, y_max = -a, a + b
    scale = min(560.0 / (x_max - x_min), 320.0 / (y_max - y_min), 60.0)
    mid_x = (x_min + x_max) / 2
    mid_y = (y_min + y_max) / 2

    def sx(x: float) -> float:
        return 320 + (x - mid_x) * scale

    def sy(y: float) -> float:
        return 200 - (y - mid_y) * scale

    def polygon(points: List[Tuple[float, float]], fill: str, stroke: str) -> str:
        return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (
            " ".join("%.1f,%.1f" % (sx(x), sy(y)) for x, y in points),
            fill,
            stroke,
        )

    parts: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 640 400" role="img" aria-label="勾股定理面积演示">'
        % (width, height),
        polygon([(0, 0), (a, 0), (a, -a), (0, -a)], "#dbe6f5", "#1a73e8"),
        polygon([(0, 0), (0, b), (-b, b), (-b, 0)], "#dcefdc", "#188038"),
        polygon(
            [(a, 0), (0, b), (b, b + a), (a + b, a)],
            "#fde7c8",
            "#f29900",
        ),
        polygon([(0, 0), (a, 0), (0, b)], "#ffffff", "#202124"),
    ]

    size = 13
    parts.append(
        '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%d" '
        'font-family="sans-serif" fill="#1a73e8">a² = %s</text>'
        % (sx(a / 2), sy(-a / 2) + 4, size, _number(result.area_a))
    )
    parts.append(
        '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%d" '
        'font-family="sans-serif" fill="#188038">b² = %s</text>'
        % (sx(-b / 2), sy(b / 2) + 4, size, _number(result.area_b))
    )
    parts.append(
        '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="%d" '
        'font-family="sans-serif" fill="#b06000">c² = %s</text>'
        % (sx((a + b) / 2), sy((a + b) / 2) + 4, size, _number(result.area_c))
    )

    parts.append(
        '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="12" '
        'font-family="sans-serif" fill="#5f6368">a = %s</text>'
        % (sx(a / 2), sy(0) + 18, _number(a))
    )
    parts.append(
        '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="12" '
        'font-family="sans-serif" fill="#5f6368">b = %s</text>'
        % (sx(0) - 18, sy(b / 2) + 4, _number(b))
    )
    parts.append(
        '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="12" '
        'font-family="sans-serif" fill="#5f6368">c = %s</text>'
        % (
            sx(a / 2 + b * 0.06) + 10,
            sy(b / 2 + a * 0.06) - 4,
            _number(c),
        )
    )

    marker = min(a, b) * 0.12
    parts.append(
        '<polyline points="%s" fill="none" stroke="#202124" stroke-width="1"/>'
        % " ".join(
            "%.1f,%.1f" % (sx(x), sy(y))
            for x, y in ((marker, 0), (marker, marker), (0, marker))
        )
    )

    parts.append(
        '<text x="20" y="28" font-size="15" font-family="sans-serif" '
        'fill="#202124">a² + b² = c²：%s² + %s² = %s²</text>'
        % (_number(a), _number(b), _number(c))
    )
    parts.append(
        '<text x="20" y="382" font-size="12" font-family="sans-serif" '
        'fill="#5f6368">两个小正方形的面积之和，等于斜边上正方形的面积：'
        "%s + %s = %s</text>"
        % (_number(result.area_a), _number(result.area_b), _number(result.area_c))
    )
    parts.append("</svg>")
    return "".join(parts)


def _number(value: float) -> str:
    text = "%.2f" % value
    text = text.rstrip("0").rstrip(".")
    return text if text else "0"


__all__ = ["GeometryError", "PythagorasResult", "render_pythagoras_svg", "solve_pythagoras"]
