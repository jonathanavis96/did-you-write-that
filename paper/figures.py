#!/usr/bin/env python
"""Generate vector PDF figures for the paper from numbers hard-coded from the
source documents (paper/main.tex tables tab:label / tab:frames, and
docs/PILOT-14-local-scale-series.md's Results cell-means table).

Run: cd paper && ../.venv/bin/python figures.py
"""
import os

from scipy.stats import beta

import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "figures")
os.makedirs(OUTDIR, exist_ok=True)

ASSIST_COLOR = "#1E88A8"
USER_COLOR = "#D35400"
OTHER_COLOR = "#7B61C9"
TEXT_COLOR = "#1B1F24"

plt.rcParams.update(
    {
        "font.size": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "text.color": TEXT_COLOR,
        "axes.labelcolor": TEXT_COLOR,
        "xtick.color": TEXT_COLOR,
        "ytick.color": TEXT_COLOR,
        "axes.edgecolor": TEXT_COLOR,
        "pdf.fonttype": 42,
    }
)

BAR_H = 0.6
BAR_W = 0.6

# ---------------------------------------------------------------------------
# Data, transcribed from paper/main.tex tab:label
# judge, prompts label, assistant-turn (num, den), user-turn (num, den)
# ---------------------------------------------------------------------------
LABEL_DATA = [
    ("Haiku, 8 (19, clean)", (256, 256), (0, 256)),
    ("Opus, 8 (19, clean)", (256, 256), (0, 256)),
    ("Haiku, 8 (13e)", (296, 296), (0, 296)),
    ("Haiku, 10 (15)", (376, 376), (0, 376)),
    ("Opus, 8 (16, 8 forks)", (360, 360), (30, 360)),
    ("Opus, 10 (15)", (188, 188), (2, 188)),
    ("Fable 5.1, 8 (13e)", (148, 148), (1, 148)),
    ("GPT, 8 (19, clean)", (194, 240), (9, 240)),
    ("GPT, 8 (13d)", (272, 272), (32, 272)),
    ("GPT, 10 (15)", (264, 264), (2, 264)),
]

# tab:frames: frame -> {judge: share}; clean rerun, 32 cells (Claude), 30 (GPT), 8 forks/cell
FRAMES_ORDER = [
    "neutral",
    "placebo",
    "rival,\nnamed",
    "rival,\nturns",
]
FRAMES_DATA = {
    "Haiku": [1.000, 1.000, 0.957, 0.684],
    "Opus": [1.000, 1.000, 0.973, 0.797],
    "GPT": [0.996, 0.821, 0.558, 0.179],
}
FRAMES_N = {"Haiku": 32, "Opus": 32, "GPT": 30}

# docs/PILOT-14-local-scale-series.md Results cell-means table.
# scale -> question -> (assistant, user2)
QWEN_DATA = {
    "Qwen2.5-1.5B": {
        "named": (0.204, 0.495),
        "neutral": (0.167, 0.511),
        "placebo": (0.612, 0.684),
        "rival": (0.043, 0.132),
    },
    "Qwen2.5-3B": {
        "named": (0.448, 0.164),
        "neutral": (0.000, 0.001),
        "placebo": (0.188, 0.225),
        "rival": (0.000, 0.000),
    },
    "Qwen3-4B": {
        "named": (0.311, 0.000),
        "neutral": (0.963, 0.945),
        "placebo": (0.922, 0.736),
        "rival": (0.073, 0.076),
    },
}
QWEN_QUESTIONS = ["named", "neutral", "placebo", "rival"]


def fig_label():
    n = len(LABEL_DATA)
    fig, ax = plt.subplots(figsize=(3.3, 0.42 * n + 0.6))

    ys = list(range(n))[::-1]
    for y, (label, (a_num, a_den), (u_num, u_den)) in zip(ys, LABEL_DATA):
        a_share = a_num / a_den
        u_share = u_num / u_den
        y_assist = y + BAR_H / 2 + 0.02
        y_user = y - BAR_H / 2 - 0.02
        ax.barh(y_assist, a_share, height=BAR_H, color=ASSIST_COLOR, label="assistant turn" if y == ys[0] else None)
        ax.barh(y_user, u_share, height=BAR_H, color=USER_COLOR, label="user turn" if y == ys[0] else None)
        ax.text(
            a_share + 0.02, y_assist, f"{a_num}/{a_den}", va="center", ha="left", fontsize=6.5, color=TEXT_COLOR
        )
        ax.text(
            u_share + 0.02, y_user, f"{u_num}/{u_den}", va="center", ha="left", fontsize=6.5, color=TEXT_COLOR
        )

    ax.set_yticks(ys)
    ax.set_yticklabels([d[0] for d in LABEL_DATA], fontsize=6.5)
    ax.set_xlim(0, 1.18)
    ax.set_xlabel("share owned")
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.legend(loc="lower right", frameon=False, fontsize=6.5)
    ax.set_ylim(-0.6, n - 1 + 0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, "fig_label.pdf"), bbox_inches="tight")
    plt.close(fig)


def fig_frames():
    judges = ["Haiku", "Opus", "GPT"]
    fig, axes = plt.subplots(1, 3, figsize=(6.9, 2.3), sharey=True)

    x = list(range(len(FRAMES_ORDER)))
    for ax, judge in zip(axes, judges):
        vals = FRAMES_DATA[judge]
        ax.bar(x, vals, width=BAR_W, color=ASSIST_COLOR)
        for xi, v in zip(x, vals):
            ax.text(xi, v + 0.02, f"{v:.3f}", ha="center", va="bottom", fontsize=6.5, color=TEXT_COLOR)
        ax.set_xticks(x)
        ax.set_xticklabels(FRAMES_ORDER, fontsize=6, ha="center", linespacing=1.3)
        ax.set_ylim(0, 1.08)
        ax.set_title(f"{judge} (n={FRAMES_N[judge]})", fontsize=8, color=TEXT_COLOR, pad=4)
        ax.set_xlim(-0.6, len(FRAMES_ORDER) - 1 + 0.6)

    axes[0].set_ylabel("P(Yes)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, "fig_frames.pdf"), bbox_inches="tight")
    plt.close(fig)


def fig_qwen():
    scales = list(QWEN_DATA.keys())
    fig, axes = plt.subplots(1, 3, figsize=(6.9, 2.4), sharey=True)

    n_q = len(QWEN_QUESTIONS)
    offset = 0.22
    bw = 0.38

    for panel_i, (ax, scale) in enumerate(zip(axes, scales)):
        cell = QWEN_DATA[scale]
        for qi, q in enumerate(QWEN_QUESTIONS):
            a_val, u_val = cell[q]
            xa = qi - offset
            xu = qi + offset
            ax.bar(
                xa,
                a_val,
                width=bw,
                color=ASSIST_COLOR,
                label="assistant layout" if (panel_i == 0 and qi == 0) else None,
            )
            ax.bar(
                xu,
                u_val,
                width=bw,
                color=USER_COLOR,
                label="user2 layout" if (panel_i == 0 and qi == 0) else None,
            )
            for xv, val in ((xa, a_val), (xu, u_val)):
                if val > 0.05:
                    ax.text(xv, val + 0.02, f"{val:.2f}", ha="center", va="bottom", fontsize=5.5, color=TEXT_COLOR)
                else:
                    ax.text(xv, 0.015, "0.00", ha="center", va="bottom", fontsize=5.5, color=TEXT_COLOR)
        ax.set_xticks(range(n_q))
        ax.set_xticklabels(QWEN_QUESTIONS, fontsize=6.5)
        ax.set_ylim(0, 1.08)
        ax.set_title(scale, fontsize=8, color=TEXT_COLOR, pad=4)
        ax.set_xlim(-0.6, n_q - 1 + 0.6)

    axes[0].set_ylabel("mean P(Yes)")
    axes[0].legend(loc="upper left", frameon=False, fontsize=6.5)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, "fig_qwen.pdf"), bbox_inches="tight")
    plt.close(fig)


# Fill in later: {"rival_gap": {"opus": {"own": x, "other": y}, ...},
#                 "pairs": {"opus": [(k, n), ...], ...}}
PARAGRAPH_DATA = {
    # pilot 17c, clean harness (out/logs/p17c_summary.txt): rival-frame P(Yes), n = 96 per own
    # and shifted cell, 192 pooled over the two other-author cells
    "rival_gap": {
        "Haiku 4.5": {"own": 0.667, "other": 0.562, "shifted": 0.094},
        "Opus 5": {"own": 0.771, "other": 0.339, "shifted": 0.000},
        "GPT-5.6-Sol": {"own": 0.083, "other": 0.031, "shifted": 0.000},
    },
    # forced choice, correct k of parsed n: (vs the other Claude model, vs the other vendor)
    "pairs": {
        "Haiku 4.5": [(7, 23), (3, 15)],
        "Opus 5": [(92, 96), (83, 96)],
        "GPT-5.6-Sol": [(89, 96), (64, 96)],
    },
}


def fig_paragraph(data):
    if data is None:
        print("fig_paragraph skipped: no data")
        return

    models = list(data["rival_gap"].keys())
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.4))

    ax = axes[0]
    x = list(range(len(models)))
    own_vals = [data["rival_gap"][m]["own"] for m in models]
    other_vals = [data["rival_gap"][m]["other"] for m in models]
    shifted_vals = [data["rival_gap"][m]["shifted"] for m in models]
    bw = 0.26
    for off, vals, col, lab in ((-bw, own_vals, ASSIST_COLOR, "own paragraph"),
                                (0, other_vals, USER_COLOR, "another model's"),
                                (bw, shifted_vals, OTHER_COLOR, "own, hedged")):
        ax.bar([xi + off for xi in x], vals, width=bw, color=col, label=lab)
        for xi, v in zip(x, vals):
            ax.text(xi + off, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=5.5, color=TEXT_COLOR)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=6.5)
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("P(Yes), rival frame")
    ax.legend(loc="upper right", frameon=False, fontsize=6.5)

    ax2 = axes[1]
    comps = ["vs other Claude", "vs other vendor"]
    bw2 = 0.35
    for ci_, (comp, col) in enumerate(zip(comps, (ASSIST_COLOR, OTHER_COLOR))):
        for xi, m in enumerate(models):
            k, n = data["pairs"][m][ci_]
            lo, hi = beta.ppf(0.025, k, n - k + 1) if k else 0.0, beta.ppf(0.975, k + 1, n - k) if k < n else 1.0
            acc = k / n
            xpos = xi + (ci_ - 0.5) * bw2
            ax2.bar(xpos, acc, width=bw2, color=col, label=comp if xi == 0 else None)
            ax2.errorbar(xpos, acc, yerr=[[acc - lo], [hi - acc]], fmt="none", ecolor=TEXT_COLOR, elinewidth=0.6, capsize=1.5)
            ax2.text(xpos, hi + 0.02, f"{k}/{n}", ha="center", va="bottom", fontsize=5.5, color=TEXT_COLOR)
    ax2.axhline(0.5, color=TEXT_COLOR, lw=0.5, ls=":")
    ax2.set_xticks(list(range(len(models))))
    ax2.set_xticklabels(models, fontsize=6.5)
    ax2.set_ylim(0, 1.15)
    ax2.set_ylabel("forced-choice accuracy")
    ax2.legend(loc="upper left", frameon=False, fontsize=6.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUTDIR, "fig_paragraph.pdf"), bbox_inches="tight")
    plt.close(fig)


def main():
    fig_label()
    fig_frames()
    fig_qwen()
    fig_paragraph(PARAGRAPH_DATA)


if __name__ == "__main__":
    main()
