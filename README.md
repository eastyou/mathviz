# mathviz

[![CI](https://github.com/eastyou/mathviz/actions/workflows/ci.yml/badge.svg)](https://github.com/eastyou/mathviz/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](pyproject.toml)

给初中数学课做的可视化工具：一次函数、二次函数、反比例函数的图像，勾股定理的面积演示，以及频数分布直方图。一条命令生成可打印的单文件 HTML，也能在命令行直接看关键结论。**零依赖，不联网。**

函数图像、勾股图、直方图在课本上都是静态的，换一组参数就得重新画。`mathviz` 用输入的系数和参数实时计算顶点、交点、面积和频数，并把图画出来，方便课堂上改一个数就演示一次。

## 特性

- **一次函数**：画出直线，标出与 x 轴、y 轴的交点
- **二次函数**：计算顶点、判别式与实数根，标出顶点和交点，判断开口方向
- **反比例函数**：画出双曲线的两支，标出坐标轴渐近线
- **勾股定理**：三边向外作正方形，用面积 `a² + b² = c²` 直观呈现
- **频数分布直方图**：按指定组数统计频数，标出平均数与中位数
- **可打印**：A4 纵向报告，单文件、无外部资源
- **41 个单元测试**：函数特征、SVG 坐标、勾股面积、直方图统计与命令行

## 安装

```bash
pip install "git+https://github.com/eastyou/mathviz.git"
```

或者不安装，直接运行：

```bash
git clone https://github.com/eastyou/mathviz.git
cd mathviz
python3 -m mathviz --help
```

## 快速开始

### 一次函数

```console
$ mathviz linear -k 2 -b 1
y = 2x + 1
与 y 轴交点：(0, 1)
与 x 轴交点：(-0.5, 0)
```

### 二次函数

```console
$ mathviz quadratic -a 1 -b -2 -c -3
y = x² - 2x - 3
顶点：(1, -4)
与 x 轴交点：x = -1、x = 3
```

### 反比例函数

```console
$ mathviz inverse -k 6
y = 6 / x
图像位于第一、三象限，坐标轴是渐近线
```

### 勾股定理

```console
$ mathviz pythagoras -a 3 -b 4
c = 5，3² + 4² = 5²
面积：9 + 16 = 25
```

### 频数分布直方图

```console
$ mathviz histogram 72 75 78 80 80 82 85 88 90 95 --bins 5
共 10 个数据，平均数 82.5，中位数 81
  72 ~ 76.6：2 个
  76.6 ~ 81.2：3 个
  81.2 ~ 85.8：2 个
  85.8 ~ 90.4：2 个
  90.4 ~ 95：1 个
```

### 生成可视化页面

```console
$ mathviz html -o 数学可视化.html
已生成 数学可视化.html
```

页面包含五组示例图和对应数据表，浏览器打开后可直接打印或存为 PDF。

## 参数

| 命令 | 说明 |
| --- | --- |
| `mathviz linear -k 2 -b 1 [--xmin -10 --xmax 10]` | 一次函数 |
| `mathviz quadratic -a 1 -b -2 -c -3` | 二次函数 |
| `mathviz inverse -k 6` | 反比例函数 |
| `mathviz pythagoras -a 3 -b 4` | 勾股定理 |
| `mathviz histogram 1 2 3 --bins 5` | 直方图 |
| `mathviz html [-o 文件] [--title 标题]` | 生成示例页面 |

### 退出码

| 退出码 | 含义 |
| --- | --- |
| `0` | 成功 |
| `1` | 页面写入失败 |
| `2` | 参数或数据不合法 |

## 计算依据

- 一次函数：`y = kx + b`，与 x 轴交点为 `(-b/k, 0)`
- 二次函数：顶点 `(-b/2a, c - b²/4a)`，判别式 `Δ = b² - 4ac`
- 反比例函数：`y = k/x`，`k > 0` 时图像在第一、三象限
- 勾股定理：`c = √(a² + b²)`
- 直方图：等宽分组，落在最大值上的数据计入最后一组

## 说明与边界

- 函数图像默认绘制 `x ∈ [-10, 10]`，可用 `--xmin`、`--xmax` 调整；范围过大会被拒绝
- 反比例函数在 x 接近 0 时函数值趋于无穷，图中纵轴限制在 ±20 以内，超出部分被裁剪
- 直方图最多 20 组；数据必须为有限数字
- 图像用于理解数量关系，不追求出版级精度

## 常见问题

**可以画别的函数吗？**
目前覆盖初中常见的三类函数。更多函数类型可以在 `mathviz/functions.py` 中扩展，采样和绘图部分可以复用。

**数据会上传吗？**
不会，程序没有任何联网代码，生成的 HTML 也不引用外部资源。

**为什么二次函数有时显示「无实数根」？**
当判别式小于 0 时，抛物线与 x 轴没有交点，图像仍然会正常绘制。

## 开发与测试

```bash
python3 -m unittest discover -s tests -v
```

CI 覆盖 Python 3.9 ~ 3.13 与 Linux/macOS/Windows。

## License

[MIT](LICENSE) © 2026 eastyou
