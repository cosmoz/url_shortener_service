class Config(object):
    DEBUG = False
    TESTING = False
    REDIS_URI = 'sqlite://:memory:'

class ProductionConfig(Config):
    REDIS_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
