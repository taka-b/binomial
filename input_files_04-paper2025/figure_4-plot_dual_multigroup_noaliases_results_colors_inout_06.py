# -*- coding: utf-8 -*-
"""
Multi-group dual-scale plotter with bottom SD subplots.

- Top row:   Mean (geometric on log axis / arithmetic on linear axis)
- Bottom row: Standard deviation over time
    * For geometric plots: use SD in log10-space (σ_log10)
    * For arithmetic plots: use SD in linear units
- Keeps the original shaded ±SD band around the mean (for quick visual width).
"""

import sys, datetime
from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt

# -------------------- User settings --------------------
TARGETS = [
    ["glucose", "O2", "glucose_total", "O2_total"],["O2"],
    ["glucose_in:=Cell_1", "Pyruvate_created:=Cell_1"],["Pyruvate_created:=Cell_1"],
    ["ATP_created::Cell_1::Mitochondria_1", "CO2::Cell_1::Mitochondria_1"],
]

# SD band multiplier: number of standard deviations for the shaded area
SD_MULTIPLIER = 1

# Color definition file (text file containing *Element / *ElementInOut sections)
COLOR_DEF_FILE = None

# Font sizes
FONT_TICK, FONT_LABEL, FONT_TITLE, FONT_LEGEND = 14, 16, 20, 18

# Grid settings
GRID_WHICH, GRID_LINEWIDTH, GRID_ALPHA = "major", 0.6, 0.5

# Figure size (width, height) in inches
# （2段構成なので従来より少し背を高くしています）
FIG_SIZE_MEAN_SD = (10, 9)

# ---- User options ----
NONPOS_REPLACEMENT = 0.001
FIX_YMIN = True
YMIN_FIXED_VALUE = 100
# ------------------------------------------------------

def _this_folder():
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd()

def _prepare_results_folder(folder):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = folder / f"results_{ts}"
    out_dir.mkdir(exist_ok=True)
    print(f"[INFO] Results will be saved in: {out_dir}")
    return out_dir

def read_all_csvs(folder):
    return sorted(folder.glob("*.csv"))

def extract_row_timeseries_exact(df, wanted):
    """Return (time_vals, cleaned_values, had_nonpos_original)."""
    if "Name" not in df.columns:
        return None, None, None
    time_cols = [c for c in df.columns if c != "Name"]
    time_vals = pd.to_numeric(pd.Index(time_cols), errors="coerce").values
    order = np.argsort(time_vals)
    time_vals = time_vals[order]
    ordered_cols = ["Name"] + [str(int(t)) for t in time_vals if not np.isnan(t)]
    ordered_cols = [c for c in ordered_cols if c in df.columns]
    df = df[ordered_cols]
    hit = df[df["Name"] == wanted]
    if hit.empty:
        return None, None, None
    raw = pd.to_numeric(hit.iloc[0, 1:], errors="coerce").values
    had_nonpos = np.any(np.isnan(raw) | (raw <= 0))
    vals = np.where(np.isnan(raw) | (raw <= 0), NONPOS_REPLACEMENT, raw)
    return time_vals, vals, had_nonpos

def compute_geom_stats(series_list):
    A = np.vstack(series_list)
    logA = np.log10(A)
    mean_log = logA.mean(axis=0)
    std_log  = logA.std(axis=0, ddof=1)  # ← 下段サブプロット用
    mean_vals = 10**mean_log
    upper = 10**(mean_log + SD_MULTIPLIER * std_log)
    lower = 10**(mean_log - SD_MULTIPLIER * std_log)
    return mean_vals, lower, upper, std_log

def compute_arith_stats(series_list):
    A = np.vstack(series_list)
    mean_vals = A.mean(axis=0)
    std_vals  = A.std(axis=0, ddof=1)  # ← 下段サブプロット用
    lower = np.maximum(mean_vals - SD_MULTIPLIER * std_vals, 0.0)
    upper = mean_vals + SD_MULTIPLIER * std_vals
    return mean_vals, lower, upper, std_vals

def compute_summary_timeseries(series_list):
    A = np.vstack(series_list)
    min_vals  = np.min(A, axis=0)
    max_vals  = np.max(A, axis=0)
    mean_vals = np.mean(A, axis=0)
    std_vals  = np.std(A, axis=0, ddof=1)

    logA     = np.log10(A)
    mean_log = np.mean(logA, axis=0)
    std_log  = np.std(logA, axis=0, ddof=1)

    geom_mean = 10.0**mean_log
    geoSD     = 10.0**std_log

    std_vals = np.nan_to_num(std_vals, nan=0.0)
    std_log  = np.nan_to_num(std_log,  nan=0.0)
    geoSD    = np.nan_to_num(geoSD,    nan=1.0)

    return {
        "min": min_vals, "max": max_vals, "mean": mean_vals, "std": std_vals,
        "geom_mean": geom_mean, "std_log": std_log, "geoSD": geoSD
    }

def save_series_summary_csv(time_index, stats_dict, out_path):
    df = pd.DataFrame({
        "time_msec": time_index.astype(int),
        "min":       stats_dict["min"],
        "max":       stats_dict["max"],
        "mean":      stats_dict["mean"],
        "std":       stats_dict["std"],
        "geom_mean": stats_dict["geom_mean"],
        "std_log":   stats_dict["std_log"],
        "geoSD":     stats_dict["geoSD"],
    })
    df.to_csv(out_path, index=False)

def style_axes(ax):
    for side in ["top","right","bottom","left"]:
        ax.spines[side].set_visible(True)
        ax.spines[side].set_linewidth(1.2)
    ax.grid(True, which=GRID_WHICH, linestyle="-", linewidth=GRID_LINEWIDTH, alpha=GRID_ALPHA)

def _scan_color_files(folder):
    if COLOR_DEF_FILE:
        p = folder / COLOR_DEF_FILE
        return [p] if p.exists() else []
    return sorted(folder.glob("*.txt"))

def _parse_color_map_from_file(path):
    mapping = {}
    in_element = in_inout = False
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return mapping
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("**"):
            continue
        if line.startswith("*"):
            low = line.lower()
            if low.startswith("*elementinout"):
                in_inout, in_element = True, False
            elif low.startswith("*element"):
                in_element, in_inout = True, False
            else:
                in_element = in_inout = False
            continue
        if not (in_element or in_inout):
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 3:
            continue
        mapping[parts[0]] = parts[2]
    return mapping

def build_color_map(folder):
    cmap = {}
    for p in _scan_color_files(folder):
        cmap.update(_parse_color_map_from_file(p))
    print(f"[INFO] Loaded {len(cmap)} color entries." if cmap else "[INFO] No color definitions found.")
    return cmap

def plot_group_with_sd_subplots(folder, out_dir, names, group_index, csv_files, color_map):
    """
    Generate TWO figures per group:
      1) Geometric mean (log-y) + bottom subplot: SD in log10 units
      2) Arithmetic mean (linear-y) + bottom subplot: SD in linear units
    """
    # ---- collect time-series across CSVs for each target ----
    collected = {}
    for target in names:
        series_list, time_index = [], None
        had_nonpos_any = False
        for f in csv_files:
            try:
                df = pd.read_csv(f)
            except Exception:
                continue
            t_vals, y_vals, had_nonpos = extract_row_timeseries_exact(df, target)
            if t_vals is None:
                continue
            if time_index is None:
                time_index = t_vals
            elif not np.array_equal(time_index, t_vals):
                continue
            series_list.append(y_vals)
            had_nonpos_any = had_nonpos_any or bool(had_nonpos)
        if series_list:
            collected[target] = {"time": time_index, "series": series_list, "had_nonpos": had_nonpos_any}
    if not collected:
        return

    n_label = f"{len(csv_files)}"
    group_had_nonpos = any(d["had_nonpos"] for d in collected.values())

    # -------- Figure 1: Geometric mean (log) + SD(log10) --------
    fig1, (ax1_top, ax1_bot) = plt.subplots(
        2, 1, figsize=FIG_SIZE_MEAN_SD, dpi=150, sharex=True,
        gridspec_kw={"height_ratios":[3, 1.4], "hspace": 0.08}
    )
    for name, data in collected.items():
        t, S = data["time"], data["series"]
        gm, gl, gu, std_log = compute_geom_stats(S)
        color = color_map.get(name)
        # top: mean with ±σ band (geometric)
        ax1_top.plot(t, gm, lw=1.8, label=name, color=color)
        ax1_top.fill_between(t, gl, gu, alpha=0.18, color=color)
        # bottom: SD in log10 units
        ax1_bot.plot(t, std_log, lw=1.6, label=name, color=color)

        # also export per-series summary as before
        stats = compute_summary_timeseries(S)
        safe = name.replace(":", "_").replace("=", "_")
        out_csv_summary = out_dir / f"summary_{safe}_group{group_index}.csv"
        save_series_summary_csv(t, stats, out_csv_summary)

    # style top (geom/log)
    style_axes(ax1_top)
    ax1_top.set_yscale("log")
    if FIX_YMIN and group_had_nonpos:
        ax1_top.set_ylim(bottom=YMIN_FIXED_VALUE)
    ax1_top.set_ylabel("Count (log scale)", fontsize=FONT_LABEL)
    ax1_top.set_title(f"Geometric mean ±{SD_MULTIPLIER}σ (n={n_label})", fontsize=FONT_TITLE)
    ax1_top.tick_params(axis="both", labelsize=FONT_TICK)
    ax1_top.legend(fontsize=FONT_LEGEND)

    # style bottom (SD log10)
    style_axes(ax1_bot)
    ax1_bot.set_xlabel("Time (msec)", fontsize=FONT_LABEL)
    ax1_bot.set_ylabel("SD (log10 units)", fontsize=FONT_LABEL)
    ax1_bot.tick_params(axis="both", labelsize=FONT_TICK)

    fig1.tight_layout()
    fig1.savefig(out_dir / f"geom_log_withSD_group{group_index}.png", bbox_inches="tight")
    plt.close(fig1)

    # -------- Figure 2: Arithmetic mean (linear) + SD(linear) --------
    fig2, (ax2_top, ax2_bot) = plt.subplots(
        2, 1, figsize=FIG_SIZE_MEAN_SD, dpi=150, sharex=True,
        gridspec_kw={"height_ratios":[3, 1.4], "hspace": 0.08}
    )
    for name, data in collected.items():
        t, S = data["time"], data["series"]
        m, l, u, std_vals = compute_arith_stats(S)
        color = color_map.get(name)
        # top: mean with ±σ band (arithmetic)
        ax2_top.plot(t, m, lw=1.8, label=name, color=color)
        ax2_top.fill_between(t, l, u, alpha=0.18, color=color)
        # bottom: SD (linear)
        ax2_bot.plot(t, std_vals, lw=1.6, label=name, color=color)

    # style top (arith)
    style_axes(ax2_top)
    ax2_top.set_ylabel("Count (linear scale)", fontsize=FONT_LABEL)
    ax2_top.set_title(f"Arithmetic mean ±{SD_MULTIPLIER}σ (n={n_label})", fontsize=FONT_TITLE)
    ax2_top.tick_params(axis="both", labelsize=FONT_TICK)
    ax2_top.legend(fontsize=FONT_LEGEND)

    # style bottom (SD linear)
    style_axes(ax2_bot)
    ax2_bot.set_xlabel("Time (msec)", fontsize=FONT_LABEL)
    ax2_bot.set_ylabel("SD (linear)", fontsize=FONT_LABEL)
    ax2_bot.tick_params(axis="both", labelsize=FONT_TICK)

    fig2.tight_layout()
    fig2.savefig(out_dir / f"arith_linear_withSD_group{group_index}.png", bbox_inches="tight")
    plt.close(fig2)

def main():
    folder = _this_folder()
    csv_files = read_all_csvs(folder)
    if not csv_files:
        sys.exit("[ERROR] No CSV files found.")
    out_dir = _prepare_results_folder(folder)
    color_map = build_color_map(folder)
    groups = [list(g) if isinstance(g, (list, tuple)) else list(TARGETS) for g in TARGETS]
    for i, names in enumerate(groups, start=1):
        plot_group_with_sd_subplots(folder, out_dir, names, i, csv_files, color_map)

if __name__ == "__main__":
    main()
