"""数据的频数分布直方图。"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass
from typing import List, Sequence, Tuple


class StatsError(ValueError):
    """统计数据不合法。"""


@dataclass(frozen=True)
class HistogramResult:
    """一组数据的直方图与基本统计量。"""

    values: Tuple[float, ...]
    edges: Tuple[float, ...]
    counts: Tuple[int, ...]
    mean: float
    median: float
    minimum: float
    maximum: float


def build_histogram(values: Sequence[float], bins: int = 5) -> HistogramResult:
    """把数据分成 ``bins`` 个等宽区间并统计频数。"""
    if not values:
        raise StatsError("至少需要一个数据")
    if bins <= 0:
        raise StatsError("分组数必须大于 0")
    if bins > 20:
        raise StatsError("分组数最多 20 个")

    numbers = [float(value) for value in values]
    for value in numbers:
        if not math.isfinite(value):
            raise StatsError("数据必须是有限数字")

    low = min(numbers)
    high = max(numbers)
    if abs(high - low) < 1e-12:
        low -= 0.5
        high += 0.5

    width = (high - low) / bins
    edges = tuple(low + width * index for index in range(bins + 1))
    counts = [0] * bins
    for value in numbers:
        index = int((value - low) / width)
        if index >= bins:
            index = bins - 1
        if index < 0:
            index = 0
        counts[index] += 1

    return HistogramResult(
        values=tuple(numbers),
        edges=edges,
        counts=tuple(counts),
        mean=sum(numbers) / len(numbers),
        median=statistics.median(numbers),
        minimum=min(numbers),
        maximum=max(numbers),
    )


def render_histogram_svg(result: HistogramResult, width: int = 640, height: int = 340) -> str:
    """画直方图并标出平均数。"""
    left, right, top, bottom = 56.0, 20.0, 34.0, 62.0
    plot_width = 640 - left - right
    plot_height = 340 - top - bottom
    bins = len(result.counts)
    max_count = max(result.counts) if result.counts else 0
    y_max = max(1, max_count)

    parts: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 640 340" role="img" aria-label="频数分布直方图">'
        % (width, height),
        '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#202124" '
        'stroke-width="1.4"/>'
        % (left, top + plot_height, left + plot_width, top + plot_height),
        '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#202124" '
        'stroke-width="1.4"/>' % (left, top + plot_height, left, top),
    ]

    for tick in range(y_max + 1):
        y = top + plot_height - tick / y_max * plot_height
        parts.append(
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#eef1f5"/>'
            % (left, y, left + plot_width, y)
        )
        parts.append(
            '<text x="%.1f" y="%.1f" text-anchor="end" font-size="10" '
            'font-family="sans-serif" fill="#80868b">%d</text>'
            % (left - 6, y + 3, tick)
        )

    slot = plot_width / bins
    bar_width = slot * 0.72
    for index, count in enumerate(result.counts):
        height_px = count / y_max * plot_height
        x = left + slot * index + (slot - bar_width) / 2
        y = top + plot_height - height_px
        parts.append(
            '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#1a73e8" '
            'rx="2"/>' % (x, y, bar_width, height_px)
        )
        if count:
            parts.append(
                '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="11" '
                'font-family="sans-serif" fill="#202124">%d</text>'
                % (x + bar_width / 2, y - 5, count)
            )
        parts.append(
            '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="9" '
            'font-family="sans-serif" fill="#80868b">%s~%s</text>'
            % (
                x + bar_width / 2,
                top + plot_height + 16,
                _number(result.edges[index]),
                _number(result.edges[index + 1]),
            )
        )

    span = result.maximum - result.minimum
    mean_position = 0.5 if span < 1e-12 else (result.mean - result.minimum) / span
    mean_x = left + plot_width * mean_position
    parts.append(
        '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#d93025" '
        'stroke-width="1.4" stroke-dasharray="5 4"/>'
        % (mean_x, top, mean_x, top + plot_height)
    )
    parts.append(
        '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="11" '
        'font-family="sans-serif" fill="#d93025">平均 %s</text>'
        % (mean_x, top - 8, _number(result.mean))
    )
    parts.append(
        '<text x="%.1f" y="%.1f" font-size="13" font-family="sans-serif" '
        'fill="#202124">频数分布直方图（共 %d 个数据）</text>'
        % (left, top - 8, len(result.values))
    )
    parts.append(
        '<text x="%.1f" y="%.1f" text-anchor="middle" font-size="11" '
        'font-family="sans-serif" fill="#5f6368">数据区间</text>'
        % (left + plot_width / 2, 332)
    )
    parts.append("</svg>")
    return "".join(parts)


def _number(value: float) -> str:
    text = "%.1f" % value
    return text[:-2] if text.endswith(".0") else text


__all__ = ["HistogramResult", "StatsError", "build_histogram", "render_histogram_svg"]
