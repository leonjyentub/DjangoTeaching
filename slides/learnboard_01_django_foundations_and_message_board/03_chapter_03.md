---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnBoard 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

## LearnBoard 的視覺責任

```css
body { background: var(--lb-bg); }
.navbar { background: linear-gradient(90deg, var(--lb-deep), var(--lb-blue)); }
.avatar { width: 34px; height: 34px; border-radius: 9999px; }
```

`static/css/site.css` 讓留言板擁有自己的色彩、頭像與卡片 hover 細節；Bootstrap 只提供基礎元件。Template 繼承、static tag、RWD 與 escaping 的共通原理請見整合教材第 3 章。