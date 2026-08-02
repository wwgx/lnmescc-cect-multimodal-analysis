from __future__ import annotations

import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter


BASE_DIR = Path(__file__).resolve().parent
SOURCE_CSV = BASE_DIR / "supplementary_figure_s1_metrics.csv"
OUTPUT_STEM = BASE_DIR / "Supplementary_Figure_S1_K_selection"

REGIONS = ["t", "p2", "p3", "p4"]
REGION_TITLES = {
    "t": "Intratumoral (t)",
    "p2": "Peritumoral 2 mm",
    "p3": "Peritumoral 3 mm",
    "p4": "Peritumoral 4 mm",
}

ORANGE = "#C85A00"
BLUE = "#0072B2"
RED = "#B2182B"
NAVY = "#00557A"
GRAY = "#666666"
BLACK = "#222222"


def geometric_knee(k: list[int], bic: list[float]) -> int:
    """Return the point farthest from the normalized endpoint chord."""
    x_min, x_max = min(k), max(k)
    y_min, y_max = min(bic), max(bic)
    x = [(value - x_min) / (x_max - x_min) for value in k]
    y = [(value - y_min) / (y_max - y_min) for value in bic]

    x0, y0 = x[0], y[0]
    x1, y1 = x[-1], y[-1]
    denominator = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    distances = [
        abs((y1 - y0) * xi - (x1 - x0) * yi + x1 * y0 - y1 * x0)
        / denominator
        for xi, yi in zip(x, y)
    ]
    return k[max(range(len(k)), key=lambda index: distances[index])]


def load_metrics() -> dict[str, list[dict[str, float]]]:
    grouped: dict[str, list[dict[str, float]]] = {region: [] for region in REGIONS}
    with SOURCE_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            region = row["Region"]
            if region not in grouped:
                continue
            grouped[region].append(
                {
                    "k": int(row["K"]),
                    "bic": float(row["BIC"]),
                    "silhouette": float(row["Silhouette"]),
                }
            )
    for rows in grouped.values():
        rows.sort(key=lambda item: item["k"])
    return grouped


def main() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 7,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "legend.frameon": False,
        }
    )

    metrics = load_metrics()
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 6.2), constrained_layout=False)
    panel_labels = ["a", "b", "c", "d"]

    for panel_index, (ax, panel_label, region) in enumerate(
        zip(axes.flat, panel_labels, REGIONS)
    ):
        rows = metrics[region]
        k = [item["k"] for item in rows]
        bic = [item["bic"] for item in rows]
        silhouette = [item["silhouette"] for item in rows]

        ax2 = ax.twinx()
        ax.plot(k, bic, color=ORANGE, marker="o", markersize=3.8, linewidth=1.8)
        ax2.plot(
            k,
            silhouette,
            color=BLUE,
            marker="s",
            markersize=3.6,
            linewidth=1.6,
            linestyle="--",
        )

        knee_k = geometric_knee(k, bic)
        knee_idx = k.index(knee_k)
        silhouette_max_idx = max(range(len(k)), key=lambda idx: silhouette[idx])
        bic_min_idx = min(range(len(k)), key=lambda idx: bic[idx])

        ax.axvline(4, color=BLACK, linewidth=1.0, linestyle=":", zorder=0)
        ax.scatter(
            [knee_k],
            [bic[knee_idx]],
            marker="*",
            s=95,
            color=RED,
            edgecolor="white",
            linewidth=0.5,
            zorder=5,
        )
        ax2.scatter(
            [k[silhouette_max_idx]],
            [silhouette[silhouette_max_idx]],
            marker="D",
            s=36,
            color=NAVY,
            edgecolor="white",
            linewidth=0.5,
            zorder=5,
        )
        ax.scatter(
            [k[bic_min_idx]],
            [bic[bic_min_idx]],
            marker="o",
            s=42,
            facecolor="white",
            edgecolor=ORANGE,
            linewidth=1.3,
            zorder=5,
        )

        ax.set_title(REGION_TITLES[region], fontsize=8.5, pad=5)
        ax.text(
            -0.14,
            1.06,
            panel_label,
            transform=ax.transAxes,
            fontsize=9,
            fontweight="bold",
            va="top",
        )
        ax.text(
            0.98,
            0.97,
            f"BIC min: K={k[bic_min_idx]}",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=6.4,
            color=GRAY,
        )

        ax.set_xticks(k)
        ax.set_xlabel("Number of habitats (K)")
        ax.set_ylabel("BIC (×10³)" if panel_index % 2 == 0 else "", color=ORANGE)
        ax2.set_ylabel(
            "Silhouette coefficient" if panel_index % 2 == 1 else "", color=BLUE
        )
        ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value / 1000:.0f}"))
        ax.tick_params(axis="y", colors=ORANGE)
        ax2.tick_params(axis="y", colors=BLUE)
        ax.grid(axis="both", color="#D9D9D9", linewidth=0.55, linestyle="--", alpha=0.7)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax2.spines["top"].set_visible(False)
        ax2.spines["left"].set_visible(False)

        sil_min = min(silhouette)
        sil_max = max(silhouette)
        sil_margin = max(0.025, (sil_max - sil_min) * 0.12)
        ax2.set_ylim(sil_min - sil_margin, sil_max + sil_margin)

    legend_handles = [
        Line2D([0], [0], color=ORANGE, marker="o", markersize=4, linewidth=1.8, label="BIC"),
        Line2D(
            [0],
            [0],
            color=BLUE,
            marker="s",
            markersize=4,
            linewidth=1.6,
            linestyle="--",
            label="Silhouette coefficient",
        ),
        Line2D(
            [0],
            [0],
            color=RED,
            marker="*",
            markeredgecolor="white",
            markersize=10,
            linewidth=0,
            label="Region-specific geometric knee",
        ),
        Line2D(
            [0],
            [0],
            color=BLACK,
            linewidth=1.0,
            linestyle=":",
            label="Common selected K=4",
        ),
        Line2D(
            [0],
            [0],
            color=NAVY,
            marker="D",
            markeredgecolor="white",
            markersize=5,
            linewidth=0,
            label="Silhouette maximum (K=2)",
        ),
        Line2D(
            [0],
            [0],
            color=ORANGE,
            marker="o",
            markerfacecolor="white",
            markersize=5,
            linewidth=0,
            label="BIC global minimum",
        ),
    ]
    fig.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.995),
        ncol=3,
        columnspacing=1.4,
        handletextpad=0.5,
        fontsize=7,
    )
    fig.subplots_adjust(left=0.10, right=0.90, bottom=0.08, top=0.88, wspace=0.36, hspace=0.35)

    fig.savefig(OUTPUT_STEM.with_suffix(".png"), dpi=600, bbox_inches="tight", facecolor="white")
    fig.savefig(OUTPUT_STEM.with_suffix(".svg"), bbox_inches="tight", facecolor="white")
    fig.savefig(OUTPUT_STEM.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
