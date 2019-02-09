from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Post


class BlogUserLoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class CommentForm(forms.Form):
    comment_content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Input comment...',
        'rows': 3
    }))


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title', 'post_content']
        widgets = {
            'post_content': forms.Textarea(attrs={
                'rows': 5
            })
        }


class EditPostForm(forms.Form):
    post_title = forms.CharField(max_length=30)
    post_content = forms.CharField(max_length=2500,
                                   widget=forms.Textarea(attrs={'rows': 5}))


class BlogUserCreationForm(forms.Form):
    first_name = forms.CharField(max_length=20,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    matric_no = forms.CharField(min_length=9, max_length=9)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation:
            if password != password_confirmation:
                raise forms.ValidationError(_("Please re-enter your password and password confirmation."))
