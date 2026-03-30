#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ==========================================
# Data
# ==========================================

rate_ratio = np.array([1.000, 0.600, 0.300, 0.100, 0.060, 0.030])

datasets = [
    {
        "label": "DHO:: = 3.12×10^8",
        "ATP_D": np.array([877311, 450984, 73281, 1305, 143, 3], dtype=float),
        "ATP_H": np.array([227191779, 228039969, 227912499, 228082692, 228092808, 228115959], dtype=float),
        "marker": "o",
        "linestyle": "-",
    },
    {
        "label": "DHO:: = 3.12×10^7",
        "ATP_D": np.array([86904, 39849, 6933, 128, 15, 0], dtype=float),
        "ATP_H": np.array([228033567, 228071283 , 228095520, 228112272, 228109710, 228115101], dtype=float),
        "marker": "s",
        "linestyle": "-",
    },
    {
        "label": "DHO:: = 3.12×10^6",
        "ATP_D": np.array([7479, 3300, 600, 9, 0, 0], dtype=float),
        "ATP_H": np.array([228128850, 228113121, 228122085, 228115200, 228125799, 228123999], dtype=float),
        "marker": "^",
        "linestyle": "-",
    },
]

# ==========================================
# Settings
# ==========================================

plt.rcParams["font.size"] = 12

FIGSIZE = (7.2, 6.0)

# D+ の 0 を log 表示するための仮置き値
D_ZERO_DISPLAY_VALUE = 0.1

OUTPUT_H = "Figure8A_ATP_via_H_r2.png"
OUTPUT_D = "Figure8B_ATP_via_D_r2.png"

# 線形 x 軸用の主目盛
XTICKS = rate_ratio
XTICKLABELS = [f"{x:.3f}" for x in XTICKS]

# ==========================================
# Helper
# ==========================================

def get_log_limits_with_margin(values, zero_replace=None,
                               lower_margin_decades=0.5,
                               upper_margin_decades=0.3):
    arr = np.array(values, dtype=float).copy()

    if zero_replace is not None:
        arr[arr <= 0] = zero_replace
    else:
        arr = arr[arr > 0]

    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        raise ValueError("No positive finite values found.")

    ymin = arr.min()
    ymax = arr.max()

    log_min = np.log10(ymin) - lower_margin_decades
    log_max = np.log10(ymax) + upper_margin_decades

    return 10**log_min, 10**log_max


def set_linear_x_axis(ax):
    """x軸は線形スケール、補助線も線形で表示"""
    ax.set_xlim(1.02, 0.02)   # 0 は入れない
    ax.set_xticks(XTICKS)
    ax.set_xticklabels(XTICKLABELS, rotation=40, ha="right")

    # 線形の補助目盛
    ax.xaxis.set_minor_locator(MultipleLocator(0.1))

    # グリッド：主目盛・補助目盛とも線形
    ax.grid(True, which="major", axis="both", alpha=0.25)
    ax.grid(True, which="minor", axis="x", alpha=0.12)


# ==========================================
# 1) Figure 8A: ATP production via H+
# ==========================================

fig_h, ax_h = plt.subplots(figsize=FIGSIZE)

for ds in datasets:
    ax_h.plot(
        rate_ratio,
        ds["ATP_H"],
        marker=ds["marker"],
        linestyle=ds["linestyle"],
        linewidth=2.0,
        markersize=6.5,
        label=ds["label"]
    )

# y軸は線形のままでもよいですが、現状の図の見た目を維持するなら linear が自然
# 小さい変化を見やすくするため、範囲をやや絞る
all_h = np.concatenate([ds["ATP_H"] for ds in datasets])
ymin_h = np.min(all_h)
ymax_h = np.max(all_h)
margin_h = (ymax_h - ymin_h) * 5.0 + 5e5  # ある程度余白を持たせる
ax_h.set_ylim(ymin_h - margin_h, ymax_h + margin_h)

set_linear_x_axis(ax_h)

ax_h.set_xlabel("Rate constant ratio (D⁺ / H⁺)", fontsize=14)
ax_h.set_ylabel("ATP production via H⁺", fontsize=14)
ax_h.legend(frameon=True, fontsize=11, loc="best")

fig_h.tight_layout()
fig_h.savefig(OUTPUT_H, dpi=300, bbox_inches="tight")
plt.show()

# ==========================================
# 2) Figure 8B: ATP production via D+
# ==========================================

fig_d, ax_d = plt.subplots(figsize=FIGSIZE)

for ds in datasets:
    y = ds["ATP_D"].copy()
    zero_mask = (y <= 0)

    y_plot = y.copy()
    y_plot[zero_mask] = D_ZERO_DISPLAY_VALUE

    ax_d.plot(
        rate_ratio,
        y_plot,
        marker=ds["marker"],
        linestyle=ds["linestyle"],
        linewidth=2.0,
        markersize=6.5,
        label=ds["label"]
    )

    # 0 のところに "0" を表示
    for x_val, y_val, is_zero in zip(rate_ratio, y_plot, zero_mask):
        if is_zero:
            ax_d.text(
                x_val,
                y_val * 1.35,
                "0",
                ha="center",
                va="bottom",
                fontsize=10
            )

ax_d.set_yscale("log")

all_d = np.concatenate([ds["ATP_D"] for ds in datasets])
ylim_d = get_log_limits_with_margin(
    all_d,
    zero_replace=D_ZERO_DISPLAY_VALUE,
    lower_margin_decades=0.5,
    upper_margin_decades=0.25
)
ax_d.set_ylim(ylim_d)

set_linear_x_axis(ax_d)

# log y軸なので y方向の補助線はそのまま表示してよい
ax_d.grid(True, which="both", axis="y", alpha=0.18)

ax_d.set_xlabel("Rate constant ratio (D⁺ / H⁺)", fontsize=14)
ax_d.set_ylabel("ATP production via D⁺", fontsize=14)
ax_d.legend(frameon=True, fontsize=11, loc="best")

fig_d.tight_layout()
fig_d.savefig(OUTPUT_D, dpi=300, bbox_inches="tight")
plt.show()