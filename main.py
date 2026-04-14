from environment import ENVIRONMENT
from database_client import DatabaseClient
from stock_db_service import StockDbService
from stock_summary_db_service import StockSummaryDatabaseService
from stock_helper  import calculate_deltas, get_nominal_delta_min_max, get_percent_delta_min_max
from monitoring.logging_service import LoggingService

def main(analysis_date_string, is_test = False):
    # Load ENV variables
    environment = ENVIRONMENT()

    #Connect to Database

    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')

    database_client = DatabaseClient(mongodb_connstring, mongodb_name, is_test)

    if database_client.is_connected():
        print('Successfully connected to database')

    #Initialize Logging Service
    logging_service = LoggingService(database_client.get_logging_collection())
    logging_service.log_info(analysis_date_string, 'Beginning Data Analysis')
    #Retrieve stocks for the day

    try:
        stock_db_service = StockDbService(database_client.get_stock_collection())
        daily_stocks = stock_db_service.get_daily_stocks(analysis_date_string)

        #Calculate daily summary
        stocks = list(daily_stocks)

        if len(stocks) == 0:
            logging_service.log_info(analysis_date_string, 'No stocks found for analysis date. Markets may have been closed')

        deltas = calculate_deltas(stocks)

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

        logging_service.log_info(analysis_date_string, 'Analysis completed')

    except Exception as e:
        logging_service.log_error(analysis_date_string, e)

    #Close db client connection
    database_client.close_client()