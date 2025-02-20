from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.forms.fields import CharField, ChoiceField

from time import sleep
from ..models import Post, Group


User = get_user_model()


class PostPagesTests(TestCase):
    """Тестирование страниц приложения posts"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.user_test = User.objects.create_user(username='test')
        cls.group = Group.objects.create(
            title='Группа 1',
            slug='group1',
            description='описание'
        )
        cls.group_test = Group.objects.create(
            title='группа тест',
            slug='group_test',
            description='test'
        )
        for i in range(1, 14):
            Post.objects.create(
                text=f'текст{i}',
                author=cls.user,
                group=cls.group,
            )
            sleep(0.01)
        cls.post_test = Post.objects.create(
            text='test',
            author=cls.user_test,
            group=cls.group_test
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostPagesTests.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон"""
        pages_names_templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:groups_list', kwargs={'slug': 'group1'}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'auth'}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': 1}): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': 1}): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html'
        }
        for page_name, template in pages_names_templates.items():
            with self.subTest(page_name=page_name):
                response = self.authorized_client.get(page_name)
                self.assertTemplateUsed(response, template)

    def test_pages_with_posts_show_correct_context(self):
        """Шаблоны index, groups_list, profile, post_detail сформированы с правильным контекстом"""
        context_page_name = {
            reverse('posts:index'): 'test',
            reverse('posts:groups_list', kwargs={'slug': 'group1'}): 'текст13',
            reverse('posts:profile', kwargs={'username': 'test'}): 'test'
        }
        for page_name, context in context_page_name.items():
            with self.subTest(page_name=page_name):
                response = self.guest_client.get(page_name)
                text_post = response.context.get('page_obj')[0].text
                self.assertEqual(text_post, context)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом"""
        response = self.guest_client.get(
            reverse('posts:post_detail', kwargs={'post_id': 14})
        )
        post_text = response.context.get('post').text
        self.assertEqual(post_text, 'test')

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        form_context = response.context.get('form')
        form_text = form_context.fields.get('text')
        form_group = form_context.fields.get('group')
        self.assertIsInstance(form_text, CharField)
        self.assertIsInstance(form_group, ChoiceField)

    def test_first_page_paginator(self):
        """Проверка первой страницы пагинатора в шаблонах index, group_list, profile"""
        pages = [
            reverse('posts:index'),
            reverse('posts:groups_list', kwargs={'slug': 'group1'}),
            reverse('posts:profile', kwargs={'username': 'auth'})
        ]
        for page in pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertEqual(len(response.context.get('page_obj')), 10)
