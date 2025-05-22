# config.py
import os

class Config:
    SECRET_KEY = 'cc38dd4b149d6aac8f5c6e7fae70d4a0'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/harvester_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
