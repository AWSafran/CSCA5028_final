import os
from dotenv import load_dotenv

class ENVIRONMENT:
    vars = {}

    def __init__(self):
        load_dotenv()
        
        self.vars['mongodb_connstring'] = os.getenv('mongodb_connstring')
        self.vars['mongodb_name'] = os.getenv('mongodb_name')
        self.vars['is_prod'] = os.getenv('is_prod')
        self.vars['news_api_key'] = os.getenv('news_api_key')
        self.vars['news_api_url'] = os.getenv('news_api_url')
        self.vars['stock_api_url'] = os.getenv('stock_api_url')
        self.vars['stock_api_key'] = os.getenv('stock_api_key')

    def get(self, key):
        return self.vars[key]