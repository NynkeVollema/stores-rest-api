import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    # Disable flask SQLAlchemy tracker, because SQLAlchemy
                                                        # itself, the main library, has its own tracker which
                                                        # is a bit better.
app.secret_key = "Reus"
api = Api(app)

jwt = JWT(app, authenticate, identity)
# JWT creates a new endpoint, /auth
# When we call /auth, we send it a username and a password
# JWT sends these to the authenticate function
# authenticate function checks whether password is correct en returns the correct User object
# /auth endpoint returns a JWT token
# JWT token doesn't do anything, but we can send it to the next request we make
# JWT then calls the identity function

api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)      # debug gives nice error messages if something goes wrong
