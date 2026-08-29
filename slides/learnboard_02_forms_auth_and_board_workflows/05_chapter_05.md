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

# 第 5 章
## 安全三課：CSRF、XSS、IDOR

目標：能指出每一種攻擊「利用什麼信任」以及「哪一行程式碼擋住它」。

<!--
授課提示：本章建議搭配 trust_boundary 圖解。三課的共同句型：「攻擊者濫用了＿＿的信任，防線是＿＿。」
-->

---

## 安全的心智模型：信任邊界

![w:1000](../assets/trust_boundary.svg)

瀏覽器送來的一切——GET 參數、POST body、cookie 內容——都在邊界之外。

**伺服器端的驗證與授權，是唯一算數的防線。**

---

## XSS：注入的腳本

```text
攻擊：留言內容寫 <script>偷取document.cookie</script>
若輸出未跳脫 → 其他訪客的瀏覽器執行它
```

**我們的防線（已經在作用）：**

- Template 的 `{{ }}` 自動跳脫 `< > & " '`（Deck 01 3-11）
- 全專案禁止對使用者內容使用 `|safe`

**驗證方式：**admin 建立含 `<script>alert(1)</script>` 的留言，前台只會看到文字，不會彈窗。

---

## CSRF：借刀殺人的偽造請求

```text
情境：你登入著 A 站，又逛到惡意 B 站。
B 站偷偷向 A 站送出 POST（瀏覽器自動附上 A 站的 cookie）。
A 站看到有效 session → 以為是你本人。
```

攻擊者不需要偷 cookie——他借**你的瀏覽器**出手。

**防線：**A 站要求 POST 附帶一張「本站發放的暗號」（csrfmiddlewaretoken）。B 站拿不到這個 token，請求被 CsrfViewMiddleware 以 403 拒絕。

這就是每個 `<form method="post">` 都要有 `{% csrf_token %}` 的原因。

---

## CSRF 實測：拿掉 token 會怎樣？

```html
<!-- 暫時刪掉 message_form.html 的 {% csrf_token %} -->
```

```text
登入 → 送出留言 →
Forbidden (403)
CSRF verification failed. Request aborted.
```

恢復 token 後一切正常。**親手觸發一次，比背十遍定義有用。**

> **常見錯誤：**API 工具（curl/Postman）測 POST 失敗 403——不是壞了，是它們沒帶 token。

---

## IDOR：不安全的直接物件參照

```text
攻擊：猜測或遍歷 /messages/3/edit/、/messages/4/edit/…
弱防線：只要登入就能打開 → 別人的留言任你改
強防線：queryset 過濾（404）＋test_func（403）
```

IDOR 的本質：**只驗證了「登入」，沒驗證「歸屬」。**

第 4 章的雙層防禦正是針對它。測試章將把四種身份場景固化成自動化測試。

---

## 教學版尚未處理的事（誠實清單）

- DEBUG=True 與課堂 SECRET_KEY——正式環境必改
- 無 HTTPS、rate limit、帳號鎖定
- 密碼強度規則採 Django 預設，未接 HIBP 之類服務
- 無稽核 log（誰刪了哪則留言）

> 這份清單在商城 Deck 02 的安全章會再加長。知道邊界，比假裝安全更重要。

---

## 第 5 章｜觀念檢核

1. 三種攻擊分別濫用了什麼信任？
2. 為什麼 csrf token 能防 CSRF 卻防不了 XSS？
3. 若把留言內容加上 `|safe`，哪一課的防線瓦解了？
4. IDOR 與第 4 章哪一段程式碼一一對應？
