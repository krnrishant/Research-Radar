from flask import Flask, request
from flask_restful import Resource, Api
import requests
from requests.exceptions import RequestException

app = Flask(__name__)
api = Api(app)

class Paper(Resource):
    def get(self):
        url = 'https://api.openalex.org/works'

        payload = {
            'search': request.args.get('search', 'research')
        }
        try:
            r = requests.get(url, params=payload, timeout=15)
        except RequestException as e:
            return {
                'error': "Failed to connect to api",
                'details': str(e)

            }, 503
        
        if r.status_code != 200:
            return {
                'error': 'External API returned error',
                "status_code": r.status_code
            }, r.status_code

        try:
            data = r.json()
        except Exception as e:
            return {
                'error': str(e)
            },502
        # authors = []
        # for paper in data['results']:

        #     for author in paper['authorships']:
        #         name = author['author']['display_name']
        #         authors.append(name)
        try:
            results = [
        {
            'title': paper['title'],
            'cited_by_count': paper['cited_by_count'],
            'year': paper['publication_year'],
            'authors': [
                author['author']['display_name']
                for author in paper["authorships"]
            ],
        }
            for paper in data['results']
    ]

        except Exception as e:
            return {
                'error': str(e)
            }, 500
        return {
            'results':results
        }, 200

api.add_resource(Paper, '/api/v1/papers')
if __name__ == '__main__':
    app.run(debug=True)