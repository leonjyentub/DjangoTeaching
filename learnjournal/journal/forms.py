from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from journal.models import Article, Comment, Subscription, User


class BootstrapFormMixin:
    def apply_bootstrap(self):
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            if isinstance(field.widget, forms.CheckboxInput):
                css_class = "form-check-input"
            field.widget.attrs.setdefault("class", css_class)


class RegistrationForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label="電子郵件", required=True)

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class ArticleForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Article
        # author and view_count remain server-owned. published_at is exposed here
        # because Deck 03B now implements scheduled publishing end-to-end.
        fields = ("title", "slug", "category", "coauthors", "excerpt", "body", "status", "published_at")
        widgets = {
            "body": forms.Textarea(attrs={"rows": 12, "placeholder": "支援 Markdown"}),
            "excerpt": forms.Textarea(attrs={"rows": 2}),
            "published_at": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["slug"].required = False
        self.fields["published_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        if user is not None:
            self.fields["coauthors"].queryset = User.objects.exclude(pk=user.pk)
            if not user.has_perm("journal.publish_article"):
                self.fields["status"].help_text = "一般作者只能儲存草稿；Editors 群組可以排程與發佈。"
        self.apply_bootstrap()

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get("status")
        published_at = cleaned.get("published_at")

        if status == Article.Status.SCHEDULED and not published_at:
            self.add_error("published_at", "排程文章必須指定發佈時間。")

        if status == Article.Status.PUBLISHED and not published_at:
            # Django 6.1 validates model constraints during ModelForm validation.
            # Supply the same default that Article.save() uses so the
            # published_article_has_timestamp constraint is already true at
            # form-validation time rather than only after save().
            published_at = timezone.now()
            cleaned["published_at"] = published_at

        if status in {Article.Status.SCHEDULED, Article.Status.PUBLISHED}:
            if self.user is None or not self.user.has_perm("journal.publish_article"):
                self.add_error("status", "你沒有排程或發佈文章的權限，請先儲存為草稿。")

        return cleaned


class CommentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "留下你的想法"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()


class SubscriptionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
