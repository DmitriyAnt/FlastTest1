import json
from api import db
from app import app
from unittest import TestCase
from api.models.user import UserModel
from config import Config


class TestUsers(TestCase):
    def setUp(self):
        """
        Данный метод запускается перед КАЖДЫМ тестом
        """
        self.app = app
        # Клиент для отправки запросов
        self.client = self.app.test_client()
        self.app.config.update({
            'SQLALCHEMY_DATABASE_URI': Config.TEST_DATABASE_URI
        })

        with self.app.app_context():
            # Создаем таблицы в БД
            db.create_all()

    def test_user_not_found(self):
        response = self.client.get('/users/2')
        self.assertEqual(response.status_code, 404)

    # def test_user_get_by_id(self):
    #     user_data = {
    #         "username": 'user',
    #         'password': 'user'
    #     }
    #     user = UserModel(**user_data)
    #     user.save()
    #     user_id = user.id
    #     response = self.client.get(f'/users/{user_id}')
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["username"], user_data["username"])

    def test_users_get(self):
        """
        Тест на получения списка пользователей
        """
        users_data = [
            {
                "username": 'admin',
                'password': 'admin'
            },
            {
                "username": 'ivan',
                'password': '1234'
            },
        ]
        for user_data in users_data:
            user = UserModel(**user_data)
            db.session.add(user)
        db.session.commit()

        response = self.client.get("/users")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(users_data[0]["username"], data[0]["username"])
        self.assertEqual(users_data[1]["username"], data[1]["username"])
        self.assertNotIn("password", data[0])


    def test_user_creation(self):
        """
        Тест на создание нового пользователя
        """
        user_data = {
            "username": 'admin',
            'password': 'admin'
        }
        ...

    def tearDown(self):
        """
        Данный метод запускается после КАЖДОГО теста
        """
        with self.app.app_context():
            # Удаляем все таблицы в БД
            db.session.remove()
            db.drop_all()
