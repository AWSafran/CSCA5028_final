from environment import ENVIRONMENT
from database_client import DatabaseClient
from stock_db_service import StockDbService
from stock_summary_db_service import StockSummaryDatabaseService
from stock_helper  import calculate_deltas, get_nominal_delta_min_max, get_percent_delta_min_max

TEST_FETCH_DATE = '2026-03-26'
ORIGINAL_SUMMARY_T_VAL = 'ORIGINAL_FROM_TEST_DATE'
WRONG_DATE_T_VAL = 'WRONG_DATE_T_VAL'
WRONG_DATE_SUMMARY_DATE = '2026-03-01'
NEW_SUMMARY_T_VAL = 'NEW_SUMMARY_T_VAL'

MOCK_STOCKS = [
    {
        #Highest delta_pct
        'o': 1,
        'c': 2,
        'T': 'TEST1',
        'fetch_date': TEST_FETCH_DATE
    },
    {
        #highest delta
        'o': 100,
        'c': 150,
        'T': 'TEST2',
        'fetch_date': TEST_FETCH_DATE
    },
    {
        #delta and delta_pct = 0
        'o': 100,
        'c': 100,
        'T': 'TEST3',
        'fetch_date': TEST_FETCH_DATE
    },
    {

        'o': 100,
        'c': 75,
        'T': 'TEST4',
        'fetch_date': TEST_FETCH_DATE
    },
    {
        #lowest delta_pct
        'o': 4,
        'c': 1,
        'T': 'TEST5',
        'fetch_date': TEST_FETCH_DATE
    },
    {
        #lowest delta
        'o': 100,
        'c': 26,
        'T': 'TEST6',
        'fetch_date': TEST_FETCH_DATE
    },
    {
        'o': 0,
        'c': 2,
        'T': 'OPENZERO',
        'fetch_date': TEST_FETCH_DATE
    },
    {
        'o': 10,
        'c': 12,
        'T': 'BADDATE',
        'fetch_date': '2026-03-25'
    },
]

MOCK_STOCK_SUMMARIES = [
    {
        'date': TEST_FETCH_DATE,
        'nominal_min': [
            {
                'T': ORIGINAL_SUMMARY_T_VAL
            }
        ],
        'nominal_max': [
            {
                'T': ORIGINAL_SUMMARY_T_VAL
            }
        ],
        'percent_min': [
            {
                'T': ORIGINAL_SUMMARY_T_VAL
            }
        ],
        'percent_max': [
            {
                'T': ORIGINAL_SUMMARY_T_VAL
            }
        ]
    },
    {
        'date': WRONG_DATE_SUMMARY_DATE,
        'nominal_min': [
            {
                'T': WRONG_DATE_T_VAL
            }
        ],
        'nominal_max': [
            {
                'T': WRONG_DATE_T_VAL
            }
        ],
        'percent_min': [
            {
                'T': WRONG_DATE_T_VAL
            }
        ],
        'percent_max': [
            {
                'T': WRONG_DATE_T_VAL
            }
        ]
    }    
]


def seed_test_db_stocks():
    environment = ENVIRONMENT()

    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')

    database_client = DatabaseClient(mongodb_connstring, mongodb_name, is_test=True)

    assert database_client.is_connected() == True

    stock_collection = database_client.get_stock_collection()

    #Clear collection and insert only our current test data
    stock_collection.delete_many({})

    stock_collection.insert_many(MOCK_STOCKS)

    return stock_collection
    
def seed_test_db_summary():
    environment = ENVIRONMENT()

    mongodb_connstring = environment.get('mongodb_connstring')
    mongodb_name = environment.get('mongodb_name')

    database_client = DatabaseClient(mongodb_connstring, mongodb_name, is_test=True)

    assert database_client.is_connected() == True

    stock_summary_collection = database_client.get_stock_summary_collection()

    stock_summary_collection.delete_many({})

    stock_summary_collection.insert_many(MOCK_STOCK_SUMMARIES)

    return stock_summary_collection

def test_retrieve_stocks():
    stock_collection = seed_test_db_stocks()

    stock_db_service = StockDbService(stock_collection)

    stocks = stock_db_service.get_daily_stocks(TEST_FETCH_DATE)

    assert len(list(stocks)) == 6

def test_calculate_deltas():
    nonzero_mocks = [stock for stock in MOCK_STOCKS if stock['o'] != 0]
    mocks_with_deltas = calculate_deltas(nonzero_mocks)

    test1 = mocks_with_deltas[0]
    test2 = mocks_with_deltas[1]
    test3 = mocks_with_deltas[2]
    test4 = mocks_with_deltas[3]
    test5 = mocks_with_deltas[4]
    test6 = mocks_with_deltas[5]

    assert test1['delta'] == 1
    assert test2['delta'] == 50
    assert test3['delta'] == 0
    assert test4['delta'] == -25
    assert test5['delta'] == -3
    assert test6['delta'] == -74

    assert test1['delta_pct'] == 1
    assert test2['delta_pct'] == 0.5
    assert test3['delta_pct'] == 0
    assert test4['delta_pct'] == -0.25
    assert test5['delta_pct'] == -0.75
    assert test6['delta_pct'] == -0.74

def test_get_nominal_deltas_min_max():
    nonzero_mocks = [stock for stock in MOCK_STOCKS if stock['o'] != 0]
    mocks_with_deltas = calculate_deltas(nonzero_mocks)

    nominal_min, nominal_max = get_nominal_delta_min_max(mocks_with_deltas)

    assert nominal_min[0]['T'] == 'TEST6'
    assert nominal_max[0]['T'] == 'TEST2'

def test_get_percent_delta_min_max():
    nonzero_mocks = [stock for stock in MOCK_STOCKS if stock['o'] != 0]
    mocks_with_deltas = calculate_deltas(nonzero_mocks)

    percent_min, percent_max = get_percent_delta_min_max(mocks_with_deltas)
    assert percent_min[0]['T'] == 'TEST5'
    assert percent_max[0]['T'] == 'TEST1'

def test_stock_summary_insert():
    stock_summary_collection = seed_test_db_summary()

    stock_summary_db_service = StockSummaryDatabaseService(stock_summary_collection)

    new_stock_summary = {
        'date': TEST_FETCH_DATE,
        'nominal_min': [
            {
                'T': NEW_SUMMARY_T_VAL
            }
        ],
        'nominal_max': [
            {
                'T': NEW_SUMMARY_T_VAL
            }
        ],
        'percent_min': [
            {
                'T': NEW_SUMMARY_T_VAL
            }
        ],
        'percent_max': [
            {
                'T': NEW_SUMMARY_T_VAL
            }
        ]
    }

    stock_summary_db_service.insert_summary(new_stock_summary)

    #Ensure we didn't delete the summary from a different date
    other_date_summary_count = stock_summary_collection.count_documents({'date': WRONG_DATE_SUMMARY_DATE})

    assert other_date_summary_count == 1

    #Ensure we replaced the old summary with the new one
    test_date_summary = stock_summary_collection.find_one({'date': TEST_FETCH_DATE})
    
    assert test_date_summary['nominal_min'][0]['T'] == NEW_SUMMARY_T_VAL


    
