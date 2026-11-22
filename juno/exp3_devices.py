# 実験3：実機の価格と満足度の散布図化（Juno / Python）
# 入力：data/devices.json（満足度）＋ 下記の検証済み価格
# 出力：data/chart-devices.png（価格 vs 満足度）
# 価格（検証済みのみ）：
#   iPhone 11：38,000円で購入（本人）／満足度70点
#   POCO F7 Pro：約60,000円（本人評価「約6万円」）／満足度85点
# 除外と理由：
#   Galaxy A25 5G（満足度60点）：価格が未確認のため、価格を推測で入れず散布図から除外
#   Xiaomi Pad、ゲーミングPC：未採点のため除外
# 注意：価格が2点しかないため、傾向線・相関の主張はしない。2点の記録として描く。
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
GRID = "#344157"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": TEXT, "axes.edgecolor": GRID, "axes.labelcolor": TEXT,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True,
    "grid.color": GRID, "grid.alpha": 0.5,
})

with open(os.path.join(BASE, "data", "devices.json"), encoding="utf-8") as f:
    devices = {d["name"]: d for d in json.load(f)["devices"]}

# 価格が検証済みの機種だけをプロットする
points = [
    ("iPhone 11", 38000, devices["iPhone 11"]["score"], CYAN, "iPhone 11\n38,000 yen / 70"),
    ("POCO F7 Pro", 60000, devices["POCO F7 Pro"]["score"], MAGENTA,
     "POCO F7 Pro\nabout 60,000 yen / 85"),
]

fig, ax = plt.subplots(figsize=(8, 5))
for name, price, score, color, label in points:
    ax.scatter([price], [score], s=220, color=color, edgecolors=BG, linewidths=2, zorder=3)
    ax.annotate(label, (price, score), xytext=(10, 12), textcoords="offset points",
                color=TEXT, fontsize=10)
ax.set_xlabel("Price (yen)", color=TEXT)
ax.set_ylabel("Satisfaction / 100", color=TEXT)
ax.set_title("Owned devices: price vs satisfaction (2 devices only)", color=TEXT, fontsize=12)
ax.set_xlim(20000, 75000)
ax.set_ylim(50, 100)
fig.tight_layout()
fig.savefig(os.path.join(BASE, "data", "chart-devices.png"), dpi=150)
plt.close(fig)
print("plotted:", [(p[0], p[1], p[2]) for p in points])
print("excluded: Galaxy A25 5G (price unknown), Xiaomi Pad / Gaming PC (unscored)")
print("saved: data/chart-devices.png")
