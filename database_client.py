import pymongo
from pymongo import MongoClient, server_api

class DatabaseClient:
    def __init__(self, uri, db_name, is_test = False):
        self.client = MongoClient(uri, server_api=server_api.ServerApi(version="1", strict=True, deprecation_errors=True))
        self.db_name = db_name
        self.is_test = is_test

    def get_client(self):
        return self.client[self.db_name]
    
    def is_connected(self):
        is_connected = False
        try:
            self.client.admin.command('ping')
            is_connected = True
        except Exception as e:
            print('Error pinging database: ', e)

        return is_connected

    def close_client(self):
        self.client.close()

    def get_collection_by_name(self, name):
        client = self.get_client()
        if name not in client.list_collection_names():
            client.create_collection(name)
        return client[name]
    
    def get_stock_collection(self):
        collection_name = 'stock_test' if self.is_test else 'stock'
        return self.get_collection_by_name(collection_name)
    
    def get_stock_summary_collection(self):
        collection_name = 'stock_summary_test' if self.is_test else 'stock_summary'
        return self.get_collection_by_name(collection_name)
    
