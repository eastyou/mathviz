"""一次函数、二次函数与反比例函数的图像。"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

Point = Tuple[float, float]


class MathError(ValueError):
    """函数参数不合法。"""


@dataclass(frozen=True)
class PlotResult:
    """通用函数图像数据。"""

    kind: str
    label: str
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    segments: Tuple[Tuple[Point, ...], ...]
    features: Tuple[Tuple[float, float, str], ...] = ()
    vertical_asymptote: Optional[float] = None
    horizontal_asymptote: Optional[float] = None


@dataclass(frozen=True)
class LinearInfo:
    plot: PlotResult
    k: float
    b: float
    x_intercept: Optional[float]
    y_intercept: float


@dataclass(frozen=True)
class QuadraticInfo:
    plot: PlotResult
    a: float
    b: float
    c: float
    vertex: Point
    roots: Tuple[float, ...]


@dataclass(frozen=True)
class InverseInfo:
    plot: PlotResult
    k: float


def linear(
    k: float, b: float, x_min: float = -10.0, x_max: float = 10.0
) -> LinearInfo:
    """一次函数 y = kx + b。"""
    _validate_range(x_min, x_max)
    samples = 81
    segment = tuple(
        (x, k * x + b)
        for x in _linspace(x_min, x_max, samples)
    )
    values = [point[1] for point in segment]
    y_min, y_max = _padded_range(min(values), max(values))
    features: List[Tuple[float, float, str]] = []
    x_intercept: Optional[float] = None
    if k != 0:
        x_intercept = -b / k
        if x_min <= x_intercept <= x_max:
            features.append((x_intercept, 0.0, "与 x 轴交点"))
    if x_min <= 0 <= x_max:
        features.append((0.0, b, "与 y 轴交点"))
    plot = PlotResult(
        kind="linear",
        label=_linear_label(k, b),
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
        segments=(segment,),
        features=tuple(features),
    )
    return LinearInfo(plot, k, b, x_intercept, b)


def quadratic(
    a: float, b: float, c: float, x_min: float = -10.0, x_max: float = 10.0
) -> QuadraticInfo:
    """二次函数 y = ax² + bx + c。"""
    if a == 0:
        raise MathError("二次项系数 a 不能为 0")
    _validate_range(x_min, x_max)

    segment = tuple(
        (x, a * x * x + b * x + c)
        for x in _linspace(x_min, x_max, 161)
    )
    vertex = (-b / (2 * a), c - b * b / (4 * a))
    discriminant = b * b - 4 * a * c
    roots: Tuple[float, ...] = ()
    if discriminant > 1e-12:
        root = math.sqrt(discriminant)
        roots = ((-b - root) / (2 * a), (-b + root) / (2 * a))
    elif abs(discriminant) <= 1e-12:
        roots = (-b / (2 * a),)

    values = [point[1] for point in segment] + [vertex[1]]
    y_min, y_max = _padded_range(min(values), max(values))
    features: List[Tuple[float, float, str]] = [(vertex[0], vertex[1], "顶点")]
    for value in roots:
        if x_min <= value <= x_max:
            features.append((value, 0.0, "与 x 轴交点"))

    plot = PlotResult(
        kind="quadratic",
        label=_quadratic_label(a, b, c),
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
        segments=(segment,),
        features=tuple(features),
    )
    return QuadraticInfo(plot, a, b, c, vertex, roots)


def inverse(k: float, x_min: float = -10.0, x_max: float = 10.0) -> InverseInfo:
    """反比例函数 y = k / x。"""
    if k == 0:
        raise MathError("反比例系数 k 不能为 0")
    _validate_range(x_min, x_max)
    if x_min < 0 < x_max:
        segments = (
            tuple((x, k / x) for x in _linspace(x_min, -0.02, 80)),
            tuple((x, k / x) for x in _linspace(0.02, x_max, 80)),
        )
    else:
        segments = (tuple((x, k / x) for x in _linspace(x_min, x_max, 160)),)

    limit = min(20.0, max(2.0, abs(k) * 2.0))
    features: List[Tuple[float, float, str]] = []
    for factor in (1.0, -1.0):
        x = math.sqrt(abs(k)) * factor
        if x_min <= x <= x_max and abs(x) > 1e-9:
            features.append((x, k / x, "分支点"))

    plot = PlotResult(
        kind="inverse",
        label="y = %s / x" % _number(k),
        x_min=x_min,
        x_max=x_max,
        y_min=-limit,
        y_max=limit,
        segments=segments,
        features=tuple(features),
        vertical_asymptote=0.0 if x_min < 0 < x_max else None,
        horizontal_asymptote=0.0,
    )
    return InverseInfo(plot, k)


def render_plot_svg(plot: PlotResult, width: int = 640, height: int = 420) -> str:
    """把函数图像画成 SVG。"""
    left, right, top, bottom = 52.0, 20.0, 24.0, 44.0
    plot_width = 640 - left - right
    plot_height = 420 - top - bottom

    def px(x: float) -> float:
        return left + (x - plot.x_min) / (plot.x_max - plot.x_min) * plot_width

    def py(y: float) -> float:
        return top + (plot.y_max - y) / (plot.y_max - plot.y_min) * plot_height

    parts: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 640 420" role="img" aria-label="%s">'
        % (width, height, _escape(plot.label)),
        '<defs><clipPath id="plot-clip"><rect x="%.0f" y="%.0f" width="%.0f" '
        'height="%.0f"/></clipPath></defs>'
        % (left, top, plot_width, plot_height),
        '<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="#ffffff"/>'
        % (left, top, plot_width, plot_height),
    ]

    x_step = _nice_step(plot.x_max - plot.x_min)
    y_step = _nice_step(plot.y_max - plot.y_min)
    for tick in _ticks(plot.x_min, plot.x_max, x_step):
        x = px(tick)
        parts.append(
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#eef1f5"/>'
            % (x, top, x, top + plot_height)
        )
        parts.append(
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10" '
            'font-family="sans-serif" fill="#80868b">%s</text>'
            % (x, top + plot_height + 16, _number(tick))
        )
    for tick in _ticks(plot.y_min, plot.y_max, y_step):
        y = py(tick)
        parts.append(
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#eef1f5"/>'
            % (left, y, left + plot_width, y)
        )
        parts.append(
            '<text x="%.1f" y="%.1f" text-anchor="end" font-size="10" '
            'font-family="sans-serif" fill="#80868b">%s</text>'
            % (left - 6, y + 3, _number(tick))
        )

    if plot.x_min <= 0 <= plot.x_max:
        parts.append(
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#202124" '
            'stroke-width="1.4"/>' % (px(0), top, px(0), top + plot_height)
        )
    if plot.y_min <= 0 <= plot.y_max:
        parts.append(
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#202124" '
            'stroke-width="1.4"/>' % (left, py(0), left + plot_width, py(0))
        )

    if plot.vertical_asymptote is not None:
        x = px(plot.vertical_asymptote)
        parts.append(
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#d93025" '
            'stroke-width="1" stroke-dasharray="5 4"/>'
            % (x, top, x, top + plot_height)
        )
    if plot.horizontal_asymptote is not None:
        y = py(plot.horizontal_asymptote)
        parts.append(
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#d93025" '
            'stroke-width="1" stroke-dasharray="5 4"/>'
            % (left, y, left + plot_width, y)
        )

    parts.append('<g clip-path="url(#plot-clip)">')
    for segment in plot.segments:
        points = " ".join(
            "%.1f,%.1f" % (px(x), py(y))
            for x, y in segment
            if math.isfinite(x) and math.isfinite(y)
        )
        if points:
            parts.append(
                '<polyline points="%s" fill="none" stroke="#1a73e8" '
                'stroke-width="2.4"/>' % points
            )
    parts.append("</g>")

    for x, y, text in plot.features:
        if plot.x_min <= x <= plot.x_max and plot.y_min <= y <= plot.y_max:
            parts.append(
                '<circle cx="%.1f" cy="%.1f" r="3.5" fill="#d93025"/>'
                % (px(x), py(y))
            )
            parts.append(
                '<text x="%.1f" y="%.1f" font-size="11" font-family="sans-serif" '
                'fill="#d93025">%s</text>'
                % (px(x) + 7, py(y) - 7, _escape(text))
            )

    parts.append(
        '<text x="%.0f" y="%.0f" font-size="13" font-family="sans-serif" '
        'fill="#202124">%s</text>'
        % (left, top + 18, _escape(plot.label))
    )
    parts.append(
        '<text x="%.0f" y="%.0f" font-size="11" font-family="sans-serif" '
        'fill="#5f6368">x</text>' % (left + plot_width - 6, py(0) - 6 if plot.y_min <= 0 <= plot.y_max else top + 12)
    )
    parts.append(
        '<text x="%.0f" y="%.0f" font-size="11" font-family="sans-serif" '
        'fill="#5f6368">y</text>' % (px(0) - 12 if plot.x_min <= 0 <= plot.x_max else left - 20, top + 10)
    )
    parts.append("</svg>")
    return "".join(parts)


def _validate_range(x_min: float, x_max: float) -> None:
    if not math.isfinite(x_min) or not math.isfinite(x_max):
        raise MathError("x 的范围必须是有限数字")
    if x_min >= x_max:
        raise MathError("x 的最小值必须小于最大值")
    if x_max - x_min > 10000:
        raise MathError("x 的范围过大，请控制在 10000 以内")


def _linspace(start: float, stop: float, count: int) -> List[float]:
    if count <= 1:
        return [start]
    step = (stop - start) / (count - 1)
    return [start + step * index for index in range(count)]


def _padded_range(low: float, high: float) -> Tuple[float, float]:
    if not math.isfinite(low) or not math.isfinite(high):
        raise MathError("函数值超出可绘制范围")
    if abs(high - low) < 1e-9:
        return low - 1.0, high + 1.0
    padding = (high - low) * 0.12
    return low - padding, high + padding


def _nice_step(span: float) -> float:
    if span <= 0:
        return 1.0
    raw = span / 10.0
    magnitude = 10 ** math.floor(math.log10(raw))
    for multiplier in (1, 2, 5, 10):
        if raw <= multiplier * magnitude:
            return multiplier * magnitude
    return 10 * magnitude


def _ticks(low: float, high: float, step: float) -> List[float]:
    if step <= 0:
        return []
    start = math.ceil(low / step) * step
    result: List[float] = []
    tick = start
    while tick <= high + 1e-9 and len(result) < 40:
        if abs(tick) < 1e-9:
            result.append(0.0)
        else:
            result.append(round(tick, 10))
        tick += step
    return result


def _linear_label(k: float, b: float) -> str:
    if k == 0:
        return "y = %s" % _number(b)
    term = "x" if k == 1 else ("-x" if k == -1 else "%sx" % _number(k))
    if b == 0:
        return "y = %s" % term
    if b > 0:
        return "y = %s + %s" % (term, _number(b))
    return "y = %s - %s" % (term, _number(abs(b)))


def _quadratic_label(a: float, b: float, c: float) -> str:
    parts: List[str] = []
    if a == 1:
        parts.append("x²")
    elif a == -1:
        parts.append("-x²")
    else:
        parts.append("%sx²" % _number(a))
    if b != 0:
        parts.append(("+ " if b > 0 else "- ") + ("x" if abs(b) == 1 else "%sx" % _number(abs(b))))
    if c != 0:
        parts.append(("+ " if c > 0 else "- ") + _number(abs(c)))
    return "y = " + " ".join(parts)


def _number(value: float) -> str:
    if abs(value) < 1e-9:
        return "0"
    text = "%.2f" % value
    text = text.rstrip("0").rstrip(".")
    return text


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


__all__ = [
    "InverseInfo",
    "LinearInfo",
    "MathError",
    "PlotResult",
    "QuadraticInfo",
    "inverse",
    "linear",
    "quadratic",
    "render_plot_svg",
]
