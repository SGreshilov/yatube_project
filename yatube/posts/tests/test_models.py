from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Post, Group


User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )


    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        group = PostModelTest.group
        post = PostModelTest.post
        field_object_name = {
            'Тестовая группа': group.title,
            'Тестовый пост': post.text
        }
        for expected_value, field in field_object_name.items():
            with self.subTest(field=field):
                self.assertEqual(str(field), expected_value)