class StockDbService:
    def __init__(self, stock_collection):
        self.stock_collection = stock_collection

    def insert_stocks(self, stocks, selected_date):
        if len(stocks) > 0:
            # If we've already fetched this date, do nothing - too much data to delete and re-insert
            query_filter = { 'fetch_date': selected_date }
            existing_stock_count = self.stock_collection.count_documents(query_filter)

            if existing_stock_count == 0:
                self.stock_collection.insert_many(stocks)