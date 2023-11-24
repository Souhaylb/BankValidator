import os

root_path = "/resources/"
redis_port = os.getenv("REDIS_PORT", 6379)
redis_host = os.getenv("REDIS_HOST", 'redis')
redis_trainingDataKey = os.getenv("REDIS_TRAINING_DATA_KEY", 'TrainingData')
redis_training_data_field_key = os.getenv("REDIS_TRAINING_DATA_FIELD_KEY", 'TrainingDataField')
redis_training_data_columns_key = os.getenv("REDIS_TRAINING_DATA_COLUMNS_KEY", 'TrainingDataColumns')


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    STATIC_FOLDER = "static/"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False
    ENV = "dev"


config = {
    "dev": "config.DevelopmentConfig",
    "default": "config.DevelopmentConfig",
}


def configure_app(app):
    global root_path
    config_name = os.getenv("FLASK_CONFIGURATION", "default")
    app.config.from_object(config[config_name])
    root_path = os.path.dirname(app.root_path) + root_path
    app.root_path = root_path
