#!/bin/bash
#package installation file, now dont need to use all cmds seperately just run this file and it will do its work xD
#VORTEX
# Check if the script is being run as root (required for package installation)
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root or using sudo."
    exit 1
fi

# Update package information
sudo apt-get update -y
sudo apt update; sudo apt install software-properties-common -y
sudo chmod 777 bombsquad_server dist/bombsquad_headless


# Add the repository for Python 3.10
sudo add-apt-repository -y ppa:deadsnakes/ppa

# Install Python 3.10
sudo apt-get install python3.10 -y

# Install the development library for Python 3.10
sudo apt-get install libpython3.10 -y

#intall the pip
sudo apt install python3-pip -y

#fix the perms for aws ubuntu
sudo chown -R ubuntu:ubuntu /home/ubuntu/VH-Bombsquad-Modded-Server-Files

#install the pymongo and psutil and ping3
pip3 install ping3 --target=/usr/lib/python3.10
pip3 install pymongo --target=/usr/lib/python3.10
pip3 install psutil --target=/usr/lib/python3.10
pip3 install --upgrade discord.py --target=/usr/lib/python3.10


# Additional commands or post-installation actions can be added here
