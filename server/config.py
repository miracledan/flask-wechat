import os
import logging
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    PROJECT_NAME = 'wechat'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    LOG_FILE = '/var/log/%s.log' % PROJECT_NAME
    LOG_MAX_BYTES = 10000
    LOG_BACKUP_COUNT = 1
    LOG_FORMATTER = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} " \
        "%(levelname)s - %(message)s")
    LOG_LEVEL = logging.DEBUG
    
    @staticmethod
    def init_app(cls, app):
        # config log
        from logging.handlers import RotatingFileHandler
        handler = RotatingFileHandler(cls.LOG_FILE, maxBytes=cls.LOG_MAX_BYTES, 
            backupCount=cls.LOG_BACKUP_COUNT)
        handler.setLevel(cls.LOG_LEVEL)
        handler.setFormatter(cls.LOG_FORMATTER)
        app.logger.addHandler(handler)

class DevelopmentConfig(Config):
    DEBUG = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(cls, app)

class ProductConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(cls, app)

config = {
    'default': DevelopmentConfig,
    'product': ProductConfig
}
