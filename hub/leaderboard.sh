#!/bin/bash

print_leaderboard() {

    game_name=$1
    echo ""
    echo "=========== ${game_name} Leaderboard ==========="

    printf "%-12s %-10s %-10s %-10s %-10s %-10s\n" \
    "Player_name" "Played" "Wins" "Losses" "Win_pct" "Loss_pct"

    awk -F',' -v game="$game_name" '
    {
        if (NR > 1) {
            if ($1 == game) {
                if ($5 != "Yes") {
                    winner = $3
                    loser  = $4

                    played[winner]++
                    played[loser]++

                    wins[winner]++
                    losses[loser]++
                }
            }
        }
    }

    END {

        for (name in played) {

            w = wins[name]
            l = losses[name]
            p = played[name]

            if (w == "") w = 0
            if (l == "") l = 0

            if (p > 0) {
                win_pct  = (w * 100) / p
                loss_pct = (l * 100) / p
            } else {
                win_pct  = 0
                loss_pct = 0
            }

            printf "%s\t%d\t%d\t%d\t%.2f\t%.2f\n", \
            name, p, w, l, win_pct, loss_pct
        }
    }' history.csv |
    sort -t$'\t' -k5 -nr |
    awk -F'\t' '{
        printf "%-12s %-10d %-10d %-10d %-10.2f %-10.2f\n",
        $1,$2,$3,$4,$5,$6
    }'
}

# RUN
print_leaderboard "TicTacToe"
print_leaderboard "Connect4"
print_leaderboard "Othello"
