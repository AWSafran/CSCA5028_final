from environment import ENVIRONMENT
from database_client import DatabaseClient
from stock_db_service import StockDbService
from stock_summary_db_service import StockSummaryDatabaseService
import sys
from datetime import date, timedelta
from stock_helper  import calculate_deltas, get_nominal_delta_min_max, get_percent_delta_min_max


def main(analysis_date_string):
    # Load ENV variables
    environment = ENVIRONMENT()

    #Connect to Database

    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')

    database_client = DatabaseClient(mongodb_connstring, mongodb_name)

    if database_client.is_connected():
        print('Successfully connected to database')


    #Retrieve stocks for the day

    stock_db_service = StockDbService(database_client.get_stock_collection())
    daily_stocks = stock_db_service.get_daily_stocks(analysis_date_string)

    #Calculate daily summary
    deltas = calculate_deltas(list(daily_stocks))

    nominal_min, nominal_max = get_nominal_delta_min_max(deltas)

    percent_min, percent_max = get_percent_delta_min_max(deltas)

    stock_summary = {
        'date': analysis_date_string,
        'nominal_min': nominal_min,
        'nominal_max': nominal_max,
        'percent_min': percent_min,
        'percent_max': percent_max
    }

    stock_summary_db_service = StockSummaryDatabaseService(database_client.get_stock_summary_collection())

    stock_summary_db_service.insert_summary(stock_summary)

    stock_db_service.purge_daily_stocks(analysis_date_string)

    #Close db client connection
    database_client.close_client()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        date_string = sys.argv[1]
    else:
        today = date.today()
        collection_date = today - timedelta(days = 2)
        date_string = collection_date.isoformat()
    main(date_string)