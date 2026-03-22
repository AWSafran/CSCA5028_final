from environment import ENVIRONMENT
from news.news_api_service import NewsApiService
from database.database_client import DatabaseClient
from datetime import date, timedelta

def main():
    # Load ENV variables
    environment = ENVIRONMENT()

    today = date.today()
    yesterday = today - timedelta(days = 2)

    #Connect to Database
    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')

    database_client = DatabaseClient(mongodb_connstring, mongodb_name)

    if database_client.is_connected():
        print('Successfully connected to database')

    #Fetch News Data
    news_api_key = environment.get('news_api_key')
    news_api_url = environment.get('news_api_url')
    news_api_service = NewsApiService(news_api_url, news_api_key)

    articles = news_api_service.fetch_articles(yesterday)

    #Store News Data
    news_collection = database_client.get_news_collection()
    news_collection.insert_many(articles)

    #Fetch Stock Data

    #Store Stock Data

    #Log Date Collected

    #Send Message with Date



if __name__ == "__main__":
    main()