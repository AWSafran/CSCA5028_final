import responses
from main import main
from environment import ENVIRONMENT
from database.database_client import DatabaseClient
import re, json

TEST_FETCH_DATE = '2020-01-01'

MOCK_ARTICLES = {
    "status":"ok",
    "totalResults":204987,
    "articles":[
        {
            "source":{
                "id":"usa-today",
                "name":"USA Today"
            },
            "author":"BrieAnna J. Frank, USA TODAY",
            "title":"TESTARTICLE1",
            "url":"https://www.usatoday.com/story/news/factcheck/2024/05/13/mtg-marjorie-taylor-green-trump-trial-judge-fact-check/73653252007/",
            "urlToImage":"https://s.yimg.com/ny/api/res/1.2/uZ57uVnFvNwAS7vZ0ULvOA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyMDA7aD04MDA-/https://media.zenfs.com/en/usa_today_news_641/55b0b2582e2a44ee19262ec8d9ee923a",
            "publishedAt":"2024-05-13T18:45:20Z",
            "content":"The claim: Rep. Marjorie Taylor Green said judge forced Trump to delete Stormy Daniels post\r\nA May 3 Facebook post (direct link, archive link) includes a screenshot of a statement on X, formerly Twit… [+4518 chars]"
        },
        {
            "source":
                {
                    "id":"usa-today",
                    "name":"USA Today"
                },
            "author":"Julia Gomez, USA TODAY",
            "title":"TESTARTICLE2",
            "description":"Body cams caught the moment officers were left shocked by the aftermath of the Francis Scott Key Bridge collapse in Baltimore.",
            "url":"https://www.usatoday.com/story/news/nation/2024/05/12/francis-scott-key-bridge-collapse-reaction-on-body-cam-footage/73664029007/",
            "urlToImage":"https://s.yimg.com/ny/api/res/1.2/j6xaDmrmsuYAxP.12u9uMQ--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyMDA7aD04MDA-/https://media.zenfs.com/en/austin_american_statesman_natl_articles_871/36a115828a43e4d7fda7f8ba2884ec65",
            "publishedAt":"2024-05-12T16:59:00Z",
            "content":"Body camera footage caught the moment first responders were left shocked by the Baltimore bridge collapse.\r\n\"This is [expletive] bad,\" one officer is heard saying in the footage. \"Like, there is no b… [+1667 chars]"
        }
    ]
}

MOCK_STOCKS = {
    "queryCount":11771,
    "resultsCount":11771,
    "adjusted":True,
    "status": "OK",
    "results": [
        {"T":"STOCK1","v":71017,"vw":30.4265,"o":30.42,"c":30.33,"h":30.49,"l":30.3101,"t":1767387600000,"n":318},
        {"T":"STOCK2","v":89769,"vw":0.6606,"o":0.6613,"c":0.6587,"h":0.6771,"l":0.6427,"t":1767387600000,"n":567}
    ]
}

@responses.activate
def test_integration():
    #Initialize Test DB Connection
    environment = ENVIRONMENT()
    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')

    database_client = DatabaseClient(mongodb_connstring, mongodb_name, is_test=True)

    assert database_client.is_connected() == True

    #Clear out any existing test data
    stock_collection = database_client.get_stock_collection()
    stock_collection.delete_many({})

    news_collection = database_client.get_news_collection()
    news_collection.delete_many({})

    news_regex = re.compile("https://newsapi.org")

    stocks_regex = re.compile("https://api.massive.com")

    news_mock_response = responses.Response(
        method="GET",
        url=news_regex,
        json=MOCK_ARTICLES
    )

    responses.add(news_mock_response)

    stock_mock_response = responses.Response(
        method="GET",
        url=stocks_regex,
        json=MOCK_STOCKS
    )

    responses.add(stock_mock_response)

    main(TEST_FETCH_DATE, True)
    
    collected_stocks = list(stock_collection.find({ "fetch_date": TEST_FETCH_DATE }))

    collected_articles = list(news_collection.find({ "fetch_date": TEST_FETCH_DATE }))

    assert len(collected_stocks) == 2
    assert collected_stocks[0]['T'] == 'STOCK1'
    assert collected_stocks[1]['T'] == 'STOCK2'

    assert len(collected_articles) == 2
    assert collected_articles[0]['title'] == 'TESTARTICLE1'
    assert collected_articles[1]['title'] == 'TESTARTICLE2'



    #teardown
    #Clear out any newly generated test data
    stock_collection.delete_many({})

    news_collection = database_client.get_news_collection()

    database_client.close_client()