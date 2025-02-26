from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from ..models import Post


User = get_user_model()


class PostFormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            text='Тест',
            author=cls.user
        )
        cls.post_edit = Post.objects.create(
            text='Текст до редактирования',
            author=cls.user
        )
        cls.post_id = cls.post_edit.pk

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormsTests.user)

    def test_create_post_form(self):
        post_cnt = Post.objects.count()
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            {
                'text': 'Тест2',
                'author': PostFormsTests.user
            },
            follow=True
        )
        self.assertEqual(post_cnt + 1, Post.objects.count())
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': 'auth'})
        )
        self.assertTrue(
            Post.objects.filter(
                text='Тест2',
                author=PostFormsTests.user
            )
        )

    def test_edit_post_form(self):
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': PostFormsTests.post_id}),
            {'text': 'Текст после редактирования'}
        )
        text_post = Post.objects.get(pk=PostFormsTests.post_id).text
        self.assertEqual(text_post, 'Текст после редактирования')
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': PostFormsTests.post_id})
        )