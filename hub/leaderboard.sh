#!/bin/bash
B_YEL=$'\033[1;33m'
B_BLU=$'\033[0;34m'
B_GRN=$'\033[0;32m'
BOLD=$'\033[1m'
RST=$'\033[0m'
P1_COL=$'\033[1;96m'
P2_COL=$'\033[1;91m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HISTORY_FILE="$SCRIPT_DIR/history.csv"

PLAYER1=$1
PLAYER2=$2
SORTING_METRIC=${3:-"Win_pct"}

declare -A metric_col=(["Wins"]=3 ["Win_pct"]=5 ["WL_Ratio"]=7)
sort_col=${metric_col[$SORTING_METRIC]:-5}

print_leaderboard() {
    local game_name=$1
    local sort_col=$2

    echo ""
    echo "${B_YEL}${BOLD}  ------------------${game_name} Leaderboard------------------${RST}"
    echo ""
    echo "  ${P1_COL}${BOLD}■ $PLAYER1 (Player1)${RST}    ${P2_COL}${BOLD}■ $PLAYER2 (Player2)${RST}    ${B_GRN}■ Others${RST}"
    echo ""
    echo "${B_BLU}  ┌─────────────────┬──────────┬──────────┬───────────┬───────────┬───────────┬───────────┬──────────────┐${RST}"
    printf "${B_BLU}  │${RST} ${BOLD}%-15s${RST} ${B_BLU}│${RST} ${BOLD}%-8s${RST} ${B_BLU}│${RST} ${BOLD}%-8s${RST} ${B_BLU}│${RST} ${BOLD}%-9s${RST} ${B_BLU}│${RST} ${BOLD}%-9s${RST} ${B_BLU}│${RST} ${BOLD}%-9s${RST} ${B_BLU}│${RST} ${BOLD}%-9s${RST} ${B_BLU}│${RST} ${BOLD}%-12s${RST} ${B_BLU}│${RST}\n" \
        "Player" "Played" "Wins" "Losses" "Win %" "Loss %" "W/L Ratio" "Rank"
    echo "${B_BLU}  ├─────────────────┼──────────┼──────────┼───────────┼───────────┼───────────┼───────────┼──────────────┤${RST}"

    local row_num=0
    awk -F',' -v game="$game_name" '
    NR > 1 {
        if ($1 == game && $5 != "Yes") {
            winner = $3
            loser  = $4
            played[winner]++
            played[loser]++
            wins[winner]++
            losses[loser]++
        }
    }
    END {
        for (name in played) {
            w = (wins[name]   == "" ? 0 : wins[name])
            l = (losses[name] == "" ? 0 : losses[name])
            p = played[name]
            win_pct  = (p > 0) ? (w * 100) / p : 0
            loss_pct = (p > 0) ? (l * 100) / p : 0
            wl_ratio = (l > 0) ? w / l :  w  # if no losses, ratio = wins (best case)
            printf "%s\t%d\t%d\t%d\t%.2f\t%.2f\t%.2f\n", name, p, w, l, win_pct, loss_pct, wl_ratio
        }
    }' "$HISTORY_FILE" | \
    sort -t$'\t' -k"${sort_col}" -nr | \
    while IFS=$'\t' read -r name played wins losses win_pct loss_pct wl_ratio; do
        row_num=$((row_num + 1))
        rank=$(printf "#%-6s" "$row_num  ")
        if [ "$name" = "$PLAYER1" ]; then
            color=$P1_COL; tag="◀ P1"
        elif [ "$name" = "$PLAYER2" ]; then
            color=$P2_COL; tag="◀ P2"
        else
            color=$B_GRN; tag="    "
        fi
        printf "${B_BLU}  │${RST} ${color}${BOLD}%-15s${RST} ${B_BLU}│${RST} ${color}${BOLD}%-8s${RST} ${B_BLU}│${RST} ${color}${BOLD}%-8s${RST} ${B_BLU}│${RST} ${color}${BOLD}%-9s${RST} ${B_BLU}│${RST} ${color}${BOLD}%-9s${RST} ${B_BLU}│${RST} ${color}${BOLD}%-9s${RST} ${B_BLU}│${RST} ${color}${BOLD}%-9s${RST} ${B_BLU}│${RST} ${color}${BOLD}%-5s %-4s${RST} ${B_BLU}│${RST}\n" \
            "$name" "$played" "$wins" "$losses" "$win_pct" "$loss_pct" "$wl_ratio" "$rank" "$tag"
    done

    echo "${B_BLU}  └─────────────────┴──────────┴──────────┴───────────┴───────────┴───────────┴───────────┴──────────────┘${RST}"
    echo ""
}

echo ""
echo "${BOLD}  Sorted by: ${B_YEL}$SORTING_METRIC${RST}"

print_leaderboard "TicTacToe" "$sort_col"
print_leaderboard "Connect4"  "$sort_col"
print_leaderboard "Othello"   "$sort_col"

# ── Quit / Restart prompt ─────────────────────────────────────────────────────
echo ""
echo "${B_YEL}${BOLD}  What would you like to do?${RST}"
echo "  ${P1_COL}[R]${RST} Restart game"
echo "  ${P2_COL}[Q]${RST} Quit"
echo ""
read -rp "  Enter choice: " choice

declare -A exit_code=(["r"]=0 ["R"]=0 ["q"]=2 ["Q"]=2)
exit "${exit_code[$choice]:-2}"