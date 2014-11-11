
import os

PROJECT = "IsPepsiOkay"

class BaseConfig(object):

    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')

    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = 'ispepsiokay'
    MYSQL_DATABASE_DB = 'IsPepsiOkay'

class ProductionConfig(BaseConfig):
    DEBUG = False
