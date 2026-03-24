import pytest
from unittest.mock import patch
from environment import ENVIRONMENT
from stock.stock_api_service import StockApiService
from stock.stock_db_service import StockDbService
from database.database_client import DatabaseClient

@pytest.fixture
def mock_get():
    with patch('requests.get') as mock_response:
        yield mock_response


def test_get_stocks(mock_get):
    #Set up mock
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'status': 'OK',
        'results': [
            {
                #blank stock listing to have fetch_date affixed to
            }
        ]
    }
    #Initialize Service
    environment = ENVIRONMENT()

    stock_api_key = environment.get('stock_api_key')
    stock_api_url = environment.get('stock_api_url')
    stock_api_service = StockApiService(stock_api_url, stock_api_key)

    #Test success handling
    response = stock_api_service.fetch_stocks('2000-00-00')
    assert len(response) == 1
    assert response[0]['fetch_date'] == '2000-00-00'

def test_get_stockss_error_status(mock_get):
    #Set up mock
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'status': 'ERROR',
        'reults': [
            {
                #blank article to have fetch_date affixed to
            }
        ]
    }
    #Initialize Service
    environment = ENVIRONMENT()

    stock_api_key = environment.get('stock_api_key')
    stock_api_url = environment.get('stock_api_url')
    stock_api_service = StockApiService(stock_api_url, stock_api_key)

    #Test failure handling
    with pytest.raises(Exception):
        stock_api_service.fetch_stocks('2000-00-00')

def test_build_url():
    stock_api_service = StockApiService('mock_url', 'mock_key')
    url = stock_api_service.build_url('mock_date')
    assert url == 'mock_url/mock_date?apiKey=mock_key'

def test_set_fetch_date():
    stock_api_sevice = StockApiService('mock_url', 'mock_key')
    result = stock_api_sevice.set_fetch_date([{}], '2000-00-00')
    assert result[0]['fetch_date'] == '2000-00-00'

def test_insert_articles():
    #Initialize db connection with is_test=True to avoid messing with real data
    environment = ENVIRONMENT()
    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')

    database_client = DatabaseClient(mongodb_connstring, mongodb_name, is_test=True)

    assert database_client.is_connected() == True

    stock_collection = database_client.get_stock_collection()
    stock_db_service = StockDbService(stock_collection)

    #Empty it out so we know we're starting fresh
    stock_collection.delete_many({})

    stock_db_service.insert_stocks([{
        'fetch_date': '2000-00-00',
        'stock': 'test stock 1'
    }], selected_date='2000-00-00')


    assert stock_collection.count_documents({}) == 1

    #Run again with a different date, make sure we don't delete the old one, since the dates don't match
    stock_db_service.insert_stocks([{
        'fetch_date': '2000-01-01',
        'title': 'test article 1'
    }], selected_date='2000-01-01')

    assert stock_collection.count_documents({}) == 2

    stock_collection.delete_many({})

    database_client.close_client()






    
        

