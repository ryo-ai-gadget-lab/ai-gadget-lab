# 実験2：AI批評の採点データの棒グラフ化（Juno / Python）
# 入力：data/ai_top10.json（TOP10 + 特別枠 Claude Ultra）
# 出力：data/chart-ai-top10.png（横棒グラフ）
# 注意：31AIすべての5基準内訳は元データにないため、合計点のみを描く。
#       内訳スコアは推測で作らない。
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]:
    if os.path.exists(_p):
        font_manager.fontManager.addfont(_p)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=_p).get_name()
        break

BG = "#121A2B"
TEXT = "#EDF1F7"
MUTED = "#B7C2D2"
CYAN = "#8FBBC6"
MAGENTA = "#BFA3CC"
YELLOW = "#C6B78A"
GRID = "#344157"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": TEXT, "axes.edgecolor": GRID, "axes.labelcolor": TEXT,
    "xtick.color": MUTED, "ytick.color": TEXT, "axes.grid": True,
    "grid.color": GRID, "grid.alpha": 0.5,
})

with open(os.path.join(BASE, "data", "ai_top10.json"), encoding="utf-8") as f:
    data = json.load(f)

ranking = sorted(data["ranking"], key=lambda r: r["score"])
names = [r["name"] for r in ranking]
scores = [r["score"] for r in ranking]
# 特別枠（18歳以上限定）は一番下に別色で追加（順位と誤解されないよう最上位には置かない）
special = data["special_frame"]
names.insert(0, f"{special['name']} *")
scores.insert(0, special["score"])

colors = [YELLOW] + [CYAN] * len(ranking)
# 1位をマゼンタで強調
colors[-1] = MAGENTA

fig, ax = plt.subplots(figsize=(8, 5.5))
bars = ax.barh(names, scores, color=colors, height=0.6)
for bar, s in zip(bars, scores):
    ax.text(s + 1, bar.get_y() + bar.get_height() / 2, str(s),
            va="center", color=TEXT, fontsize=11)
ax.set_xlim(0, 100)
ax.set_xlabel("Score / 100", color=TEXT)
ax.set_title("AI review TOP10 (total score)", color=TEXT, fontsize=13)
ax.grid(axis="y", visible=False)
fig.text(0.08, 0.01, "* Claude Ultra 67: 18+ only, special frame (not in TOP10)",
         color=MUTED, fontsize=9)
fig.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig(os.path.join(BASE, "data", "chart-ai-top10.png"), dpi=150)
plt.close(fig)
print("saved: data/chart-ai-top10.png")
