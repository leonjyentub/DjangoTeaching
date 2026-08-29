from django import forms
from django.contrib.auth.forms import UserCreationForm

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
        # author、published_at、view_count 由伺服器決定，不放進表單（回扣 seller 不在 fields）。
        fields = ("title", "slug", "category", "coauthors", "excerpt", "body", "status")
        widgets = {
            "body": forms.Textarea(attrs={"rows": 12, "placeholder": "支援 Markdown"}),
            "excerpt": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, author=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False
        if author is not None:
            # 動態縮小 queryset：共同作者不能選自己。
            self.fields["coauthors"].queryset = User.objects.exclude(pk=author.pk)
        self.apply_bootstrap()

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("status") == Article.Status.SCHEDULED and not cleaned.get("published_at"):
            # 教學版：排程時間簡化為「存檔後由編輯在 admin 補上」，這裡只擋明顯錯誤。
            pass
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
