from author import Author
from schema import AuthorSchema

author = Author("1", "Alex", "alex@mail.ru")
schema = AuthorSchema()
result = schema.dump(author)
print(result)
