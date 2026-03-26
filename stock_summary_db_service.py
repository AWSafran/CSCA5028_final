class StockSummaryDatabaseService:
    def __init__(self, stock_summary_collection):
        self.stock_summary_collection = stock_summary_collection

    def insert_summary(self, summary):
        #Use the latest data if we somehow already have one - should never happen
        delete_filter = { 'date': summary['date'] }
        self.stock_summary_collection.delete_one(delete_filter)

        self.stock_summary_collection.insert_one(summary)