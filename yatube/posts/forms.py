from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    """Форма создания поста"""

    class Meta:
        model = Post
        fields = ('text', 'group')
