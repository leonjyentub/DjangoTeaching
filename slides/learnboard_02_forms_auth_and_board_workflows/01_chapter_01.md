---
marp: true
theme: default
size: 16:9
paginate: true
header: "LearnBoard 02｜表單、帳號與留言權限"
footer: "Django 初學者課程｜LearnBoard"
style: |
  section {
    font-family: 'Noto Sans CJK TC', 'Noto Serif CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', 'Heiti TC', sans-serif;
    font-size: 28px;
    line-height: 1.35;
  }
  h1, h2 {
    font-family: 'Noto Sans CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', sans-serif;
  }
  h1 { color: #1e3a8a; }
  h2 { color: #17324d; }
  blockquote {
    font-family: 'Noto Serif CJK TC', 'Noto Sans CJK TC', 'WenQuanYi Zen Hei', serif;
  }
  code, kbd {
    font-family: 'Noto Sans Mono CJK TC', 'SF Mono', Consolas,
                 'WenQuanYi Zen Hei Mono', 'Courier New', monospace;
    font-size: 0.82em;
  }
  pre { margin-top: 0.35em; margin-bottom: 0.35em; }
  .label { display: inline-block; padding: 0.15em 0.55em; border-radius: 999px; font-size: 0.72em; font-weight: 700; background: #e8eef5; color: #17324d; }
  .current { background: #e5f4ea; color: #17633a; }
  .warning { background: #fff0d9; color: #8a4b08; }
  .check { background: #f3e8ff; color: #6b21a8; }
  .small { font-size: 0.78em; }
---

# 第 1 章
## 完整表單生命週期

目標：能從 HTML 表單一路追到 Django 驗證、儲存、redirect 與提示訊息。

<!--
授課提示：本章要背的是「生命週期」而非 API 清單；每個語法都要求學生說出它在週期的哪一站。
-->

---

## 為什麼不能直接相信 `request.POST`？

瀏覽器是「資料來源」，不是可信任邊界。

使用者可以：

- 移除 HTML 的 `required`、`maxlength`
- 修改 hidden input
- 不經過你的頁面，直接送 HTTP request
- 把文字欄位送成空白或極端值

因此 View 必須在**伺服器端**驗證，再決定是否改資料。

---

## HTML form 的四個核心部分

```html
<form action="{% url 'board:list' %}" method="get">
  <label for="q">關鍵字</label>
  <input id="q" name="q" value="django">
  <button type="submit">搜尋</button>
</form>
```

- `action`：送到哪一個 URL
- `method`：GET 或 POST
- `name`：送出的 key
- `value`：送出的 value

---

## GET：查詢，不改變資料

```text
GET /?q=django
```

- 參數出現在網址上 → 可分享、可收藏
- 瀏覽器會快取；重新整理安全
- Django 從 `request.GET` 讀取

Deck 01 的搜尋就是標準 GET 用法。**凡是不新增/修改/刪除資料的操作，都用 GET。**

---

## POST：改變資料的動詞

```html
<form method="post" action="/new/">
  {% csrf_token %}
  <textarea name="content" maxlength="500"></textarea>
  <button type="submit">發布</button>
</form>
```

- 資料藏在 request body，不出現在網址
- 語意：「我要建立／修改東西」
- Django 從 `request.POST` 讀取
- 必須附 `{% csrf_token %}`（第 5 章揭曉原因）

---

## 表單生命週期全景

```text
1. GET /new/        → view 回傳空表單 HTML
2. 使用者填寫送出   → POST /new/
3. view 收 request.POST → Form 驗證
4a. 合法   → 存 DB → redirect（PRG）
4b. 不合法 → 重新渲染表單＋錯誤訊息
5. redirect 目標發起新的 GET → 看到結果
```

**4a 的 redirect 不是裝飾：**它防止重新整理時重複送 POST（PRG 模式）。

---

## Form 物件：伺服器端的第一道關卡

```python
from django import forms


class MessageForm(forms.Form):
    content = forms.CharField(
        label="留言內容",
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 3}),
    )
```

```python
form = MessageForm(request.POST)
if form.is_valid():          # 觸發全部驗證
    data = form.cleaned_data # 通過後才有的乾淨資料
```

HTML 的 `required`／`maxlength` 只是體驗；**驗證必須在這裡才算數**。

---

## is_valid() 與 cleaned_data

```python
>>> form = MessageForm({"content": "hi"})
>>> form.is_valid()
True
>>> form.cleaned_data["content"]
'hi'

>>> form = MessageForm({"content": ""})
>>> form.is_valid()
False
>>> form.errors
{"content": ["This field is required."]}
```

`errors` 是 dict-like：key 是欄位名，value 是錯誤清單——模板直接渲染成紅字。

---

## ModelForm：從 model 自動生成表單

```python
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("content",)
        widgets = {"content": forms.Textarea(
            attrs={"rows": 3, "placeholder": "想說什麼？（最多 500 字）"})}
```

- 欄位型別與驗證規則直接繼承 model（max_length=500 自動生效）
- `fields` 白名單明確宣告可編輯範圍——絕不省略它
- form.save() 直接產生／更新 model instance

> 教學順序先 Form 再 ModelForm：知道 ModelForm 幫你省了什麼。

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

---

## csrf_token：模板裡的一行保命符

```html
<form method="post">{% csrf_token %}…</form>
```

渲染結果是一個 hidden input：

```html
<input type="hidden" name="csrfmiddlewaretoken" value="xK9f…">
```

沒有它 → 所有 POST 一律 403（CsrfViewMiddleware 擋下）。原理在第 5 章。

---

## 匿名發文的最小實作（教學過渡版）

```python
def create_message(request):
    form = MessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("board:list")
    return render(request, "board/message_form.html", {"form": form})
```

`request.POST or None`：POST 時帶資料驗證，GET 時回空表單——一行表達兩種狀態。

> **常見錯誤：**忘記 redirect → 重新整理就重複發文。這是 PRG 缺角。

---

## messages framework：跨 redirect 的提示訊息

```python
from django.contrib import messages

messages.success(request, "留言已發布。")
return redirect("board:list")   # 訊息跟著 session 到下一頁
```

```html
{# base.html #}
{% for message in messages %}
  <div class="alert alert-{{ message.tags }}">{{ message }}</div>
{% endfor %}
```

redirect 之後仍能看到「留言已發布」，靠的是 session（下一章主角）＋一次性讀取。

---

## 第 1 章｜觀念檢核與實作

**觀念檢核：**

1. PRG 模式解決什麼問題？
2. `request.POST or None` 在 GET 與 POST 時各是什麼？
3. Form 與 ModelForm 怎麼選？
4. `{% csrf_token %}` 少了會怎樣？為什麼現在只說現象、不說原理？

**實作任務：**加上匿名發文功能（本冊第 2 章會把它改成登入限定），測試空白內容與 501 字內容都會被擋下。

→ 步驟與解答在配套手冊第 1 章。
