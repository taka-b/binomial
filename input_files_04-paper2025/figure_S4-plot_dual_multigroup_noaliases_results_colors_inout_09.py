# -*- coding: utf-8 -*-
"""
Multi-group dual-scale plotter (no aliases) with color mapping from *Element and *ElementInOut sections.
Now includes FIX_YMIN and YMIN_FIXED_VALUE options to lock the lower Y limit.
"""

import sys, datetime
from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt

# -------------------- User settings --------------------
TARGETS = [
    ["glucose", "O2", "glucose_total", "O2_total"],["O2"],
    ["glucose_in:=Cell_1", "Pyruvate_created:=Cell_1"],["Pyruvate_created:=Cell_1"],
    ["ATP_created::Cell_1::Mitochondria_1", "CO2::Cell_1::Mitochondria_1"],
    ["glucose:=Cell_1", "Pyruvate-:=Cell_1", "Lactic-:=Cell_1"],
    ["NAD+:=Cell_1", "NADH:=Cell_1"],["NAD+:=Cell_1"], ["NADH:=Cell_1"],
    ["H+:=Cell_1", "OH-:=Cell_1", "O2:=Cell_1"],
    ["ATP:=Cell_1", "ADP:=Cell_1", "Pi:=Cell_1"],["O2:=Cell_1"],
    ["Pyruvate-::Cell_1::Mitochondria_1", "Pyruvate-_in::Cell_1::Mitochondria_1", "O2::Cell_1::Mitochondria_1"],
    ["H+::Cell_1::Mitochondria_1", "H+_inter::Cell_1::Mitochondria_1", "OH-::Cell_1::Mitochondria_1"],
    ["NAD+::Cell_1::Mitochondria_1", "GDP::Cell_1::Mitochondria_1", "FAD::Cell_1::Mitochondria_1"],
    ["NADH::Cell_1::Mitochondria_1", "GTP::Cell_1::Mitochondria_1", "FADH2::Cell_1::Mitochondria_1"],
    ["ATP::Cell_1::Mitochondria_1", "ADP::Cell_1::Mitochondria_1", "Pi::Cell_1::Mitochondria_1"],
    ["CoA-SH::Cell_1::Mitochondria_1", "Acetyl_CoA::Cell_1::Mitochondria_1", "CO2::Cell_1::Mitochondria_1"],   
]

# SD band multiplier: number of standard deviations for the shaded area
# (1 → ±1σ, 2 → ±2σ, 3 → ±3σ)
SD_MULTIPLIER = 3

# Color definition file (text file containing *Element / *ElementInOut sections)
# If None, all *.txt files in the folder will be scanned automatically
COLOR_DEF_FILE = None

# Font sizes for plot elements: (tick labels, axis labels, title, legend)
FONT_TICK, FONT_LABEL, FONT_TITLE, FONT_LEGEND = 14, 16, 20, 18

# Grid settings:
GRID_WHICH, GRID_LINEWIDTH, GRID_ALPHA = "major", 0.6, 0.5

# Figure size (width, height) in inches
FIG_SIZE = (10, 7)

# ---- User options ----
NONPOS_REPLACEMENT = 0.001

# ✅ New: Y-axis minimum lock options
FIX_YMIN = False              # True = lock minimum Y value; False = auto scale
YMIN_FIXED_VALUE = 1       # The bottom limit of Y-axis when FIX_YMIN=True
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
    if "Name" not in df.columns:
        return None, None
    time_cols = [c for c in df.columns if c != "Name"]
    time_vals = pd.to_numeric(pd.Index(time_cols), errors="coerce").values
    order = np.argsort(time_vals)
    time_vals = time_vals[order]
    ordered_cols = ["Name"] + [str(int(t)) for t in time_vals if not np.isnan(t)]
    ordered_cols = [c for c in ordered_cols if c in df.columns]
    df = df[ordered_cols]
    hit = df[df["Name"] == wanted]
    if hit.empty:
        return None, None
    vals = pd.to_numeric(hit.iloc[0, 1:], errors="coerce").values
    vals = np.where(np.isnan(vals) | (vals <= 0), NONPOS_REPLACEMENT, vals)
    return time_vals, vals

def compute_geom_stats(series_list):
    A = np.vstack(series_list)
    logA = np.log10(A)
    mean_log = logA.mean(axis=0)
    std_log  = logA.std(axis=0, ddof=1)
    mean_vals = 10**mean_log
    upper = 10**(mean_log + SD_MULTIPLIER * std_log)
    lower = 10**(mean_log - SD_MULTIPLIER * std_log)
    return mean_vals, lower, upper, std_log

def compute_arith_stats(series_list):
    A = np.vstack(series_list)
    mean_vals = A.mean(axis=0)
    std_vals  = A.std(axis=0, ddof=1)
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

def plot_group(folder, out_dir, names, group_index, csv_files, color_map):
    collected = {}
    for target in names:
        series_list, time_index = [], None
        for f in csv_files:
            try:
                df = pd.read_csv(f)
            except Exception:
                continue
            t_vals, y_vals = extract_row_timeseries_exact(df, target)
            if t_vals is None:
                continue
            if time_index is None:
                time_index = t_vals
            elif not np.array_equal(time_index, t_vals):
                continue
            series_list.append(y_vals)
        if series_list:
            collected[target] = {"time": time_index, "series": series_list}
    if not collected:
        return
    n_label = f"{len(csv_files)}"

    # ---- Log plot ----
    figA, axA = plt.subplots(figsize=FIG_SIZE, dpi=150)
    for name, data in collected.items():
        t, S = data["time"], data["series"]
        gm, gl, gu, _ = compute_geom_stats(S)
        color = color_map.get(name)
        axA.plot(t, gm, lw=1.8, label=name, color=color)
        axA.fill_between(t, gl, gu, alpha=0.18, color=color)

        stats = compute_summary_timeseries(S)
        safe = name.replace(":", "_").replace("=", "_")
        out_csv_summary = out_dir / f"summary_{safe}_group{group_index}.csv"
        save_series_summary_csv(t, stats, out_csv_summary)

    style_axes(axA)
    axA.set_yscale("log")
    if FIX_YMIN:
        axA.set_ylim(bottom=YMIN_FIXED_VALUE)
    axA.set_xlabel("Time (msec)", fontsize=FONT_LABEL)
    axA.set_ylabel("Count (log scale)", fontsize=FONT_LABEL)
    axA.set_title(f"Geometric mean ±{SD_MULTIPLIER}σ (n={n_label})", fontsize=FONT_TITLE)
    axA.tick_params(axis="both", labelsize=FONT_TICK)
    axA.legend(fontsize=FONT_LEGEND)
    figA.tight_layout()
    figA.savefig(out_dir / f"geom_log_group{group_index}.png", bbox_inches="tight")
    plt.close(figA)

    # ---- Linear plot ----
    figB, axB = plt.subplots(figsize=FIG_SIZE, dpi=150)
    for name, data in collected.items():
        t, S = data["time"], data["series"]
        m, l, u, _ = compute_arith_stats(S)
        color = color_map.get(name)
        axB.plot(t, m, lw=1.8, label=name, color=color)
        axB.fill_between(t, l, u, alpha=0.18, color=color)
    style_axes(axB)
    if FIX_YMIN:
        axB.set_ylim(bottom=YMIN_FIXED_VALUE)
    axB.set_xlabel("Time (msec)", fontsize=FONT_LABEL)
    axB.set_ylabel("Count (linear scale)", fontsize=FONT_LABEL)
    axB.set_title(f"Arithmetic mean ±{SD_MULTIPLIER}σ (n={n_label})", fontsize=FONT_TITLE)
    axB.tick_params(axis="both", labelsize=FONT_TICK)
    axB.legend(fontsize=FONT_LEGEND)
    figB.tight_layout()
    figB.savefig(out_dir / f"arith_linear_group{group_index}.png", bbox_inches="tight")
    plt.close(figB)

def main():
    folder = _this_folder()
    csv_files = read_all_csvs(folder)
    if not csv_files:
        sys.exit("[ERROR] No CSV files found.")
    out_dir = _prepare_results_folder(folder)
    color_map = build_color_map(folder)
    groups = [list(g) if isinstance(g, (list, tuple)) else list(TARGETS) for g in TARGETS]
    for i, names in enumerate(groups, start=1):
        plot_group(folder, out_dir, names, i, csv_files, color_map)

if __name__ == "__main__":
    main()
