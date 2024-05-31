from pymongo.mongo_client import MongoClient

import config

client = MongoClient(config.MONGO_URI)
database = client[config.DATABASE_KAPITA_SELEKTA]
user_collection = database[config.USER_COLLECTION]
product_collection = database[config.PRODUCT_COLLECTION]
transaction_collection = database[config.TRANSACTION_COLLECTION]
