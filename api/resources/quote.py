from api import Resource, reqparse, db
from api.models.author import AuthorModel
from api.models.quote import QuoteModel


class QuoteResource(Resource):
    def get(self, author_id, quote_id):
        quote = QuoteModel.query.get(quote_id)
        if quote:
            return quote.to_dict(), 200
        return {"Error": "Quote not found"}, 404

    def put(self, author_id, quote_id):

        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404

        quote = QuoteModel.query.get(quote_id)
        if quote is None:
            return {"Error": f"Quote id={quote_id} not found"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        quote_data = parser.parse_args()
        quote = QuoteModel(author, quote_data["text"])
        db.session.add(quote)
        db.session.commit()

        return quote.to_dict(), 200

    def delete(self, author_id, quote_id):
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404

        quote = QuoteModel.query.get(quote_id)
        if quote is None:
            return {"Error": f"Quote id={quote_id} not found"}, 404

        db.session.delete(quote)
        db.session.commit()
        return f"Quote {quote.id} deleted.", 200


class QuoteListResource(Resource):
    def get(self, author_id=None):
        if author_id is None:
            quotes = QuoteModel.query.all()
            if quotes is None:
                return {"Error": f"Quotes not found"}, 404
            return [quote.to_dict() for quote in quotes]

        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404

        quotes = author.quotes.all()
        if quotes is None:
            return {"Error": f"Quotes not found"}, 404
        return [quote.to_dict() for quote in quotes], 200  # Возвращаем все цитаты автора

    def post(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        quote_data = parser.parse_args()

        print(f"{quote_data=}")

        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404

        quote = QuoteModel(author, quote_data["text"])
        db.session.add(quote)
        db.session.commit()
        return quote.to_dict(), 201


