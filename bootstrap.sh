#!/bin/bash

debconf-set-selections <<< 'mysql-server mysql-server/root_password password ispepsiokay'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password ispepsiokay'

PROJECT_DIR=/home/vagrant/is-pepsi-okay
PROJECT_NAME=IsPepsiOkay

# install
sudo apt-get update
sudo apt-get install -y git
sudo apt-get install -y vim
sudo apt-get install -y libmysqlclient-dev
sudo apt-get install -y python-dev
sudo apt-get install -y python-virtualenv
sudo apt-get install -y mysql-server
sudo apt-get install -y mysql-client
sudo apt-get install -y nginx
sudo apt-get install -y supervisor

# python requirements
cd $PROJECT_DIR
sudo apt-get -y remove python-pip
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py > /dev/null 2>&1
sudo python get-pip.py
rm get-pip.py
sudo pip install -r $PROJECT_DIR/requirements.txt

# start web server
#cd $PROJECT_DIR/$PROJECT_NAME
#sudo gunicorn -D --max-requests 1 $PROJECT_NAME:app -b 127.0.0.1:8000

#sudo /etc/init.d/nginx start

#sudo rm -f /etc/nginx/sites-enabled/default
#sudo rm -f /etc/nginx/sites-available/is-pepsi-okay
#sudo touch /etc/nginx/sites-available/is-pepsi-okay
#sudo rm -f /etc/nginx/sites-enabled/is-pepsi-okay
#sudo ln -s /etc/nginx/sites-available/is-pepsi-okay /etc/nginx/sites-enabled/is-pepsi-okay
#sudo printf 'server {\n\tlocation / {\n\t\tproxy_pass http://127.0.0.1:8000;\n\t}\n}' >> /etc/nginx/sites-available/is-pepsi-okay

#sudo /etc/init.d/nginx restart

#cd $PROJECT_DIR/$PROJECT_NAME
#sudo gunicorn -D --max-requests 1 $PROJECT_NAME:app -b localhost:8000

# mysql initialize
mysql -uroot -pispepsiokay < $PROJECT_DIR/$PROJECT_NAME/database/schema.sql
mysql -uroot -pispepsiokay < $PROJECT_DIR/$PROJECT_NAME/database/dump.sql

sudo apt-get install -y python-mysqldb

cd $PROJECT_DIR
sudo ./runserver.py

echo "Navigate to 33.33.33.33 in your web browser!"
