from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # lazy="dynamic" means that the item list is not (yet) retrieved from the database if the store
    #   is created. Otherwise, the script would make an object for each item in the database, which
    #   can be quite expensive when a lot of items are present.
    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json(self):
        # self.items = query builder because lazy is set to "dynamic"
        # .all() is needed to look into the table and retrieve a list of items
        # this means that the json method is slower (but creating a store is faster)
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()     # SQL: SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)    # inserts or, if it already exists, updates the object "self"
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
