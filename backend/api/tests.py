from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from education.models import Lesson, LessonProduct, Product, UserProduct
from users.models import User


class CreateUserTest(APITestCase):
    def test_can_create_user(self):
        """
        Проверяем, что пользователь может зарегистрироваться.
        """
        request_data = {
            "username": "test",
            "email": "test@mail.ru",
            "password": "mysecretpassword",
        }
        response = self.client.post("/api/v1/users/", request_data)
        expected_data = {
            "username": "test",
            "email": "test@mail.ru",
            "id": User.objects.get(username="test").id,
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Запрос возвращает не 201 код",
        )
        self.assertEqual(
            User.objects.all().count(),
            1,
            "Пользователь не создается в базе данных",
        )
        self.assertEqual(
            response.data,
            expected_data,
            "Тело ответа API не соответствует документации",
        )


class CreataTokenTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", username="test")
        self.user_password = "mysecretpassword"
        self.user.set_password(self.user_password)
        self.user.save()
        self.token_count = Token.objects.all().count()

    def test_can_get_token(self):
        """
        Проверяем, что зарегистрированный пользователь может получить токен.
        """
        request_data = {
            "username": self.user.username,
            "password": self.user_password,
        }
        response = self.client.post("/api/v1/auth/login/", request_data)
        token_count = Token.objects.all().count()
        expected_data = {"auth_token": Token.objects.get(user=self.user).key}
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Ответ API содержит не 200 код",
        )
        self.assertEqual(
            token_count,
            self.token_count + 1,
            "Токен не создается в базе данных",
        )
        self.assertEqual(
            response.data,
            expected_data,
            "Тело ответа API не соответствует документации",
        )


class DestroyTokenTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", username="test")
        self.user.set_password("mysecretpassword")
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.token_count = Token.objects.all().count()
        self.client = APIClient()

    def test_auth_can_destroy_token(self):
        """
        Проверяем, что аутентифицированный пользователь
        может уничтожить свой токен.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post("/api/v1/auth/logout/")
        token_count = Token.objects.all().count()
        expected_data = None
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            "Ответ API содержит не 204 код",
        )
        self.assertEqual(
            token_count,
            self.token_count - 1,
            "Токен не удаляется из базы данных",
        )
        self.assertEqual(
            response.data,
            expected_data,
            "Тело ответа API не соответствует документации",
        )

    def test_noauth_cant_destroy_token(self):
        """
        Проверяем, что неаутентифицированный
        пользователь не может уничтожить токен.
        """
        response = self.client.post("/api/v1/auth/logout/")
        token_count = Token.objects.all().count()
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "Ответ API содержит не 401 код",
        )
        self.assertEqual(
            token_count,
            self.token_count,
            "Токен всё равно удалился из базы данных",
        )
        self.assertEqual(
            {"detail": "Учетные данные не были предоставлены."},
            response.data,
            "Тело ответа API не соответствует документации",
        )


class AllProductsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", username="test")
        self.user.set_password("mysecretpassword")
        self.user.save()
        self.product = Product.objects.create(name="SQL", owner=self.user)
        self.lessons = Lesson.objects.bulk_create(
            [
                Lesson(
                    name=f"LESSON {i}",
                    link_to_video="https://youtu.be/qwerty",
                    viewing_duration=i + 1234,
                )
                for i in range(2)
            ]
        )
        self.lessons_products = LessonProduct.objects.bulk_create(
            [
                LessonProduct(lesson=lesson, product=self.product)
                for lesson in self.lessons
            ]
        )
        self.user_product = UserProduct.objects.create(
            user=self.user, product=self.product
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_auth_can_get_his_products(self):
        """
        Проверяем, что аутентифицированный пользователь
        может уничтожить свой токен.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/v1/users/me/products/")
        expected_data = [
            {
                "id": self.product.id,
                "product_name": self.product.name,
                "owner": self.product.owner.username,
                "lessons": [
                    {
                        "lesson_name": self.lessons[0].name,
                        "link_to_video": "https://youtu.be/qwerty",
                        "viewing_duration": str(
                            self.lessons[0].viewing_duration
                        ),
                        "viewed": False,
                        "viewing_time": 0,
                    },
                    {
                        "lesson_name": self.lessons[1].name,
                        "link_to_video": "https://youtu.be/qwerty",
                        "viewing_duration": str(
                            self.lessons[1].viewing_duration
                        ),
                        "viewed": False,
                        "viewing_time": 0,
                    },
                ],
            }
        ]
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Ответ API содержит не 200 код",
        )
        self.assertEqual(
            response.data.get("results"),
            expected_data,
            "Тело ответа API не соответствует документации",
        )

    def test_noauth_cant_get_his_products(self):
        """
        Проверяем, что неаутентифицированный
        пользователь не может посмотреть свои продукты.
        """
        response = self.client.get("/api/v1/users/me/products/")
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "Ответ API содержит не 401 код",
        )
        self.assertEqual(
            {"detail": "Учетные данные не были предоставлены."},
            response.data,
            "Тело ответа API не соответствует документации",
        )


class ConcreteProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru", username="test")
        self.user.set_password("mysecretpassword")
        self.user.save()
        self.product = Product.objects.create(name="SQL", owner=self.user)
        self.lessons = Lesson.objects.bulk_create(
            [
                Lesson(
                    name=f"LESSON {i}",
                    link_to_video="https://youtu.be/qwerty",
                    viewing_duration=i + 1234,
                )
                for i in range(2)
            ]
        )
        self.lessons_products = LessonProduct.objects.bulk_create(
            [
                LessonProduct(lesson=lesson, product=self.product)
                for lesson in self.lessons
            ]
        )
        self.user_product = UserProduct.objects.create(
            user=self.user, product=self.product
        )
        self.user_lessons = self.user.user_lessons.all()
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_auth_can_get_his_concrete_products(self):
        """
        Проверяем, что аутентифицированный пользователь
        может уничтожить свой токен.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/v1/users/me/products/1/")
        expected_data = {
            "id": self.product.id,
            "product_name": self.product.name,
            "owner": self.product.owner.username,
            "lessons": [
                {
                    "lesson_name": self.lessons[0].name,
                    "link_to_video": "https://youtu.be/qwerty",
                    "viewing_duration": str(self.lessons[0].viewing_duration),
                    "viewed": False,
                    "viewing_time": 0,
                    "date_of_last_viewing": self.user_lessons[
                        0
                    ].date_of_last_viewing,
                },
                {
                    "lesson_name": self.lessons[1].name,
                    "link_to_video": "https://youtu.be/qwerty",
                    "viewing_duration": str(self.lessons[1].viewing_duration),
                    "viewed": False,
                    "viewing_time": 0,
                    "date_of_last_viewing": self.user_lessons[
                        1
                    ].date_of_last_viewing,
                },
            ],
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Ответ API содержит не 200 код",
        )
        self.assertEqual(
            response.data,
            expected_data,
            "Тело ответа API не соответствует документации",
        )

    def test_noauth_cant_get_his_concrete_products(self):
        """
        Проверяем, что неаутентифицированный
        пользователь не может посмотреть свои продукты.
        """
        response = self.client.get("/api/v1/users/me/products/1/")
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "Ответ API содержит не 401 код",
        )
        self.assertEqual(
            {"detail": "Учетные данные не были предоставлены."},
            response.data,
            "Тело ответа API не соответствует документации",
        )


class StatProductAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@mail.ru", username="test", is_staff=True
        )
        self.user.set_password("mysecretpassword")
        self.user.save()
        self.product = Product.objects.create(name="SQL", owner=self.user)
        self.lessons = Lesson.objects.bulk_create(
            [
                Lesson(
                    name=f"LESSON {i}",
                    link_to_video="https://youtu.be/qwerty",
                    viewing_duration=i + 1234,
                )
                for i in range(2)
            ]
        )
        self.lessons_products = LessonProduct.objects.bulk_create(
            [
                LessonProduct(lesson=lesson, product=self.product)
                for lesson in self.lessons
            ]
        )
        self.user_product = UserProduct.objects.create(
            user=self.user, product=self.product
        )
        self.user_lessons = self.user.user_lessons.all()
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_admin_can_get_products_stats(self):
        """
        Проверяем, что администратор
        может посмотреть статистику продуктов.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/v1/products/")
        expected_data = [
            {
                "id": self.product.id,
                "product_name": self.product.name,
                "owner": self.product.owner.username,
                "lessons_watched_count": 0,
                "amount_of_time_watched": sum(
                    list(map(lambda x: x.viewing_time, self.user_lessons))
                ),
                "amount_of_students": 1,
                "product_purchase_percentage": "100.0%",
            }
        ]
        print(expected_data)
        print(response.data.get("results"))
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            "Ответ API содержит не 200 код",
        )
        self.assertEqual(
            response.data.get("results"),
            expected_data,
            "Тело ответа API не соответствует документации",
        )

    def test_noadmin_cant_get_products_stats(self):
        """четные данные не были предоставлены
        Проверяем, что неаутентифицированный
        пользователь не может посмотреть свои продукты.
        """
        user = User.objects.create(
            email="test2@mail.ru", username="test2", is_staff=False
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get("/api/v1/products/")
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            "Ответ API содержит не 403 код",
        )
        self.assertEqual(
            {
                "detail": "У вас недостаточно прав "
                "для выполнения данного действия."
            },
            response.data,
            "Тело ответа API не соответствует документации",
        )
