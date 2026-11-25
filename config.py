import os
from pathlib import Path

BASEDIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-this-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{BASEDIR / 'data.sqlite'}"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or f"sqlite:///{BASEDIR / 'data-dev.sqlite'}"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    @staticmethod
    def init_app(app):
        if not app.config.get("SECRET_KEY"):
            app.logger.warning("Configure SECRET_KEY nas variáveis de ambiente do PythonAnywhere.")

config = {"development": DevelopmentConfig, "testing": TestingConfig, "production": ProductionConfig, "default": DevelopmentConfig}
