# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Resource, Api
from models import db, Earthquake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api=Api(app=app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
class EarthquakeResource(Resource):
    def get(self, id):
        
        earthquake = Earthquake.query.get(id)
        if earthquake:
            return earthquake.to_dict(), 200
        else:
            return {"message": f'Earthquake {id} not found.'}, 404
        
class EarthquakemagResource(Resource):
    def get(self, magnitude):                      
        earthquakes = Earthquake.query.filter(Earthquake.magnitude > magnitude).all()
        #maybe len of earthquake?
        count = len(earthquakes)
        body = {
                "count": count,
                "quakes": [{
                "id": earthquake.id,
                "location": earthquake.location,
                "magnitude": earthquake.magnitude,
                "year": earthquake.year
                } for earthquake in earthquakes]
                }
        return body, 200
        


api.add_resource(EarthquakemagResource, "/earthquakes/magnitude/<float:magnitude>")
api.add_resource(EarthquakeResource, "/earthquakes/<id>")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
