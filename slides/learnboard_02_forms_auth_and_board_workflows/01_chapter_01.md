---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnBoard 02｜表單、帳號與留言權限"
footer: "Django 初學者課程｜LearnBoard"
---

## BootstrapFormMixin：讓 as_p 好看

```python
class BootstrapFormMixin:
    def apply_bootstrap(self):
        for field in self.fields.values():
            css_class = ("form-select" if isinstance(field.widget, forms.Select)
                         else "form-control")
            field.widget.attrs.setdefault("class", css_class)


class MessageForm(BootstrapFormMixin, forms.ModelForm):
    ...
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
```

Django 生成的 input 沒有 Bootstrap class；mixin 在 `__init__` 補上。商城的表單沿用同一招。