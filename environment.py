import os
from dotenv import load_dotenv

class ENVIRONMENT:
    vars = {}

    def __init__(self):
        load_dotenv()
        
        self.vars['mongodb_connstring'] = os.getenv('mongodb_connstring')
        self.vars['mongodb_name'] = os.getenv('mongodb_name')

    def get(self, key):
        return self.vars[key]