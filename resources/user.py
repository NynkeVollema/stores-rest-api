from flask_restful import Resource, reqparse

from models.user import UserModel


# The class User Register is going to be a Resource (like Item and ItemList) so we can add it to the API
#   using flask_restful. We could create a flask endpoint to register users instead of creating a Resource.
#   It doesn't really matter which way we do it.
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
            type=str,
            required=True,
            help="This field cannot be left blank!"
    )
    parser.add_argument("password",
            type=str,
            required=True,
            help="This field cannot be left blank!"
    )

    def post(self):
        data = UserRegister.parser.parse_args()


        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists."}, 400

        # user = UserModel(data["username"], data["password"])
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User was created succesfully."}, 201
