from django.views.generic import CreateView
from .forms import CreationForm
from django.urls import reverse_lazy


class SingUp(CreateView):
    """Страница регистрации"""

    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'