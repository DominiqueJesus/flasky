import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    MAIL_RECIPIENT = os.environ.get("MAIL_RECIPIENT")
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_ADMIN_NAME = os.environ.get("FLASKY_ADMIN_NAME")
    FLASKY_ADMIN_ID = os.environ.get("FLASKY_ADMIN_ID")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_URL = os.environ.get("API_URL")
    API_KEY = os.environ.get("API_KEY")
    API_FROM = os.environ.get("API_FROM")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @staticmethod
    def init_app(app):
        if not app.config.get('SECRET_KEY'):
            raise RuntimeError('Defina SECRET_KEY no ambiente de produção.')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}