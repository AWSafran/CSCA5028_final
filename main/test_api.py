from main import create_app
from bson import json_util

def test_health_check():
    flask_app = create_app()
    flask_app.testing = True

    with flask_app.test_client() as test_client:
        response = test_client.get('/')

        assert response.status_code == 200

def test_get_summary():
    flask_app = create_app()
    flask_app.testing = True

    with flask_app.test_client() as test_client:
        response = test_client.get('/2026-03-24')
        assert response.status_code == 200

        response_summary = json_util.loads(response.data)
        
        articles = response_summary['articles']

        assert len(articles) == 10

        assert articles[0]['fetch_date'] == '2026-03-24'

def test_invalid_date_handler():
    flask_app = create_app()
    flask_app.testing = True

    with flask_app.test_client() as test_client:
        response = test_client.get('/2026-03-')

        assert response.status_code == 400


def test_date_not_found_handler():
    flask_app = create_app()
    flask_app.testing = True

    with flask_app.test_client() as test_client:
        response = test_client.get('/1900-03-24')

        assert response.status_code == 404