from redis import Redis
from config import redis_port, redis_host, redis_trainingDataKey, redis_training_data_field_key, redis_training_data_columns_key
import json

redis = Redis(host=redis_host, port=redis_port)


def saveTrainingDataOrder(datas):
    redis.set(redis_trainingDataKey, json.dumps(datas))


def getTrainingDataOrder():
    try:
        return json.loads(redis.get(redis_trainingDataKey))
    except:
        return None


def saveTrainingDataField(datas):
    redis.set(redis_training_data_field_key, json.dumps(datas))


def getTrainingDataField():
    try:
        return json.loads(redis.get(redis_training_data_field_key))
    except:
        return None

def saveTrainingDatacColumns(datas):
    redis.set(redis_training_data_columns_key, json.dumps(datas))


def getTrainingDataColumns():
    try:
        return json.loads(redis.get(redis_training_data_columns_key))
    except:
        return None


