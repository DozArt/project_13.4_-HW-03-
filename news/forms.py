from django import forms
from .models import Post


class PostForms(forms.ModelForm):
    header = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'header',
            'text',
            'category',
            'author',
        ]

    # def clean(self):
    #     cleaned_data = super().clean()
    #     header = cleaned_data.get("header")
    #     if header is not None and len(header) < 20:
    #         raise ValidationError({
    #             "header": "Заголовок не может быть менее 20 символов."
    #         })
    #
    #     return cleaned_data
