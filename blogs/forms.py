from django import forms


class BlogUserForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class CommentForm(forms.Form):
    comment_content = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Input comment...',
        'rows': 3
    }))
