---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnBoard 02｜表單、帳號與留言權限"
footer: "Django 初學者課程｜LearnBoard"
---

## 模板中的權限感知按鈕

```html
{% if post.author == user %}
  <a class="btn btn-outline-primary btn-sm" href="{% url 'board:update' post.pk %}">編輯</a>
  <a class="btn btn-outline-danger btn-sm" href="{% url 'board:delete' post.pk %}">刪除</a>
{% elif user.is_staff %}
  <a class="btn btn-outline-danger btn-sm" href="{% url 'board:delete' post.pk %}">刪除</a>
{% endif %}
```

模板按鈕只是**體驗**；真正的關卡永遠在 view（queryset/test_func）。

直接打網址繞過按鈕？view 會擋——這才是安全的分界。