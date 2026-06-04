from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

#
# admin.site.register(Author)
# admin.site.register(Category)
# admin.site.register(Post)
# admin.site.register(PostCategory)
# admin.site.register(Comment)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'post_type',
        'time_in',
        'rating',
        'get_categories'
    )

    list_filter = ('post_type', 'category', 'author', 'time_in')

    search_fields = ('title', 'text', 'author__user__username')

    list_per_page = 10

    sortable_by = ('id', 'title', 'time_in', 'rating')

    def get_categories(self, obj):
        return ", ".join([c.name for c in obj.category.all()])

    get_categories.short_description = 'Categories'


admin.site.register(Post, PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subscribers_count', 'posts_count')
    search_fields = ('name',)

    def subscribers_count(self, obj):
        return obj.subscribers.count()

    subscribers_count.short_description = 'Subscribers'

    def posts_count(self, obj):
        return obj.post_set.count()

    posts_count.short_description = 'Posts'


admin.site.register(Category, CategoryAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'rating', 'posts_count')
    search_fields = ('user__username', 'user__email')

    def username(self, obj):
        return obj.user.username

    username.short_description = 'Username'

    def posts_count(self, obj):
        return obj.post_set.count()

    posts_count.short_description = 'Posts'


admin.site.register(Author, AuthorAdmin)