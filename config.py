import os
import yaml
import logging

logger = logging.getLogger(__name__)

def load_yaml_config(config_name):
    with open('config.yaml', 'r') as f:
        config_data = yaml.safe_load(f)
    logger.info(f"Loaded configuration for {config_name}")
    return config_data.get(config_name, {})

class Config:
    config_data = load_yaml_config('default')
    SECRET_KEY = config_data.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = config_data.get('SQLALCHEMY_DATABASE_URI')
    SPIDER_URL = config_data.get('SPIDER_URL')
    AUTHORIZATION = config_data.get('AUTHORIZATION')
    
    @staticmethod
    def init_app(app):
        logger.info("Initializing app with default configuration")

class DevelopmentConfig(Config):
    config_data = load_yaml_config('development')
    DEBUG = config_data.get('DEBUG', False)
    logger.info("Development configuration loaded")

class TestingConfig(Config):
    config_data = load_yaml_config('testing')
    TESTING = config_data.get('TESTING', False)
    logger.info("Testing configuration loaded")

class ProductionConfig(Config):
    config_data = load_yaml_config('production')
    SQLALCHEMY_DATABASE_URI = config_data.get('SQLALCHEMY_DATABASE_URI', Config.SQLALCHEMY_DATABASE_URI)
    logger.info("Production configuration loaded")

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
