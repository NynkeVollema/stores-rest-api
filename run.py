from app import app
from db import db

db.init_app(app)

@app.before_first_request       # decorator from Flask itself, so not from one of the extensions
def create_tables():
    db.create_all()     # creates only the tables that it sees (through the imports)
