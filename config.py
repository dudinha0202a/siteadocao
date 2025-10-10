import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-adocao")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///instance/adocao.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True