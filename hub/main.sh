#!/usr/bin/env bash
Player_count=0
declare -a Logged_in_users
Start(){
    while (( Player_count < 2 ));do
        read -p "Do you want to register or login: " Login_Register
        if [[ $Login_Register == "Login" ]];then
        Login
        elif [[ $Login_Register == "Register" ]];then
        Register
        else
        echo "Invalid Choice."
        fi
    done
    echo "------------------------------------------"
    echo "Player Limit reached! Players: ${Logged_in_users[*]}"
    echo "Launching Game..."
    python3 game.py "${Logged_in_users[@]}"
}
Login(){
    read -p "Enter your Username: " Username
    read -sp "Enter your password: " Password
    echo ""
    if cut -f 1 users.tsv| grep -qw "$Username";then
        hashed_user_password=$(printf "%s" "$Password" | sha256sum | awk '{print $1}')
        actual_user_password=$(grep "^${Username}"$'\t' users.tsv |cut -f 2 )
        if [[ $hashed_user_password == $actual_user_password ]];then
            echo "Successfully logged in "
            echo "------------------------------------------"
            Logged_in_users[$Player_count]=$Username
            ((Player_count++))
        else echo "Please enter valid credentials"
        fi
    else echo "Username does not exist"
    fi
}
Register(){
    read -p "Enter your Username: " Username
    read -sp "Enter your password: " Password
    echo ""
    if cut -f 1 users.tsv| grep -qw "$Username";then
        echo "Username already exists"
    else
        hashed_password_user1=$(printf "%s" "$Password" | sha256sum | awk '{print $1}')
        echo -e "${Username}\t${hashed_password_user1}" >> users.tsv
            Logged_in_users[$Player_count]=$Username
            ((Player_count++))
            echo "Registeration Complete"
            echo "------------------------------------------"
    fi
}
echo "-----------WELCOME TO MINIGAMEHUB-----------"
Start
