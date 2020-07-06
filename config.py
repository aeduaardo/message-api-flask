from pymongo import MongoClient

mongo_conn = MongoClient()
db = mongo_conn['flask-api']