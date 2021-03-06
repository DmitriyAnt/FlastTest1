from api import Resource, reqparse, db, auth
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.schemas.author import author_schema, authors_schema


class AuthorResource(Resource):
    def get(self, author_id):
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": "Author id={author_id} not found"}, 404

        return author_schema.dump(author), 200

    @auth.login_required
    def put(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("surname")
        author_data = parser.parse_args()
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404

        for key, value in author_data.items():
            setattr(author, key, value)

        db.session.commit()
        return author_schema.dump(author), 200

    @auth.login_required
    def delete(self, author_id):
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404

        quotes = QuoteModel.query.filter(QuoteModel.author.has(name=author.name)).all()
        for quote in quotes:
            db.session.delete(quote)

        db.session.delete(author)
        db.session.commit()

        return {"Error": "Author {author_id} deleted with quotes."}, 200


class AuthorListResource(Resource):
    def get(self):
        authors = AuthorModel.query.all()
        # authors_list = [author.to_dict() for author in authors]
        return authors_schema.dump(authors), 200

    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        parser.add_argument("surname", required=True)
        author_data = parser.parse_args()
        author = AuthorModel(author_data["name"], author_data["surname"])
        db.session.add(author)
        db.session.commit()
        return author_schema.dump(author), 201
