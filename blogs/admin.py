from django.contrib import admin

from .models import BlogUser, Comment, Post


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_id', 'user', 'post', 'timestamp')


admin.site.register(BlogUser)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post)
