from api import Resource, reqparse, db
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


class UserResource(Resource):
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if user is None:
            return {"Error": f"User id={user_id} not found"}, 404

        return user_schema.dump(user), 200

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        user_data = parser.parse_args()
        user = UserModel.query.get(user_id)
        if user is None:
            return {"Error": f"User id={user_id} not found"}, 404
        user.name = user_data["username"]
        user.surname = user_data["password"]
        db.session.commit()
        return user_schema.dump(user), 200

    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if user is None:
            return {"Error": f"User id={user_id} not found"}, 404

        db.session.delete(user)
        db.session.commit()

        return {"Error": "User {user_id} deleted with quotes."}, 200


class UsersListResource(Resource):
    def get(self):
        user = UserModel.query.all()
        return users_schema.dump(user), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        user_data = parser.parse_args()
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201
