class NewsDbService:
    def __init__(self, news_collection):
        self.news_collection = news_collection

    def insert_articles(self, articles, selected_date):
        if len(articles) > 0:
            # If we've already fetched this date, replace the articles so we are always limited to 10
            query_filter = { 'fetch_date': selected_date}
            self.news_collection.delete_many(query_filter)

            self.news_collection.insert_many(articles)