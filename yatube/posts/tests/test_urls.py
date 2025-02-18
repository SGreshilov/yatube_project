from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group


User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """Добавление тестовых записей в БЖ"""
        super().setUpClass()
        user = User.objects.create_user(username='auth')
        Group.objects.create(
            title='тестовое название',
            slug='test-test',
            description='тестовое описание'
        )
        Post.objects.create(
            text='Тестовый текст',
            author=user
        )

    def setUp(self):
        """Создание авторизованного и неавторизованного пользователей"""
        self.guest_client = Client()
        self.user = User.objects.get(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_code_post_pages(self):
        """Страницы /group/test-test/, '/', /profile/auth/, /posts/1/ доступны всем"""
        templates_url_names = {
            '/group/test-test/': 'posts/group_list.html',
            '/profile/auth/': 'group/profile.html',
            '/posts/2/': 'posts/post_detail.html',
            '/': 'posts/index.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, 200, address)
