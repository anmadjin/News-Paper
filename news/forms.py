from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = ['author', 'category', 'title', 'text']

   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['author'].label_from_instance = lambda obj: obj.user.username
       self.fields['category'].label_from_instance = lambda obj: obj.name

class PostForm2(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'title', 'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Текст не должен быть идентичным заголовку."
            )

        return cleaned_data