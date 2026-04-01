from flask import abort, Blueprint
from main.environment import ENVIRONMENT
from main.database_client import DatabaseClient
from bson import json_util
import json
import datetime

routes = Blueprint("routes", __name__)

@routes.route('/')
def health_check():
    return "Alive"

@routes.route('/<date>')
def get_summary(date):        
    if not validate_date(date):
        abort(400, 'Selected date is not a valid YYYY-MM-DD formatted date')

    environment = ENVIRONMENT()
    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')


    database_client = DatabaseClient(mongodb_connstring, mongodb_name)

    if not database_client.is_connected():
        abort(500, 'Failed to connect to the database')
    
    news_collection = database_client.get_news_collection()

    news_articles = list(news_collection.find({ 'fetch_date': date }))

    stock_summary_collection = database_client.get_stock_summary_collection()

    stock_summary = stock_summary_collection.find_one({ 'date': date })

    if len(news_articles) == 0 or stock_summary == None:
        abort(404, "Selected date has not been imported and analyzed")

    daily_summary = {
        'stocks': stock_summary,
        'articles': news_articles
    }
    return json.loads(json_util.dumps(daily_summary))

def validate_date(date):
    try:
        parsed_date = datetime.date.fromisoformat(date)
    except ValueError:
        return False
    return True