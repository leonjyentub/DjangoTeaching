---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnBoard 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnBoard｜啟動後要驗證的狀態
## 留言板的示範資料與畫面

在 `learnboard/` 執行整合教材的啟動流程後，第一次 seed 的專屬結果是：

| 項目 | 預期結果 |
|---|---|
| 帳號 | `alice / alice12345`、`bob / bob12345` |
| 首頁 | 「學言板 LearnBoard」留言牆 |
| 資料 | 4 則留言，其中包含 1 則訪客留言 |
| 未來能力 | 發文與帳號功能留給 Deck 02 |

`seed_demo` 使用 `get_or_create()`；同名帳號已存在時不會重設其密碼或其他既有資料。

---

## 只在 LearnBoard 要特別留意

- 執行指令的位置是 `learnboard/`：需同時看到 `manage.py` 與 `pyproject.toml`。
- 此專案沒有商品圖片上傳，因此不依賴 Pillow，也沒有 LearnMart 的 media 設定。
- 第一冊的首頁可允許 `author` 為空；模板必須把它顯示為「訪客」，不能直接讀取 `post.author.username`。

共通的環境檔、uv、migration 與開發伺服器意義，請回到整合教材 A～F 段。
