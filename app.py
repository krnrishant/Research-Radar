from flask import Flask, request
from flask_restful import Resource, Api
import requests
from requests.exceptions import RequestException
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column 

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<your-user>:<your-password>@localhost:5432/ResearchRadar'
api = Api(app)
db.init_app(app)

class PaperModel(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    openalex_id: Mapped[str] = mapped_column(String(100), unique = True, nullable = False)
    title: Mapped[str] = mapped_column(Text, nullable =False)
    authors: Mapped[list] = mapped_column(JSON, nullable =False)
    year: Mapped[int | None] = mapped_column(nullable =True)
    cited_by_count: Mapped[int] = mapped_column(default=0)

    def storage(self, openalex_id, authors, title, year, cited_by_count):
        self.openalex_id = openalex_id
        self.authors = authors
        self.title = title
        self.year = year
        self.cited_by_count = cited_by_count

        db.session.add(self)
        # db.session.commit()

class Paper(Resource):
    def get(self):
        url = 'https://api.openalex.org/works';

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
            'openalex_id': paper['id'],
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

        for result in results:
            paper_info = PaperModel()

            paper_info.storage(openalex_id = result['openalex_id'],
                        title = result['title'],
                        authors = result['authors'],
                        year = result['year'],
                        cited_by_count=result['cited_by_count'])
        #     db.session.add(paper_info)
        db.session.commit()


        return {
            'results':results
        }, 200

    


api.add_resource(Paper, '/api/v1/papers')

with app.app_context():
    db.create_all()

# with app.app_context():
#     db.create_all()

#     test_paper = PaperModel(
#         openalex_id="https://openalex.org/W123456789",
#         title="Test Research Paper",
#         authors=["Author One", "Author Two"],
#         year=2024,
#         cited_by_count=10
#     )

#     db.session.add(test_paper)
#     db.session.commit()

#     print("Paper saved:", test_paper.id)

if __name__ == '__main__':
    app.run(debug=True)
