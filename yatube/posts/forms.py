from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    """Форма создания поста"""

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

class CommentForm(ModelForm):
    """Форма создания комментария"""

    class Meta:
        model = Comment
        fields = ('text',)