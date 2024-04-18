#!/bin/bash
source /home/sam/Desktop/DirkjanBot/venv/bin/activate
python /home/sam/Desktop/DirkjanBot/main_single.py
deactivate
sudo /usr/sbin/shutdown -h now
