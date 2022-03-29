import json

from marshmallow import ValidationError

from author import Author
from schema import AuthorSchema

json_data = """
{
   "id": 2,
   "name": "Ivan",
   "email": "ivan@mail.ru"
}
"""

schema = AuthorSchema()
try:
    result = schema.loads(json_data)
    author = Author(**result)
    print(result)
    print(author)
except ValidationError as err:
    print(err.messages)

json_data_list = """
[
   {
       "id": 1,
       "name": "Alex",
       "email": "alex@mail.ru"
   },
   {
       "id": 2,
       "name": "Ivan",
       "email": "ivan@mail.ru"
   },
   {
       "id": 4,
       "name": "Tom",
       "email": "tom@mail.ru"
   }
]
"""


try:
    result = AuthorSchema(many=True).loads(json_data_list)
    # author = Author(**result)
    print(result)
except ValidationError as err:
    print(err.messages)
