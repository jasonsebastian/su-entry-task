from django import forms

from .models import Post


class BlogUserLoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class CommentForm(forms.Form):
    comment_content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Input comment...',
        'rows': 3
    }))


class CreateEditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_title', 'post_content']
        widgets = {
            'post_content': forms.Textarea(attrs={
                'rows': 5
            })
        }


class BlogUserCreationForm(forms.Form):
    first_name = forms.CharField(max_length=20,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=20,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    matric_no = forms.CharField(min_length=9, max_length=9)
