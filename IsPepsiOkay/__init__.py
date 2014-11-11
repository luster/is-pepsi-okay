from flask import Flask
from database.database import Database
from IsPepsiOkay.config import BaseConfig, PROJECT
from flask.ext.login import LoginManager

app = Flask(PROJECT)
app.config.from_object(BaseConfig)
login_manager = LoginManager()
login_manager.setup_app(app)
database = Database(app)

import IsPepsiOkay.views

if __name__ == '__main__':
    app.run()
