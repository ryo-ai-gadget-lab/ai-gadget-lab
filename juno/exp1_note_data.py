# 実験1：note運営データのグラフ化（Juno / Python）
# 入力：juno/note_data.csv（検証済み合計のみ。日別データは含まない）
# 出力：data/chart-note-periods.png（2期間の比較）、data/chart-note-inflow.png（流入元円グラフ）
# 実行：Juno（iPhone・無料）または python3 juno/exp1_note_data.py
# 注意：スクリーンショットの日別バーの高さは数値として読めないため、
#       日別推移グラフは作らない。合計値だけを使う。
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 日本語フォント（Noto Sans CJK JP があれば使う。なければデフォルト）
for _p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
           "/System/Library/Fonts/Hiragino Sans GB.ttc"]:
    if os.path.exists(_p):
        font_manager.fontManager.addfont(_p)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=_p).get_name()
        break

BG = "#121A2B"
PANEL = "#1B2435"
TEXT = "#EDF1F7"
MUTED = "#B7C2D2"
CYAN = "#8FBBC6"
MAGENTA = "#BFA3CC"
YELLOW = "#C6B78A"
GRID = "#344157"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": TEXT, "axes.edgecolor": GRID, "axes.labelcolor": TEXT,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True,
    "grid.color": GRID, "grid.alpha": 0.5,
})

# --- CSV読み込み（「# --- 期間合計」セクションと「# --- 流入元」セクション） ---
periods, inflow = [], []
section = None
with open(os.path.join(BASE, "juno", "note_data.csv"), encoding="utf-8") as f:
    for row in csv.reader(f):
        if not row or row[0].startswith("#"):
            if "期間合計" in (row[0] if row else ""):
                section = "periods"
            elif "流入元" in (row[0] if row else ""):
                section = "inflow"
            continue
        if section == "periods" and row[0] == "period":
            continue
        if section == "inflow" and row[0] == "source":
            continue
        if section == "periods":
            periods.append({"period": row[0], "impressions": int(row[1]),
                            "pageviews": int(row[2])})
        elif section == "inflow":
            inflow.append({"source": row[0], "share": float(row[1]),
                           "pv": int(row[2])})

# (a) 2期間の比較：インプレッションとPV（スケールが違うため2パネル）
fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
labels = ["9/28〜10/25", "10/26〜11/22"]
for ax, key, title, colors in [
        (axes[0], "impressions", "Impressions", [MAGENTA, CYAN]),
        (axes[1], "pageviews", "Pageviews", [MAGENTA, CYAN])]:
    vals = [p[key] for p in periods]
    ax.bar(labels, vals, color=colors, width=0.55)
    for i, v in enumerate(vals):
        ax.text(i, v, f"{v:,}", ha="center", va="bottom", color=TEXT, fontsize=11)
    ax.set_title(title, color=TEXT, fontsize=12)
    ax.set_ylim(0, max(vals) * 1.2)
    ax.grid(axis="x", visible=False)
fig.suptitle("note 28-day totals (2026-11-22)", color=TEXT, fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.92])
fig.savefig(os.path.join(BASE, "data", "chart-note-periods.png"), dpi=150)
plt.close(fig)

# (b) 流入元（PVベース）の円グラフ（小さい項目は凡例で表示し、重なりを避ける）
fig, ax = plt.subplots(figsize=(7, 5.5))
colors = [CYAN, "#8A97AA", "#B7C2D2", "#D99595", YELLOW, MAGENTA]  # muted tones from css/style.css
vals = [s["share"] for s in inflow]
ax.pie(vals, colors=colors, autopct=lambda p: f"{p:.1f}%" if p >= 5 else "",
       pctdistance=0.8, textprops={"color": TEXT, "fontsize": 10},
       wedgeprops={"edgecolor": BG, "linewidth": 2})
legend_labels = [f"{s['source']} — {s['share']}% ({s['pv']}PV)" for s in inflow]
ax.legend(legend_labels, loc="center", bbox_to_anchor=(0.5, -0.08), ncol=2,
          frameon=False, fontsize=9, labelcolor=TEXT)
ax.set_title("Inflow sources (PV share)", color=TEXT, fontsize=12)
fig.tight_layout()
fig.savefig(os.path.join(BASE, "data", "chart-note-inflow.png"), dpi=150)
plt.close(fig)

print("periods:", periods)
print("inflow:", inflow)
print("saved: data/chart-note-periods.png, data/chart-note-inflow.png")
