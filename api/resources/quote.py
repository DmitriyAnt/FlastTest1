from api import Resource, reqparse, db
from api.models.author import AuthorModel
from api.models.quote import QuoteModel


class QuoteResource(Resource):
    def get(self, author_id, quote_id):
        """
        Обрабатываем GET запросы
        :param author_id: id автора
        :param quote_id: id цитаты
        :return: http-response(json, статус)
        """
        author = AuthorModel.query.get(author_id)
        if quote_id is None:  # Если запрос приходит по url: /authors/<int:author_id>/quotes
            quotes = author.quotes.all()
            return [quote.to_dict() for quote in quotes], 200  # Возвращаем все цитаты автора

        quote = QuoteModel.query.get(quote_id)
        if quote:
            return quote.to_dict(), 200
        return {"Error": "Quote not found"}, 404

    def post(self, author_id):
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        quote_data = parser.parse_args()
        # TODO: раскомментируйте строку ниже, чтобы посмотреть quote_data
        #   print(f"{quote_data=}")
        author = AuthorModel.query.get(author_id)
        if author is None:
            return {"Error": f"Author id={author_id} not found"}, 404

        quote = QuoteModel(author, quote_data["text"])
        db.session.add(quote)
        db.session.commit()
        return quote.to_dict(), 201

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
    def get(self):
        quotes = QuoteModel.query.all()
        return [quote.to_dict() for quote in quotes]  # Возвращаем ВСЕ цитаты


