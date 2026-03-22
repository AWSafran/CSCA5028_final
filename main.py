from environment import ENVIRONMENT
from news.news_api_service import NewsApiService
from news.news_db_service import NewsDbService
from stock.stock_api_service import StockApiService
from stock.stock_db_service import StockDbService
from database.database_client import DatabaseClient
from datetime import date, timedelta

def main():
    # Load ENV variables
    environment = ENVIRONMENT()

    today = date.today()
    collection_date = today - timedelta(days = 2)
    collection_date_string = collection_date.isoformat()

    #Connect to Database

    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')

    database_client = DatabaseClient(mongodb_connstring, mongodb_name)

    if database_client.is_connected():
        print('Successfully connected to database')

    #Set up news services

    news_api_key = environment.get('news_api_key')
    news_api_url = environment.get('news_api_url')
    news_api_service = NewsApiService(news_api_url, news_api_key)
    news_db_service = NewsDbService(database_client.get_news_collection())

    #Fetch and store News Data

    articles = news_api_service.fetch_articles(collection_date_string)
    news_db_service.insert_articles(articles, collection_date_string)

    #Set up stock services

    stock_api_key = environment.get('stock_api_key')
    stock_api_url = environment.get('stock_api_url')
    stock_api_service = StockApiService(stock_api_url, stock_api_key)
    stock_db_service = StockDbService(database_client.get_stock_collection())
    #Fetch Stock Data

    stocks = stock_api_service.fetch_stocks(collection_date_string)
    stock_db_service.insert_stocks(stocks, collection_date_string)
    #Store Stock Data

    #Log Date Collected

    #Send Message with Date



if __name__ == "__main__":
    main()