from api import Resource, reqparse, db
from api.models.author import AuthorModel
from api.models.quote import QuoteModel


#
class AuthorResource(Resource):
    def get(self, author_id):
        author = AuthorModel.query.get(author_id)
        if author is None:
            return f"Author id={author_id} not found", 404

        return author.to_dict(), 200


    def put(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        author_data = parser.parse_args()
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404
        author.name = author_data["name"]
        db.session.commit()
        return author.to_dict(), 200

    def delete(self, author_id):
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404

        # quotes = quotes.filter(QuoteModel.author.has(name=params.get('author')))
        quote = QuoteModel.query.filter(QuoteModel.author.has(name=author.name)).all()
        if quote:
            db.session.delete(quote)  # delete all not work yet

        db.session.delete(author)
        db.session.commit()

        return f"Author {quote.id} deleted with quotes.", 200


class AuthorListResource(Resource):
    def get(self):
        authors = AuthorModel.query.all()
        authors_list = [author.to_dict() for author in authors]
        return authors_list, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        author_data = parser.parse_args()
        author = AuthorModel(author_data["name"])
        db.session.add(author)
        db.session.commit()
        return author.to_dict(), 201
