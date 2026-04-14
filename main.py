from environment import ENVIRONMENT
from news.news_api_service import NewsApiService
from news.news_db_service import NewsDbService
from stock.stock_api_service import StockApiService
from stock.stock_db_service import StockDbService
from database.database_client import DatabaseClient
from monitoring.logging_service import LoggingService
from datetime import date, timedelta
from mq.queue import send_date_to_queue
import sys

def main(collection_date_string, is_test=False):
    # Load ENV variables
    environment = ENVIRONMENT()
    print(collection_date_string)

    #Connect to Database

    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')

    database_client = DatabaseClient(mongodb_connstring, mongodb_name, is_test)

    if database_client.is_connected():
        print('Successfully connected to database')

    #Set up logging service
    logging_service = LoggingService(database_client.get_logging_collection())
    logging_service.log_info(collection_date_string, "Beginning Data Collection")
    #Set up news services

    try:
        news_api_key = environment.get('news_api_key')
        news_api_url = environment.get('news_api_url')
        news_api_service = NewsApiService(news_api_url, news_api_key)
        news_db_service = NewsDbService(database_client.get_news_collection())

        #Fetch and store News Data

        articles = news_api_service.fetch_articles(collection_date_string)
        news_db_service.insert_articles(articles, collection_date_string)
        
        logging_service.log_info(collection_date_string, "News Data Colelcted")

        #Set up stock services

        stock_api_key = environment.get('stock_api_key')
        stock_api_url = environment.get('stock_api_url')
        stock_api_service = StockApiService(stock_api_url, stock_api_key)
        stock_db_service = StockDbService(database_client.get_stock_collection())
        
        #Fetch and store Stock Data

        stocks = stock_api_service.fetch_stocks(collection_date_string)
        stock_db_service.insert_stocks(stocks, collection_date_string)
        
        logging_service.log_info(collection_date_string, "Stocks Data Colelcted")

        #Log Date Collected
        logging_service.log_info(collection_date_string, 'Data Collection Complete')
    except Exception as e:
        logging_service.log_error(collection_date_string, e)

    #Close db client connection
    database_client.close_client()

    #Send Message with Date
    send_date_to_queue(collection_date_string)


if __name__ == "__main__":
    if (len(sys.argv)) > 1:
        collection_date_string = sys.argv[1]
        main(collection_date_string)
    else:
        today = date.today()
        collection_date = today - timedelta(days = 2)
        collection_date_string = collection_date.isoformat()
        main(collection_date_string)