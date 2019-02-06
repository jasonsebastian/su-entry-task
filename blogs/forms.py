from django import forms


class BlogUserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class CommentForm(forms.Form):
    comment_content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Input comment...',
        'rows': 3
    }))


class CreateEditPostForm(forms.Form):
    post_title = forms.CharField(max_length=20)
    post_content = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5
    }))
