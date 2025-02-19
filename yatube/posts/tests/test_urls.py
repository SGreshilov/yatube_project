from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Post, Group


User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """Добавление тестовых записей в БЖ"""
        super().setUpClass()
        cls.user = User.objects.create_user(username='test')
        Group.objects.create(
            title='тестовое название',
            slug='test-test',
            description='тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст'
        )
        cls.post_id = cls.post.pk

    def setUp(self):
        """Создание авторизованного и неавторизованного пользователей"""
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTests.user)

    def test_urls_uses_correct_template(self):
        """URL-адреса используют соответствующий шаблон"""
        post_id = PostURLTests.post_id
        templates_url_names = {
            '/group/test-test/': 'posts/group_list.html',
            '/profile/test/': 'posts/profile.html',
            f'/posts/{post_id}/': 'posts/post_detail.html',
            '/': 'posts/index.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{post_id}/edit/': 'posts/create_post.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_post_create_redirect_anon(self):
        """Проверка доступности страницы создания поста неавторизованному пользователю"""
        response = self.guest_client.get('/create/')
        self.assertRedirects(response, '/auth/login/?next=/create/')

    def test_post_edit_redirect_no_author(self):
        """Проверка доступности страницы редактирования поста не для автора"""
        post_id = PostURLTests.post_id
        user = User.objects.create_user(username='noauthor')
        client = Client()
        client.force_login(user)
        response = client.get(f'/posts/{post_id}/edit/')
        self.assertRedirects(response, f'/posts/{post_id}/')

    def test_unexisting_page(self):
        """Проверка на получение ошибки 404 при запросе на несуществующую страницу"""
        response = self.client.get('poz/asdz/')
        self.assertEqual(response.status_code, 404)