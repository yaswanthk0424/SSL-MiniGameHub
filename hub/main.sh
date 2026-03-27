#!/usr/bin/env bash
Player_count=0
declare -a Logged_in_users
Start(){
    while (( Player_count < 2 ));do
        read -p $'\e[33mDo you want to Register or Login: \e[0m' Login_Register
        if [[ $Login_Register == "Login" ]];then
            Login
        elif [[ $Login_Register == "Register" ]];then
            Register
        else
            echo -e "\e[31mError: Invalid Choice.\e[0m"
            echo -e "\e[36m------------------------------------------\e[0m"
        fi
    done
    echo -e "\e[36m------------------------------------------\e[0m"
    echo -e "\e[36mPlayer Limit reached! Players: ${Logged_in_users[*]}\e[0m"
    echo -e "\e[32mLaunching Game...\e[0m"
    python3 game.py "${Logged_in_users[@]}"
}
Login(){
    read -p $'\e[33mEnter your Username: \e[0m' Username
    read -sp $'\e[33mEnter your password: \e[0m' Password
    echo ""
        for Player in "${Logged_in_users[@]}";do
            if [[ $Username == $Player ]];then
                echo -e "\e[31mError:$Username is already logged in.\e[0m"
                echo -e "\e[36m------------------------------------------\e[0m"
                return
            fi
        done
    if cut -f 1 users.tsv| grep -qw "$Username";then
        hashed_user_password=$(printf "%s" "$Password" | sha256sum | awk '{print $1}')
        actual_user_password=$(grep "^${Username}"$'\t' users.tsv |cut -f 2 )
        if [[ $hashed_user_password == $actual_user_password ]];then
            echo -e "\e[32mSuccessfully logged in.\e[0m"
            echo -e "\e[36m------------------------------------------\e[0m"
            Logged_in_users[$Player_count]=$Username
            ((Player_count++))
        else echo -e "\e[31mPlease enter valid credentials\e[0m"
             echo -e "\e[36m------------------------------------------\e[0m"
        fi
    else echo -e "\e[31mUsername does not exist\e[0m" 
         echo -e "\e[36m------------------------------------------\e[0m"
    fi
}
Register(){
    read -p $'\e[33mEnter your Username: \e[0m' Username
    read -sp $'\e[33mEnter your password: \e[0m' Password
    echo ""
    for Player in "${Logged_in_users[@]}";do
        if [[ $Username == $Player ]];then
            echo -e "\e[31m$Username is already logged in.\e[0m"
            echo -e "\e[36m------------------------------------------\e[0m"
            return
        fi
    done
    if cut -f 1 users.tsv| grep -qw "$Username";then
        echo -e "\e[31mUsername already exists\e[0m"
    else
        hashed_password_user1=$(printf "%s" "$Password" | sha256sum | awk '{print $1}')
        echo -e "${Username}\t${hashed_password_user1}" >> users.tsv
            Logged_in_users[$Player_count]=$Username
            ((Player_count++))
            echo -e "\e[32mRegisteration Complete\e[0m"
            echo -e "\e[36m------------------------------------------\e[0m"
    fi
}
echo -e "\e[36m             ----------WELCOME TO MINIGAMEHUB----------\e[0m                 "
Start