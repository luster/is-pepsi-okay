#!/bin/bash

debconf-set-selections <<< 'mysql-server mysql-server/root_password password ispepsiokay'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password ispepsiokay'

PROJECT_DIR=/home/vagrant/is-pepsi-okay

# install
sudo apt-get update
sudo apt-get install -y python-pip
sudo apt-get install -y git
sudo apt-get install -y vim
sudo apt-get install -y libmysqlclient-dev
sudo apt-get install -y python-dev
sudo apt-get install -y mysql-server
sudo apt-get install -y mysql-client
sudo apt-get install -y nginx
sudo apt-get install -y supervisor
sudo apt-get update

# python requirements
sudo pip install -r $PROJECT_DIR/requirements.txt

# start web server
cd $PROJECT_DIR
sudo gunicorn -D --max-requests 1 app:app -b 127.0.0.1:8000

sudo /etc/init.d/nginx start

sudo rm -f /etc/nginx/sites-enabled/default
sudo rm -f /etc/nginx/sites-available/is-pepsi-okay
sudo touch /etc/nginx/sites-available/is-pepsi-okay
sudo rm -f /etc/nginx/sites-enabled/is-pepsi-okay
sudo ln -s /etc/nginx/sites-available/is-pepsi-okay /etc/nginx/sites-enabled/is-pepsi-okay
sudo printf 'server {\n\tlocation / {\n\t\tproxy_pass http://127.0.0.1:8000;\n\t}\n}' >> /etc/nginx/sites-available/is-pepsi-okay

sudo /etc/init.d/nginx restart

cd $PROJECT_DIR
sudo gunicorn -D --max-requests 1 app:app -b localhost:8000

# mysql initialize
mysql -uroot -pispepsiokay < $PROJECT_DIR/database/schema.sql
