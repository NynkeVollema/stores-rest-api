from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()  # initialises a new object which we can use to parse the request;
                                        # without "self." in front it belongs to the class itself and
                                        # not to one specific item resource
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Every item needs a store id."
                        )

    @jwt_required()  # authentication is required before we can call the get method
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "Item cannot be found."}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()  # only the data defined in add_argument is passed through

        item = ItemModel(name, **data)  # simplified version of next line
        # item = ItemModel(name, data["price"], data["store_id"])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500    # 500 = internal server error

        return item.json(), 201  # 201 = html status code for "created"

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item has been deleted."}

    def put(self, name):
        data = Item.parser.parse_args()  # only the data defined in add_argument is passed through

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)  # simplified version of next line
            # item = ItemModel(name, data["price"], data["store_id"])
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
        # alternative without using list comprehension, mainly useful for other programming languages:
        # return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}
