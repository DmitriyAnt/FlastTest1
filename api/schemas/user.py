from api import ma
from api.models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        # fields = ["id", "username"] # перечисление нужных
        exclude = ["password_hash"] # перечисление не нужных


user_schema = UserSchema()
users_schema = UserSchema(many=True)