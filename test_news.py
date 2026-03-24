import pytest
from unittest.mock import patch
from environment import ENVIRONMENT
from news.news_api_service import NewsApiService
from news.news_db_service import NewsDbService
from database.database_client import DatabaseClient

@pytest.fixture
def mock_get():
    with patch('requests.get') as mock_response:
        yield mock_response


def test_get_articles(mock_get):
    #Set up mock
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'status': 'ok',
        'articles': [
            {
                #blank article to have fetch_date affixed to
            }
        ]
    }
    #Initialize Service
    environment = ENVIRONMENT()

    news_api_key = environment.get('news_api_key')
    news_api_url = environment.get('news_api_url')
    news_api_service = NewsApiService(news_api_url, news_api_key)

    #Test success handling
    response = news_api_service.fetch_articles('2000-00-00')
    assert len(response) == 1
    assert response[0]['fetch_date'] == '2000-00-00'

def test_get_articles_error_status(mock_get):
    #Set up mock
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'status': 'error',
        'articles': [
            {
                #blank article to have fetch_date affixed to
            }
        ]
    }
    #Initialize Service
    environment = ENVIRONMENT()

    news_api_key = environment.get('news_api_key')
    news_api_url = environment.get('news_api_url')
    news_api_service = NewsApiService(news_api_url, news_api_key)

    #Test failure handling
    with pytest.raises(Exception):
        news_api_service.fetch_articles('')

def test_get_params():
    news_api_sevice = NewsApiService('mock_url', 'mock_key')
    params = news_api_sevice.get_params('mock_date')
    assert params['apiKey'] == 'mock_key'
    assert params['from'] == 'mock_date'

def test_set_fetch_date():
    news_api_sevice = NewsApiService('mock_url', 'mock_key')
    result = news_api_sevice.set_fetch_date([{}], '2000-00-00')
    assert result[0]['fetch_date'] == '2000-00-00'

def test_insert_articles():
    #Initialize db connection with is_test=True to avoid messing with real data
    environment = ENVIRONMENT()
    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')

    database_client = DatabaseClient(mongodb_connstring, mongodb_name, is_test=True)

    assert database_client.is_connected() == True

    news_collection = database_client.get_news_collection()
    news_db_service = NewsDbService(news_collection)

    #Empty it out so we know we're starting fresh
    news_collection.delete_many({})

    news_db_service.insert_articles([{
        'fetch_date': '2000-00-00',
        'title': 'test article 1'
    }], selected_date='2000-00-00')


    assert news_collection.count_documents({}) == 1

    #Run again with a different date, make sure we don't delete the old one, since the dates don't match
    news_db_service.insert_articles([{
        'fetch_date': '2000-01-01',
        'title': 'test article 1'
    }], selected_date='2000-01-01')

    assert news_collection.count_documents({}) == 2

    news_collection.delete_many({})

    database_client.close_client()






    
        

