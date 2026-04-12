from flask import abort, Blueprint
from environment import ENVIRONMENT
from database_client import DatabaseClient
from monitoring.logging_service import LoggingService
from bson import json_util
import json
import datetime

routes = Blueprint("routes", __name__)

@routes.route('/')
def health_check():
    return "Alive"

@routes.route('/<date>')
def get_summary(date):        

    environment = ENVIRONMENT()
    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')


    database_client = DatabaseClient(mongodb_connstring, mongodb_name)

    if not database_client.is_connected():
        _abort(500, 'Failed to connect to the database')

    logging_service = LoggingService(database_client.get_logging_collection())
    logging_service.log_info(date, 'request recieved')

    try:

        if not validate_date(date):
            logging_service.log_handled_error(date, 'Invalid Date Requested')
            _abort(400, 'Selected date is not a valid YYYY-MM-DD formatted date')
        
        news_collection = database_client.get_news_collection()

        news_articles = list(news_collection.find({ 'fetch_date': date }))

        stock_summary_collection = database_client.get_stock_summary_collection()

        stock_summary = stock_summary_collection.find_one({ 'date': date })

        if len(news_articles) == 0 or stock_summary == None:
            logging_service.log_handled_error(date, 'No Data for Requested Date')
            _abort(404, "Selected date has not been imported and analyzed")

        daily_summary = {
            'stocks': stock_summary,
            'articles': news_articles
        }

        logging_service.log_info(date, 'request fulfilled')
        return json.loads(json_util.dumps(daily_summary))
    except Exception as e:
        logging_service.log_error(date, e)
        _abort(500, 'An Unexpected Error Occurred')

def validate_date(date):
    try:
        parsed_date = datetime.date.fromisoformat(date)
    except ValueError:
        return False
    return True

def _abort(status, message):
    try:
        abort(status, message)
    except:
        None