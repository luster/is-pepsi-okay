Is Pepsi Okay?
=============

Movie Recommendation Semester Project for ECE464 Databases, Fall 2014 at Cooper Union

## Stack

- MySQL
- Python/Flask

## Get Started

0. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
1. Install [Vagrant](https://www.vagrantup.com/downloads).
2. clone the repo
3. `cd is-pepsi-okay`
3. `vagrant up`
4. Then go to [http://33.33.33.33](http://33.33.33.33) to see the app.

## Bootstrap your own system

1. Ensure MySQL is running
2. Make sure database `IsPepsiOkay` is installed with -uroot and -pispepsiokay
3. Populate database with `mysql -uroot -pispepsiokay < IsPepsiOkay/database/dump.sql`
4. Install python requirements on virtualenv with `virtualenv flask; source flask; pip install -r requirements.txt` 
2. Run flask server with `sudo python runserver.py`
4. Then go to [http://33.33.33.33](http://33.33.33.33) to see the app.

## Authors

- Ethan Lusterman
- Joe Mercedes
