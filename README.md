Is Pepsi Okay?
=============

Movie Recommendation Semester Project for ECE464 Databases, Fall 2014 at Cooper Union

## Stack

- MySQL
- Python/Flask
- gunicorn
- nginx

## Get Started (Production-like Environment)

1. Install [Vagrant](https://www.vagrantup.com/downloads).
2. clone the repo
3. ```vagrant up```
4. Then go to [http://33.33.33.33](http://33.33.33.33) to see the app.

You can modify the code on your local machine. The folder is synced with vagrant, and you can immediately see your changes reflected in the browser. To see errors in the browser (debug on), login to the VM and run the development server

    vagrant ssh
    cd is-pepsi-okay
    python app.py
    
Then go to [localhost:5000](http://localhost:5000) to see the app.

## TODO

- find dataset(s)
- populate tables (python scripts)
- consider using one database instead of local
- write some sample queries


## Authors

- Ethan Lusterman
- Joe Mercedes
