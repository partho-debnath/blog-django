from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 10,
            },
        ),
    )


class CommentModelForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            "name",
            "email",
            "body",
        ]


class SearchForm(forms.Form):
    query = forms.CharField()
