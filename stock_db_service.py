class StockDbService:
    def __init__(self, stock_collection):
        self.stock_collection = stock_collection

    def get_daily_stocks(self, selected_date):
        query_filter = { 'fetch_date': selected_date, 'o': { '$ne': 0} }
        return self.stock_collection.find(query_filter)
    
    def purge_daily_stocks(self, selected_date):
        query_filter = { 'fetch_date': selected_date }
        self.stock_collection.delete_many(query_filter)