import os

class Config:
    TESTING = False
    ENV_VAR = os.environ.get('ENV_VAR')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    BING = os.environ.get('BING')

class ProductionConfig(Config):
    FAV_FLOWER = 'rose'

class DevelopmentConfig(Config):
    FAV_FLOWER = 'sunflower'

class TestingConfig(Config):
    FAV_FLOWER = 'moonlight petal'
    TESTING = True