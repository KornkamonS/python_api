
import datetime


class Config:
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_BLACKLIST_ENABLED = True
    SECRET_KEY = "test2"
    JWT_SECRET_KEY = "test1"
    DEBUG = False 
    DATABASE_URL="mongodb://db"
    DATABASE_PORT=27017
    DATABASE_NAME="Restplus"
    HOST = '0.0.0.0'
    SERVER_PORT = 80
    LOCAL = False
    CUDA = True
    ENV = "production"
    ERROR_404_HELP = False


class DevelopmentLocalConfig(Config):
    ENV = "development"
    DATABASE_URL="mongodb://localhost"
    DATABASE_NAME="Restplus_Dev"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)
    LOCAL = True
    DEBUG = True
    CUDA = False
    HOST = '127.0.0.1'


class DevelopmentDockerConfig(Config):
    ENV = "development"
    DATABASE_NAME="Restplus_Dev"
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)
    DEBUG = True
    CUDA = False
    HOST = '0.0.0.0'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_NAME="Restplus_Test"


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev_local = DevelopmentLocalConfig,
    dev_docker = DevelopmentDockerConfig,
    test = TestingConfig,
    prod = ProductionConfig
)

key = Config.SECRET_KEY
