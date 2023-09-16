#!/bin/bash

cd ./

git pull

sudo systemctl restart ecourse
echo "Restarting Services..."
sudo systemctl restart nginx
echo "Restarting Nginx..."
