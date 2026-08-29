from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from journal.models import Article, ArticleTag, Category, Comment, Reaction, Subscription, Tag, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (("LearnJournal", {"fields": ("bio",)}),)


class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("author", "body", "is_approved", "parent", "created_at")
    readonly_fields = ("created_at",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "published_at", "view_count")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "body", "author__username")
    date_hierarchy = "published_at"
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author", "coauthors")
    inlines = [ArticleTagInline, CommentInline]
    actions = ["make_published"]

    @admin.action(description="將選取的文章標記為已發佈")
    def make_published(self, request, queryset):
        from django.utils import timezone

        updated = queryset.update(status=Article.Status.PUBLISHED, published_at=timezone.now())
        self.message_user(request, f"{updated} 篇文章已發佈。")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("article", "author", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    list_editable = ("is_approved",)
    search_fields = ("body", "author__username")


admin.site.register(Reaction)
admin.site.register(Subscription)
