---
marp: true
theme: default
size: 16:9
paginate: true
header: "Django 01｜共通基礎：LearnBoard × LearnMart"
footer: "初學者教材｜共通觀念 → 兩個專案對照"
style: |
  section {
    font-family: 'Noto Sans CJK TC', 'Noto Serif CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', 'Heiti TC', sans-serif;
    font-size: 28px;
    line-height: 1.35;
    padding: 58px 70px;
  }
  h1, h2 {
    font-family: 'Noto Sans CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', sans-serif;
  }
  h1 { color: #8f1d2c; }
  h2 { color: #a52a3a; }
  blockquote {
    border-left: 6px solid #d69aa3; padding-left: 18px; color: #4c3438;
    font-family: 'Noto Serif CJK TC', 'Noto Sans CJK TC', 'WenQuanYi Zen Hei', serif;
  }
  code, kbd {
    font-family: 'Noto Sans Mono CJK TC', 'SF Mono', Consolas,
                 'WenQuanYi Zen Hei Mono', 'Courier New', monospace;
    font-size: 0.92em;
  }
  pre { font-size: 0.72em; line-height: 1.28; }
  table { font-size: 0.78em; }
  strong { color: #7d1726; }
---

# Deck 1 總結
## 你已經能追蹤資料驅動頁面

```text
環境 → Django 啟動 → HTTP request → URL → View
→ Model / QuerySet → context → Template → responsive response
```

你已經學會：

- 分辨環境、schema 與示範資料命令
- 讀懂 URL、View、Template 的契約
- 由 model field/relationship 理解 database shape
- 由 template 使用方式反推 ORM optimization
- 解釋搜尋與 catalog 的完整 request flow

---

## 下一份教材會加入什麼？

Deck 2 將在本份基礎上加入：

- POST、Form、ModelForm、validation、CSRF、PRG
- 圖片上傳與 media 完整 request flow
- Custom User、session、登入、角色與 ownership
- Class-based View 與 `.as_view()`
- 購物車、訂單快照、checkout transaction 與 locking
- Security boundary 與 workflow tests

先確定你能用檔案與資料型別說明 catalog；之後才把「讀資料」推進到「可信任地改資料」。
