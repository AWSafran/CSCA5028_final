import requests

class NewsApiService:
    url = ''
    api_key = ''

    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def fetch_articles(self, selected_date):
        params = self.get_params(selected_date)
        articles_response = requests.get(self.url, params=params)
        json_response = articles_response.json()
        if json_response['status'] == 'ok':
            return self.set_fetch_date(json_response['articles'], selected_date)
        elif json_response['status'] == 'error':
            raise Exception(json_response['message'])
        else:
            raise Exception('An unexpected error occurred while fetching news articles')

    def get_params(self, selected_date):
        return {
            'apiKey': self.api_key,
            'sortBy': 'popularity',
            'from': selected_date,
            'language': 'en',
            'pageSize': 10,
            'page': 1,
            'domains': 'abcnews.go.com,us.cnn.com,cbsnews.com,politico.com,wsj.com,time.com,usatoday.com,apnews.com,reuters.com'
        }
    
    def set_fetch_date(self, articles, selected_date):
        for article in articles:
            article['fetch_date'] = selected_date
        return articles

        


