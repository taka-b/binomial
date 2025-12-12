# -*- coding: utf-8 -*-
"""
figure_04_embedded_3d_v4.py
---------------------------
3D band plot with unified color scale.
Z-axis (ATP amount) shown in units of 1e8 → ticks 1.0, 2.0, ... with label "×1e8".
"""

import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter, MaxNLocator

plt.ioff()

# ====================== Embedded Data ======================
DATA = """100:=	ATP量	200:=	ATP量	300:=	ATP量	400:=	ATP量	500:=	ATP量
1.00E-04	4.3442E+07	1.00E-04	4.4227E+07	1.00E-04	4.2502E+07	1.00E-04	5.1547E+07	1.00E-04	4.2600E+07
1.00E-03	4.4094E+07	1.00E-03	4.4219E+07	1.00E-03	4.2495E+07	1.00E-03	5.1544E+07	1.00E-03	4.2622E+07
1.00E-02	4.4196E+07	1.00E-02	4.4213E+07	1.00E-02	4.2504E+07	1.00E-02	5.1533E+07	1.00E-02	4.2772E+07
1.00E-01	4.4219E+07	1.00E-01	4.4221E+07	1.00E-01	4.2509E+07	1.00E-01	5.0941E+07	1.00E-01	4.3571E+07
1.00E+00	4.4216E+07	1.00E+00	4.4216E+07	1.00E+00	4.4216E+07	1.00E+00	4.4216E+07	1.00E+00	4.4216E+07
1.00E+01	4.4224E+07	1.00E+01	4.4225E+07	1.00E+01	4.4227E+07	1.00E+01	4.2484E+07	1.00E+01	4.4167E+07
1.00E+02	4.4224E+07	1.00E+02	4.4222E+07	1.00E+02	4.4218E+07	1.00E+02	4.2426E+07	1.00E+02	4.3046E+07
1.00E+03	4.4217E+07	1.00E+03	4.4225E+07	1.00E+03	4.4211E+07	1.00E+03	4.2421E+07	1.00E+03	4.2534E+07
1.00E+04	4.4214E+07	1.00E+04	4.4230E+07	1.00E+04	4.4232E+07	1.00E+04	4.2422E+07	1.00E+04	4.2513E+07
"""

def get_max_atp_from_data(data_text: str) -> float:
    """
    Extract the maximum ATP amount value from the embedded DATA string.
    
    Parameters
    ----------
    data_text : str
        Multiline string containing tab- or space-separated columns.
        Format: series_name, ATP量, series_name, ATP量, ...
    
    Returns
    -------
    float
        Maximum ATP amount value found in the data.
    """
    # Read table (space or tab delimited)
    df = pd.read_csv(io.StringIO(data_text), sep=r"\s+", engine="python")
    
    # Collect only numeric columns (skip "series" columns)
    numeric_values = []
    for col in df.columns:
        # Try to parse as numeric (ignore text columns)
        vals = pd.to_numeric(df[col], errors="coerce")
        numeric_values.append(vals)
    
    # Flatten and compute max
    all_vals = pd.concat(numeric_values)
    max_val = float(np.nanmax(all_vals))
    
    return max_val

control_ATP = 4.4216E+07
OUTPUT_FILE_NAME = "figure_5B.png"

# --- Color scale (0 → purple, control → yellow-green, max → yellow) ---
zmin_global = 0.0
zcontrol = 4.4216e+07
# zmax_global = get_max_atp_from_data(DATA)
zmax_global = 0.8E+08
t_control = (zcontrol - zmin_global) / (zmax_global - zmin_global)
colors_with_pos = [
    (0.0, "#440154"),
    (t_control, "#2FB47C"),
    (1.0, "#FDE725"),
]
cmap = LinearSegmentedColormap.from_list("custom_control_mid", colors_with_pos)

X_label = "Reaction  "
Y_label = "log10(Rate constant)"
STAND_val = 1
STSNDARD = f"Normalized rate constant = {STAND_val}"


# ==========================================================
def read_pairwise_table_from_text(text: str):
    df = pd.read_csv(io.StringIO(text), sep=r"\s+", engine="python")
    cols = [str(c) for c in df.columns]
    names, atp_list = [], []
    rate_ref = None
    for i in range(0, len(cols), 2):
        name_col, atp_col = cols[i], cols[i+1]
        names.append(name_col)
        rate_i = pd.to_numeric(df[name_col], errors="coerce").to_numpy(dtype=float)
        atp_i  = pd.to_numeric(df[atp_col],  errors="coerce").to_numpy(dtype=float)
        atp_list.append(atp_i)
        if rate_ref is None:
            rate_ref = rate_i
    mask = ~np.isnan(rate_ref)
    return rate_ref[mask], [a[mask] for a in atp_list], names

def make_segment_vertices(x_center, y_vals, z_vals, width=0.25):
    verts_all = []
    for i in range(len(y_vals) - 1):
        verts = [
            (x_center - width, y_vals[i], z_vals[i]),
            (x_center - width, y_vals[i + 1], z_vals[i + 1]),
            (x_center + width, y_vals[i + 1], z_vals[i + 1]),
            (x_center + width, y_vals[i], z_vals[i]),
        ]
        verts_all.append(verts)
    return verts_all

def plot_3d_gradual_bands_rate(rates, atp_series, series_names, out_png=OUTPUT_FILE_NAME):
    y_log = np.log10(rates.astype(float))
    Z_vals = [np.asarray(a, dtype=float) for a in atp_series]
    norm = plt.Normalize(vmin=zmin_global, vmax=zmax_global)

    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    # --- Draw colored bands ---
    for idx, z_abs in enumerate(Z_vals):
        segments = make_segment_vertices(idx, y_log, z_abs, width=0.20)
        for verts in segments:
            z_mean = np.mean([v[2] for v in verts])
            color = cmap(norm(z_mean))
            poly = Poly3DCollection([verts], facecolor=color, edgecolor=None, alpha=0.75)
            ax.add_collection3d(poly)
        ax.plot(np.full_like(y_log, idx, dtype=float), y_log, z_abs,
                color="gray", linewidth=0.6, alpha=0.5)

    # --- Axis setup ---
    ax.set_xlabel(X_label, labelpad=15, fontsize=14)
    ax.set_ylabel(Y_label, fontsize=14)

    # scale z values to 1e8 for display
    ax.set_zlim(0, zmax_global)
    ax.zaxis.set_major_locator(MaxNLocator(nbins=6))
    ax.zaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x/1e8:.1f}"))
    ax.set_zlabel("ATP amount (count) ×1e8", labelpad=20, fontsize=14)

    ax.set_xticks(range(len(series_names)))
    ax.set_xticklabels(series_names, rotation=30, ha="right")
    ax.set_ylim(np.nanmin(y_log), np.nanmax(y_log))
    ax.tick_params(axis="x", pad=1)

    # --- Colorbar ---
    mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array([])
    cbar = plt.colorbar(mappable, ax=ax, shrink=0.7, pad=0.12)
    cbar.set_label("ATP amount (count) ×1e8", rotation=90, labelpad=20, fontsize=14)
    cbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x/1e8:.1f}"))
    cbar.update_ticks()

    # --- Reference line ---
    y_ref = np.log10(STAND_val)
    z_ref = np.mean([arr[np.nanargmin(np.abs(rates - 1.0))] for arr in Z_vals])
    ax.plot(range(len(series_names)), [y_ref]*len(series_names), [z_ref]*len(series_names),
            color="red", linewidth=2.2, linestyle="--", alpha=0.95, zorder=200)
    ax.text(len(series_names)- 0.5, y_ref - 0.5, z_ref + (zmax_global - zmin_global)*0.01,
            STSNDARD, color="red", fontsize=12,
            fontweight="bold", ha="right", zorder=201)

    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[DONE] Saved: {out_png}")

# ==========================================================
if __name__ == "__main__":
    rates, series, names = read_pairwise_table_from_text(DATA)
    plot_3d_gradual_bands_rate(rates, series, names)
