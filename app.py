from flask import Flask, request
from flask_restful import Resource, Api
import requests
from requests.exceptions import RequestException
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import insert as pg_insert

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise RuntimeError("DATABASE_URL environment variable is not set")

api = Api(app)
db.init_app(app)

class PaperModel(db.Model):
    # __table__ = 'PaperModel'
    id: Mapped[int] = mapped_column(primary_key = True)
    openalex_id: Mapped[str] = mapped_column(String(100), unique = True, nullable = False)
    title: Mapped[str] = mapped_column(Text, nullable =False)
    authors: Mapped[list] = mapped_column(JSON, nullable =False)
    year: Mapped[int | None] = mapped_column(nullable =True)
    cited_by_count: Mapped[int] = mapped_column(default=0)

class Paper(Resource):
    def get(self):
        url = 'https://api.openalex.org/works';

        payload = {
            'search': request.args.get('search', 'research')
        }
        try:
            r = requests.get(url, params=payload, timeout=15)
        except RequestException as e:
            print("OpenAlex request failed:", repr(e))
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

            stmt = pg_insert(PaperModel).values(openalex_id = result['openalex_id'],
            title = result['title'],
            authors = result['authors'],
            year = result['year'],
            cited_by_count = result['cited_by_count']
                ).on_conflict_do_nothing(
                    index_elements = [PaperModel.openalex_id]
                )
            db.session.execute(stmt)
            
        db.session.commit()


        return {
            'results':results
        }, 200

class PaperList(Resource):
    def get(self):
        search_query = request.args.get('search','')
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        if per_page < 1 or per_page > 100:
            return {'error': 'per_page must be between 1 and 100'}, 400

        dt = db.select(PaperModel)
        if(search_query):
            dt = dt.where(PaperModel.title.ilike(f'%{search_query}%'))

        offset = (page -1) * per_page
        dt = dt.order_by(PaperModel.id)
        dt = dt.offset(offset).limit(per_page)

        papers = db.session.scalars(dt).all()

        return { 
            'page':page,
            'per_page':per_page,
            'result':[
            { 
                'openalex_id': p.openalex_id,
                'title': p.title,
                'year': p.year,
                'cited_by_count': p.cited_by_count,
                'authors': p.authors,
            } for p in papers
            ]
        }, 200

api.add_resource(Paper, '/api/v1/papers')
api.add_resource(PaperList, '/api/v1/saved')
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False)