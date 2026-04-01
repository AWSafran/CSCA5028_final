import requests

class StockApiService:
    url = ''
    api_key = ''

    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def fetch_stocks(self, selected_date):
        stocks_response = requests.get(self.build_url(selected_date))
        json_response = stocks_response.json()
        if json_response['status'] == 'OK':
            if json_response['resultsCount'] == 0:
                return []
            return self.set_fetch_date(json_response['results'], selected_date)
        elif json_response['status'] == 'ERROR':
            raise Exception(json_response['error'])
        else:
            raise Exception('An unexpected error occurred while fetching stocks')
        
    def build_url(self, selected_date):
        return f'{self.url}/{selected_date}?apiKey={self.api_key}'
    
    def set_fetch_date(self, stocks, selected_date):
        for stock in stocks:
            stock['fetch_date'] = selected_date
        
        return stocks