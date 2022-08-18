from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    # show readonly(editable=False) fields on admin panel. By default, it is hidden.
    readonly_fields = ('created_date',)


class CommentAdmin(admin.ModelAdmin):
    # show readonly(editable=False) fields on admin panel. By default, it is hidden.
    readonly_fields = ('created_date',)


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)


