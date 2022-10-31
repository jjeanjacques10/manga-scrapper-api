#!/bin/bash

echo 'Starting to Deploy...'

# Install required dependencies
sudo apt-get update
sudo apt-get upgrade
yes | sudo apt-get install nginx
yes | sudo apt install apt-transport-https ca-certificates curl software-properties-common
yes | curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
yes | sudo apt install docker-ce

# make sure manga-scrapper docker is not running
sudo docker rm $(sudo docker stop $(sudo docker ps -a -q --filter ancestor=manga-scrapper:latest --format="{{.ID}}"))

# copy nginx conf to default
sudo cp nginx.conf /etc/nginx/conf.d/default.conf

sudo systemctl restart nginx

# build dockerfile
sudo docker build -f dockerfile -t manga-scrapper:latest .

# run in detached mode
sudo docker run -p 3000:3000 -d manga-scrapper:latest

sleep 15

PORT=3000

echo 'Deployment completed successfully'