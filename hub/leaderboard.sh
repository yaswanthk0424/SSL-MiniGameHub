#!/bin/bash
echo -e "===========Game1 Leaderboard=========="
printf "\n%-12s %-10s %-10s %-10s %-10s %-10s\n" "Player_name" "Played" "Wins" "Losses" "Win pct" "Loss pct"
sed -nE '/^[0-9]{2}-[0-9]{2}-[0-9]{4},Game1,[A-Za-z]+,[A-Za-z]+$/p' history.csv > game1_lb.csv
awk -F',' '
{

    winner=$3;
    loser=$4;
    played[winner]++;
    played[loser]++;
    wins[winner]++;
    losses[loser]++;
    losses[winner] = played[winner] - wins[winner];
    wins[loser] = played[loser] - losses[loser];

}
END {
for(name in played){ 
    win_pct = wins[name]*100/played[name];
    loss_pct = losses[name]*100/played[name];
    printf "%s\t %d\t %d\t %d\t %d\t %d\n",name,played[name],wins[name],losses[name],win_pct,loss_pct >> "dummy_output.txt"
}

}
' game1_lb.csv
sort -n -t$'\t' -k4 dummy_output.txt | awk -F'\t' '{printf"%-12s %-10d %-10d %-10d %-10.2f %-10.2f\n",$1,$2,$3,$4,$5,$6}'
rm dummy_output.txt
rm game1_lb.csv

echo -e "\n===========Game2 Leaderboard=========="
printf "\n%-12s %-10s %-10s %-10s %-10s %-10s\n" "Player_name" "Played" "Wins" "Losses" "Win pct" "Loss pct"
sed -nE '/^[0-9]{2}-[0-9]{2}-[0-9]{4},Game2,[A-Za-z]+,[A-Za-z]+$/p' history.csv > game2_lb.csv
awk -F',' '
{

    winner=$3;
    loser=$4;
    played[winner]++;
    played[loser]++;
    wins[winner]++;
    losses[loser]++;
    losses[winner] = played[winner] - wins[winner];
    wins[loser] = played[loser] - losses[loser];

}
END {
for(name in played){ 
    win_pct = wins[name]*100/played[name];
    loss_pct = losses[name]*100/played[name];
    printf "%s\t %d\t %d\t %d\t %d\t %d\n",name,played[name],wins[name],losses[name],win_pct,loss_pct >> "dummy2_output.txt"
}

}
' game2_lb.csv
sort -n -t$'\t' -k4 dummy2_output.txt | awk -F'\t' '{printf"%-12s %-10d %-10d %-10d %-10.2f %-10.2f\n",$1,$2,$3,$4,$5,$6}'
rm dummy2_output.txt
rm game2_lb.csv

echo -e "\n===========Game3 Leaderboard=========="
printf "\n%-12s %-10s %-10s %-10s %-10s %-10s\n" "Player_name" "Played" "Wins" "Losses" "Win pct" "Loss pct"
sed -nE '/^[0-9]{2}-[0-9]{2}-[0-9]{4},Game3,[A-Za-z]+,[A-Za-z]+$/p' history.csv > game3_lb.csv
awk -F',' '
{

    winner=$3;
    loser=$4;
    played[winner]++;
    played[loser]++;
    wins[winner]++;
    losses[loser]++;
    losses[winner] = played[winner] - wins[winner];
    wins[loser] = played[loser] - losses[loser];

}
END {
for(name in played){ 
    win_pct = wins[name]*100/played[name];
    loss_pct = losses[name]*100/played[name];
    printf "%s\t %d\t %d\t %d\t %d\t %d\n",name,played[name],wins[name],losses[name],win_pct,loss_pct >> "dummy3_output.txt"
}

}
' game3_lb.csv
sort -n -t$'\t' -k4 dummy3_output.txt | awk -F'\t' '{printf"%-12s %-10d %-10d %-10d %-10.2f %-10.2f\n",$1,$2,$3,$4,$5,$6}'
rm dummy3_output.txt
rm game3_lb.csv
