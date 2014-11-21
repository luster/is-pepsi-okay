#!/bin/bash

read -p "Are you sure you want to erase and reinitialize db? [y/N] " -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Resetting db..."
    mysql -uroot -pispepsiokay < /home/vagrant/is-pepsi-okay/IsPepsiOkay/database/schema.sql
fi

