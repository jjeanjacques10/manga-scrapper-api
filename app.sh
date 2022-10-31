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
sudo docker build --build-arg AWS_ACCESS_KEY_ID=$1 \
    --build-arg AWS_SECRET_ACCESS_KEY=$2 \
    --build-arg AWS_DEFAULT_REGION=$3 \
    -f dockerfile -t manga-scrapper:latest .

echo 'AWS default region: ' $3

# run in detached mode
sudo docker run -p 3000:3000 -d manga-scrapper:latest

sleep 15

PORT=3000

echo 'Deployment completed successfully'