#!/bin/bash

main () {
    echo "This script will install all necessary dependencies...."
    choice=`read -r "Have you cloned the repository(y/n)? "`
    sudo apt update
    if [ $choice == 'n' ]; then
        cd /opt/
        sudo git clone https://github.com/Dheemn/MissionBot.git
        cd MissionBot/
    fi
    echo "Installing python dependencies..."
    python3 -m pip install --user virtualenv
    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    echo "Creating service file for the discord bot...."
    sudo cp -i service/bot.service /etc/systemd/system/
    sudo systemctl daemon-reload
    echo "Please configure the settings for the bot..."
    python setup.py
    echo "Installation done..!!"
    echo "To start bot, execute 'systemctl start bot.service'"
    echo "To start bot at startup, execute 'systemctl enable bot.service'"
    echo "Make sure to have discord bot's token set in env file"
}

main
