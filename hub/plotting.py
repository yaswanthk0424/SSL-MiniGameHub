import os
import csv
import numpy as np
import matplotlib.pyplot as plt


def Plotting():
    base_dir     = os.path.dirname(os.path.abspath(__file__))
    history_path = os.path.join(base_dir, "history.csv")

    #Reading history
    wins, losses, draws, total, games = {}, {}, {}, {}, {}

    with open(history_path, 'r') as file:
        reader = csv.reader(file)
        rows   = list(reader)
        for row in rows[1:]:
            if len(row) < 5:
                continue
            game    = row[0]
            winner  = row[2]
            loser   = row[3]
            is_draw = row[4] == "Yes"

            games[game] = games.get(game, 0) + 1

            if not is_draw:
                wins[winner]  = wins.get(winner, 0) + 1
                losses[loser] = losses.get(loser, 0) + 1
                total[winner] = total.get(winner, 0) + 1
                total[loser]  = total.get(loser, 0) + 1
            else:
                draws[winner] = draws.get(winner, 0) + 1
                draws[loser]  = draws.get(loser, 0) + 1
                total[winner] = total.get(winner, 0) + 1
                total[loser]  = total.get(loser, 0) + 1

    if not total:
        print("[plot.py] No history data to plot.")
        return

    #Top 5 players by wins
    top5    = sorted(wins.keys(), key=lambda p: wins.get(p, 0), reverse=True)[:5]
    w_vals  = [wins.get(p, 0)   for p in top5]
    l_vals  = [losses.get(p, 0) for p in top5]
    d_vals  = [draws.get(p, 0)  for p in top5]
    wp_vals = [round(wins.get(p, 0) / total[p] * 100, 1)
               if total.get(p, 0) > 0 else 0 for p in top5]

    PALETTE  = ["#1cb8f5", "#f55c5c", "#4caf50", "#ffb347",
                "#bb86fc", "#03dac6", "#cf6679", "#ffdd57"]
    p_colors = [PALETTE[i % len(PALETTE)] for i in range(len(top5))]
    BG_DARK  = "#0f1923"
    BG_PANEL = "#1a2030"
    TEXT_COL = "#e6edf3"
    GRID_COL = "#2a3040"

    plt.style.use("dark_background")
    fig = plt.figure(figsize=(10, 10), facecolor=BG_DARK)
    fig.suptitle("GameHub — Player & Game Statistics",
                 color=TEXT_COL, fontsize=15, fontweight="bold", y=0.97)

    gs = fig.add_gridspec(2, 2, hspace=0.40, wspace=0.35,
                          left=0.09, right=0.97, top=0.91, bottom=0.09)

    def style_ax(ax, title):
        ax.set_facecolor(BG_PANEL)
        ax.set_title(title, color=TEXT_COL, fontsize=11, pad=8)
        ax.tick_params(colors=TEXT_COL, labelsize=9)
        ax.xaxis.label.set_color(TEXT_COL)
        ax.yaxis.label.set_color(TEXT_COL)
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        for spine in ax.spines.values():
            spine.set_edgecolor(GRID_COL)
        ax.set_axisbelow(True)
        ax.yaxis.grid(True, color=GRID_COL, linewidth=0.6)
        return ax

    x     = np.arange(len(top5))
    width = 0.25

    # Plot 1 (top-left): Grouped W / L / D bar
    ax1 = style_ax(fig.add_subplot(gs[0, 0]), "Top 5 Players — Wins / Losses / Draws")
    b1  = ax1.bar(x - width, w_vals, width, label="Wins",   color="#1cb8f5", zorder=3)
    b2  = ax1.bar(x,         l_vals, width, label="Losses", color="#f55c5c", zorder=3)
    b3  = ax1.bar(x + width, d_vals, width, label="Draws",  color="#ffb347", zorder=3)
    ax1.bar_label(b1, padding=2, color=TEXT_COL, fontsize=8)
    ax1.bar_label(b2, padding=2, color=TEXT_COL, fontsize=8)
    ax1.bar_label(b3, padding=2, color=TEXT_COL, fontsize=8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(top5, rotation=15, ha="right")
    ax1.legend(facecolor=BG_PANEL, labelcolor=TEXT_COL, fontsize=8)

    #  Plot 2 (top-right): Win % bar
    ax2   = style_ax(fig.add_subplot(gs[0, 1]), "Top 5 Players — Win %")
    bars2 = ax2.bar(top5, wp_vals, color=p_colors, zorder=3)
    ax2.bar_label(bars2, fmt="%.1f%%", padding=2, color=TEXT_COL, fontsize=8)
    ax2.set_ylim(0, 115)
    ax2.set_ylabel("Win %")
    ax2.set_xticks(range(len(top5)))
    ax2.set_xticklabels(top5, rotation=15, ha="right")

    # ── Plot 3 : Game distribution pie
    ax3 = fig.add_subplot(gs[1, :])
    ax3.set_facecolor(BG_PANEL)
    ax3.set_title("Game Distribution", color=TEXT_COL, fontsize=11, pad=8)
    ax3.axis("off")

    ax3_inset = ax3.inset_axes([0.25, 0.0, 0.5, 1.0])
    ax3_inset.set_facecolor(BG_PANEL)
    wedges, texts, autotexts = ax3_inset.pie(
        games.values(),
        labels=games.keys(),
        autopct="%1.1f%%",
        colors=PALETTE[:len(games)],
        startangle=90,
        textprops={"color": TEXT_COL, "fontsize": 10},
        wedgeprops={"linewidth": 1.2, "edgecolor": BG_DARK}
    )
    for at in autotexts:
        at.set_fontsize(9)

        mgr = plt.get_current_fig_manager()
        mgr.window.wm_geometry("+100+50")

    plt.show(block=False)
    plt.pause(0.5)