from api import api, app
from api.resources.quote import QuoteResource, QuoteListResource
from api.resources.author import AuthorResource, AuthorListResource
from api.resources.user import UserResource
from config import Config

api.add_resource(QuoteResource,
                 '/authors/<int:author_id>/quotes/<int:quote_id>')  # <-- requests
api.add_resource(QuoteListResource,
                 '/authors/<int:author_id>/quotes',
                 '/quotes')  # <-- requests
api.add_resource(AuthorResource,
                 '/authors/<int:author_id>')  # <-- requests
api.add_resource(AuthorListResource,
                 '/authors')  # <-- requests
api.add_resource(UserResource,
                 '/users/<int:user_id>',
                 '/users')  # <-- requests


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
