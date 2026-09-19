## 來源與整合去向

> 整合 2026-09-19：本對照表原位於 `slides/django_course/`，隨連續授課教材一起移到 `slides/` 根目錄。原始四個資料夾（01、01B、02、03）已於整合後移除，下列「原始 X」僅為整合紀錄；原始內容已全部併入新章節，檔案保留於 git 歷史。

本索引涵蓋四個原始資料夾的 **12 份 Marp、610 個來源頁段**（包含 1 個空白頁段）。頁碼依 Markdown 的 Marp 分頁順序計算。

- **保留**：搬移、統一章號及連結，必要時調整跨章措辭。
- **改寫**：保留教學意圖，改為本課環境、例子或銜接方式。
- **合併**：重複概念、舊封面或舊導讀合併至新章；空白頁移除。每筆附原因。
- 原 A 第 45 頁分為第 3 章 HTTP 圖解與訊息欄位兩頁；A 第 92 頁分為第 4 章 MVT 圖解與責任說明兩頁。
- 新增頁：17 份檔案封面、路線與銜接；27 章章首、操作環境及驗收；另補連續練習、ModelForm、DeleteView、案例轉接與部署範圍。
- 新增 LearnBoard 範例核對 [forms.py](../learnboard/board/forms.py)、[views.py](../learnboard/board/views.py)、[urls.py](../learnboard/board/urls.py)。

機器可讀資料見 [source_manifest.json](source_manifest.json)。下表「新位置」先連到該章，p. 為新 MD 的投影片順序。

## A：原始 01_django_foundations_and_two_projects.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：Django 01 / 專案的共通基礎 | 合併 | [第 1 章](01_開發環境與專案建立.md#chapter-1)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：0-1 這份整合教材服務哪兩個專案？ | 合併 | [第 1 章](01_開發環境與專案建立.md#chapter-1)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 3：0-2 學完後要能讀懂什麼？ | 合併 | [第 1 章](01_開發環境與專案建立.md#chapter-1)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 4：0-3 課程地圖：基礎、資料層與頁面整合 | 合併 | [第 1 章](01_開發環境與專案建立.md#chapter-1)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 5：0-4 學習方式：每章都走同一個循環 | 合併 | [第 1 章](01_開發環境與專案建立.md#chapter-1)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 6：0-5 兩個專案的讀檔路線 | 合併 | [第 1 章](01_開發環境與專案建立.md#chapter-1)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 7：第一章 / 環境準備、專案骨架與開發伺服器 | 合併 | [第 1 章](01_開發環境與專案建立.md#chapter-1)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 8：1-0 第一章學習順序與各段成果 | 合併 | [第 1 章](01_開發環境與專案建立.md#chapter-1)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 9：1-1 先認識 uv：管理 Python 專案的工具 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 5（1-1） |
| 10：1-2 安裝 uv，再重新開啟終端機 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 6（1-2） |
| 11：1-3 venv 與 `.venv/` 是什麼？ | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 7（1-3） |
| 12：1-4 Python：真正執行程式的直譯器 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 8（1-4） |
| 13：1-5 建立自己的空練習資料夾 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 10（1-6） |
| 14：1-6 初始化 Python 專案與虛擬環境 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 11（1-7） |
| 15：1-7 確認執行的是哪一個 Python | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 12（1-8） |
| 16：1-8 安裝 Django，確認 django-admin 可用 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 14（1-10） |
| 17：1-9 `python -m` 到底是什麼？ | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 15（1-11） |
| 18：1-10 傳統 venv：另一種環境準備方式 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 16（1-12） |
| 19：1-11 先分清楚 project 與 app | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 26（2-1） |
| 20：1-12 用 django-admin 建立 project | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 27（2-2） |
| 21：1-13 透過 manage.py 建立第一個 app | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 28（2-3） |
| 22：1-14 先看外層：每一項由誰建立？ | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 29（2-4） |
| 23：1-15 config：網站共用設定與入口 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 30（2-5） |
| 24：1-16 pages：功能程式從這裡開始 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 31（2-6） |
| 25：1-17 `manage.py` 如何知道要用哪份設定？ | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 32（2-7） |
| 26：1-18 Git：記錄你每次完成的修改 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 33（2-8） |
| 27：1-19 `.gitignore`：哪些檔案可以重建？ | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 34（2-9） |
| 28：1-20 保存第一個可比較的版本 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 35（2-10） |
| 29：1-21 三個環境檔案各管什麼？ | 改寫 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 17（1-13） |
| 30：1-22 讀懂 pyproject.toml 的基本語法 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 18（1-14） |
| 31：1-23 版本範圍與鎖檔的精確版本 | 改寫 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 19（1-15） |
| 32：1-24 直接依賴、開發依賴與同步 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 20（1-16） |
| 33：1-25 settings 是 Python：先註冊自己的 app | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 36（2-11） |
| 34：1-26 settings 地圖：先知道要去哪裡找 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 37（2-12） |
| 35：1-27 settings 地圖：資料、語言與靜態資源 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 38（2-13） |
| 36：1-28 App 註冊與 template 搜尋的差別 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 39（2-14） |
| 37：1-29 本機開發設定的使用邊界 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 40（2-15） |
| 38：1-30 資料庫：持續保存網站資料 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 41（2-16） |
| 39：1-31 第一次 migrate：建立內建功能的資料表 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 43（2-18） |
| 40：1-32 分清楚之後會用到的資料指令 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 44（2-19） |
| 41：1-33 啟動開發伺服器 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 45（2-20） |
| 42：1-34 第一次 preview：看到 Django 歡迎頁 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 46（2-21） |
| 43：1-35 啟動前後的檢查不能互相取代 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 47（2-22） |
| 44：第二章 / HTTP 協定、URL 路由與 View 視圖 | 合併 | [第 3 章](02_HTTP路由與View.md#chapter-3)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 45：2-1 HTTP：瀏覽器與伺服器交換訊息 | 改寫 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 5（3-1） |
| 46：2-2 拆開網址，找出路由真正比對的部分 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 7（3-3） |
| 47：2-3 在 Network 看見 request 與 response | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 8（3-4） |
| 48：2-4 常見 response status | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 9（3-5） |
| 49：2-5 第一個 View：先回傳固定文字 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 10（3-6） |
| 50：2-6 自行新增 app 的 urls.py | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 11（3-7） |
| 51：2-7 `path()` 四個重要位置 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 12（3-8） |
| 52：2-8 把 project URL 接到 app URL | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 13（3-9） |
| 53：2-9 立刻驗收：第一個頁面確實可用 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 14（3-10） |
| 54：2-10 動態路徑：把網址片段傳入函式 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 15（3-11） |
| 55：2-11 常用 converter | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 16（3-12） |
| 56：2-12 Query string 由 request.GET 讀取 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 17（3-13） |
| 57：2-13 命名 URL：把名稱與路徑分開 / urlpatterns 內： | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 18（3-14） |
| 58：2-14 在 Python 反向產生網址 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 19（3-15） |
| 59：2-15 在 template 反向產生網址 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 20（3-16） |
| 60：2-16 `HttpResponse` 與安全顯示 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 21（3-17） |
| 61：2-17 需要 HTML 時，明確處理使用者輸入 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 22（3-18） |
| 62：2-18 追蹤一次最小 request 的旅程 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 23（3-19） |
| 63：2-19 404 與 500：沿著流程找問題 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 24（3-20） |
| 64：2-20 按順序排除常見問題 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 25（3-21） |
| 65：2-21 把驗收寫進 tests.py | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 26（3-22） |
| 66：2-22 再確認動態網址、query 與 404 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 27（3-23） |
| 67：2-23 先完成自己的練習，再進行專案對照 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 31（3-27） |
| 68：2-24 現在才打開 LearnBoard × LearnMart | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 23（6-19） |
| 69：2-25 教材根目錄與 Django 應用根目錄 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 24（6-20） |
| 70：2-26 環境對照：共同版本與 Pillow 差異 | 改寫 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 25（6-21） |
| 71：2-27 實際 TOML 節錄可以這樣讀 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 26（6-22） |
| 72：2-28 settings 對照：先找共同設定 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 27（6-23） |
| 73：2-29 settings 對照：功能增加後的差異 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 28（6-24） |
| 74：2-30 建立指令：完成專案只讀取，不再重跑 / LearnBoard 骨架的等價建立指令（只供對照） | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 29（6-25） |
| 75：2-31 從完成專案啟動 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 30（6-26） |
| 76：2-32 `seed_demo` 建立哪些資料？ | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 31（6-27） |
| 77：2-33 預覽完成專案並記錄結果 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 32（6-28） |
| 78：2-34 URL、View 與反向解析的實際對照 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 33（6-29） |
| 79：2-35 對照動態路由與反向產生網址 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 34（6-30） |
| 80：2-36 從文字回應走向資料頁 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 32（3-28） |
| 81：2-37 從自己的最小流程擴充到完整頁面 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 33（3-29） |
| 82：2-38 專案對照實作：先找檔案，再說明理由 | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 8（12-4） |
| 83：2-39 兩個首頁目前各自做了哪些事？ | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 52（13-28） |
| 84：2-40 從一個 `Message` 到商城的關聯圖 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 18（8-14） |
| 85：2-41 專案版教材如何接續使用 | 合併 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 86：2-42 觀念檢核：環境與啟動 | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 51（2-26） |
| 87：2-43 觀念檢核：URL 與 request flow | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 34（3-30） |
| 88：2-44 查閱來源與參考資料 | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 35（3-31） |
| 89：第三章 / Template、static 與響應式頁面 | 合併 | [第 4 章](03_Template與頁面呈現.md#chapter-4)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 90：3-1 從字串 response 到 template | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 5（4-1） |
| 91：3-2 `render()` 的三個核心參數 | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 6（4-2） |
| 92：3-2 步驟 A：MVT 心智模型 | 改寫 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 7（4-3） |
| 93：3-2 步驟 B：MVT 如何分工圖解 | 改寫 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 9（4-5） |
| 94：3-3 Template 到底放在哪裡？ | 改寫 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 10（4-6） |
| 95：3-4 三種 Django template delimiter | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 11（4-7） |
| 96：3-5 變數與 dot lookup | 改寫 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 12（4-8） |
| 97：3-6 Template autoescaping 的正確邊界 | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 13（4-9） |
| 98：3-7 Filter：改變顯示，不改資料庫 | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 14（4-10） |
| 99：3-8 `if`：依狀態決定顯示 | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 15（4-11） |
| 100：3-9 `for` 與 `{% empty %}` | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 16（4-12） |
| 101：3-10 URL tag 接回上一章的命名路由 | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 17（4-13） |
| 102：3-11 Template inheritance：先看 parent | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 30（5-1） |
| 103：3-12 Template inheritance：再看 child | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 31（5-2） |
| 104：3-13 `include` 與 `extends` 的工作不同 | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 32（5-3） |
| 105：3-14 static：開發者提供的固定資產 | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 33（5-4） |
| 106：3-15 static 與 media 不要混淆 | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 34（5-5） |
| 107：3-16 Bootstrap 與 Django 各做什麼？ | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 35（5-6） |
| 108：3-17 viewport 為何必須放在 `<head>`？ | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 36（5-7） |
| 109：3-18 Bootstrap grid 的 12 欄心智模型 | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 37（5-8） |
| 110：3-19 Mobile-first：breakpoint 代表「以上」 | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 38（5-9） |
| 111：3-20 商品網格：完整父子結構 | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 39（5-10） |
| 112：3-21 Utility class 要讀成組合語言 | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 40（5-11） |
| 113：3-22 語意與無障礙不是最後才補 | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 41（5-12） |
| 114：3-23 常見 template 問題如何定位？ | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 42（5-13） |
| 115：第三章｜觀念檢核與實作 | 保留 | [第 5 章](03_Template與頁面呈現.md#chapter-5)，p. 43（5-14） |
| 116：4-1 資料模型銜接：頁面的資料從哪裡來？ | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 5（6-1） |
| 117：4-2 專案導覽：先看資料之間的關係 | 改寫 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 19（8-15） |
| 118：4-3 學習路線：在 01B 完成資料層 | 合併 | [第 6 章](04_Model與欄位設計.md#chapter-6)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 119：5-1 回到頁面前：資料層檢核 | 改寫 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 5（12-1） |
| 120：5-2 整合準備：後台資料與前台頁面 | 改寫 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 6（12-2） |
| 121：5-3 整合任務：沿著一筆資料追蹤頁面 | 改寫 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 7（12-3） |
| 122：第六章 / 組合成可搜尋的資料驅動商品目錄 | 合併 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 123：6-1 步驟 A：Vertical slice 前半（Request 轉 QuerySet） | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 45（13-21） |
| 124：6-1 步驟 B：Vertical slice 後半（Context 轉 HTML） | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 46（13-22） |
| 125：6-2 先用 Function View 看清全部責任 | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 9（12-5） |
| 126：6-3 List 與 Detail 是兩種不同查詢形狀 / List | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 10（12-6） |
| 127：6-4 `get_object_or_404` 做了什麼？ | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 11（12-7） |
| 128：6-5 GET 搜尋表單先建立 URL 狀態 | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 12（12-8） |
| 129：6-6 Query string 由 `request.GET` 讀取 | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 13（12-9） |
| 130：6-7 搜尋名稱或說明 | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 14（12-10） |
| 131：6-8 把搜尋字串送回 template | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 15（12-11） |
| 132：6-9 分類篩選同樣是 GET state | 改寫 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 16（12-12） |
| 133：6-10 步驟 A：多個 query parameters 連結語法 | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 17（12-13） |
| 134：6-10 步驟 B：辨識目前 UI 的狀態保持邊界 | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 18（12-14） |
| 135：6-11 Pagination 是 QuerySet 與 UI 的共同狀態 | 改寫 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 43（13-19） |
| 136：6-12 `include` 適合抽出分頁 UI | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 44（13-20） |
| 137：6-13 商品卡會讀 relation，所以先載入 | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 19（12-15） |
| 138：6-14 圖片、fallback 與 alt 要在同一段理解 | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 20（12-16） |
| 139：6-15 空結果不是錯誤，是正常 UI state | 保留 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)，p. 21（12-17） |
| 140：6-16 步驟 A：從 Function View 收斂至 LearnMart | 改寫 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 41（13-17） |
| 141：6-16 步驟 B：目前 source 的 query state 優化細節 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 42（13-18） |
| 142：6-17 步驟 A：完整 request flow 逐層解析 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 47（13-23） |
| 143：6-17 步驟 B：圖解 Catalog 的完整資料流 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 48（13-24） |
| 144：6-18 步驟 A：手動驗證 catalog 行為 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 49（13-25） |
| 145：6-18 步驟 B：用 focused test 固定搜尋行為 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 50（13-26） |
| 146：第六章｜觀念檢核與實作 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 51（13-27） |
| 147：第七章 / LearnBoard 留言板對照實作 | 合併 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 148：7-1 同一個 vertical slice，資料領域不同 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 37（13-13） |
| 149：列表比較表 | 改寫 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 38（13-14） |
| 150：7-2 專案對照：用資料規則解讀留言牆 | 改寫 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 39（13-15） |
| 151：7-3 LearnBoard 的搜尋與模板輸出 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 40（13-16） |
| 152：課程總結 / 共通基礎回顧與下一階段地圖 | 合併 | [第 12 章](07_資料列表搜尋與分頁.md#chapter-12)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 153：總結-1 你已經能追蹤資料驅動頁面 | 改寫 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 53（13-29） |
| 154：總結-2 下一份教材會加入什麼？ | 改寫 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 54（13-30） |

## L：原始 02_first_contact_lab_and_debugging.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：Django 01 補充 Lab / 第一次從 Terminal 走到 Django Page | 合併 | [第 1 章](01_開發環境與專案建立.md#chapter-1)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：0. 每次先確認「我在哪裡」 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 9（1-5） |
| 3：1. `uv sync` 到底做什麼？ | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 21（1-17） |
| 4：2. `uv run` 的心智模型 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 13（1-9） |
| 5：3. 第一次先跑 `check` | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 48（2-23） |
| 6：4. Migration 三步驟不要背成一團 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 37（9-14） |
| 7：5. `makemigrations --check` 是什麼？ | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 38（9-15） |
| 8：6. 看 migration，不要只相信它 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 39（9-16） |
| 9：7. 啟動 server 後 Terminal 不會回 prompt | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 49（2-24） |
| 10：8. 成功啟動長什麼樣？ | 保留 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 50（2-25） |
| 11：9. Request log 是第一個 debugger | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 28（3-24） |
| 12：10. 常見 status code 怎麼讀？ | 合併 | [第 3 章](02_HTTP路由與View.md#chapter-3)；常見狀態碼併入 HTTP response status |
| 13：11. Traceback 要從哪裡開始？ | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 29（3-25） |
| 14：12. `ModuleNotFoundError` 常見原因 | 保留 | [第 1 章](01_開發環境與專案建立.md#chapter-1)，p. 22（1-18） |
| 15：13. `TemplateDoesNotExist` | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 26（4-22） |
| 16：14. `NoReverseMatch` | 保留 | [第 3 章](02_HTTP路由與View.md#chapter-3)，p. 30（3-26） |
| 17：15. ORM 先在 shell 小步驗證 | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 22（10-18） |
| 18：16. 修改 model 後的固定節奏 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 40（9-17） |
| 19：17. 測試不要一次只會「全部跑」 | 合併 | [第 18 章](12_購物車與流程測試.md#chapter-18)；單支測試命令併入流程測試定位 |
| 20：18. 測試 failure 怎麼讀？ | 合併 | [第 18 章](12_購物車與流程測試.md#chapter-18)；failure 判讀併入測試失敗分類 |
| 21：19. 每次 lab 的完成條件 | 合併 | [第 3 章](02_HTTP路由與View.md#chapter-3)；Lab 完成條件併入每章驗收頁 |
| 22：20. 第一次 Django 的固定節奏 | 合併 | [第 2 章](01_開發環境與專案建立.md#chapter-2)；固定操作節奏併入環境、路由、migration 各章驗收 |

## B：原始 01b_models_orm_and_admin.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：Django 01B / 資料模型、ORM 與 Django Admin | 合併 | [第 6 章](04_Model與欄位設計.md#chapter-6)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：0-1 本冊在課程中的位置 | 合併 | [第 6 章](04_Model與欄位設計.md#chapter-6)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 3：0-2 學習成果與課堂安排 | 合併 | [第 6 章](04_Model與欄位設計.md#chapter-6)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 4：0-3 兩個專案提供的真實案例 | 改寫 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 35（6-31） |
| 5：0-4 先學 Django，再對照專案 | 改寫 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 36（6-32） |
| 6：0-5 最小練習專案：從空資料夾開始 | 改寫 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 13（6-9） |
| 7：0-6 把 app 加入設定 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 14（6-10） |
| 8：0-7 最小 models.py：分類 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 16（6-12） |
| 9：0-8 最小 models.py：商品 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 17（6-13） |
| 10：0-9 建表：migration 是資料結構的版本紀錄 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 18（6-14） |
| 11：0-10 Shell：建立第一筆資料 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 19（6-15） |
| 12：0-11 Shell：查詢、修改與刪除 | 改寫 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 23（10-19） |
| 13：0-12 最小 Admin：把資料放到後台 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 20（6-16） |
| 14：0-13 圖片顯示所需的開發設定 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 21（6-17） |
| 15：0-13B 開發環境的 media 路由 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 22（6-18） |
| 16：0-14 切換案例前先確認環境 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 37（6-33） |
| 17：第 1 章 / Model、主鍵與唯一性 | 合併 | [第 6 章](04_Model與欄位設計.md#chapter-6)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 18：1-1 Model 的三種對應 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 6（6-2） |
| 19：1-2 一個 Model 的完整骨架 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 7（6-3） |
| 20：1-2B `__str__`：物件顯示的文字 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 8（6-4） |
| 21：1-2C Model 方法與商品詳情網址 | 合併 | [第 17 章](11_CRUD與物件權限.md#chapter-17)；get_absolute_url 解釋併入編輯型 CBV 的成功 redirect |
| 22：1-3 Primary key：資料的穩定身分 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 9（6-5） |
| 23：1-4 自訂主鍵與 UUID | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 10（6-6） |
| 24：1-5 Primary key、unique、複合唯一 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 11（6-7） |
| 25：1-6 用資料列理解複合唯一 | 保留 | [第 6 章](04_Model與欄位設計.md#chapter-6)，p. 12（6-8） |
| 26：第 2 章 / 欄位型別與參數：從需求做選擇 | 合併 | [第 7 章](04_Model與欄位設計.md#chapter-7)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 27：2-1 設計欄位先問五個問題 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 41（7-1） |
| 28：2-2 常用欄位選擇表 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 42（7-2） |
| 29：2-3 讀懂一個欄位宣告 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 43（7-3） |
| 30：2-4 CharField 與 TextField / Product | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 44（7-4） |
| 31：2-5 blank 與 null：兩個不同層次 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 45（7-5） |
| 32：2-6 default、editable 與驗證 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 46（7-6） |
| 33：2-6B full_clean 與 save 分開理解 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 47（7-7） |
| 34：2-7 整數欄位：0 算不算合法？ | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 48（7-8） |
| 35：2-8 DecimalField 與 FloatField / Python 金額使用 Decimal("199.90") | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 49（7-9） |
| 36：2-9 Boolean 與 choices | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 50（7-10） |
| 37：2-10 日期、時間、日期時間 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 51（7-11） |
| 38：2-11 三種時間設定怎麼選？ | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 52（7-12） |
| 39：2-12 時區與未發生的事件 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 53（7-13） |
| 40：2-13 SlugField：可讀的網址代稱 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 54（7-14） |
| 41：2-14 Slug 生成與重複值 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 55（7-15） |
| 42：2-15 圖片：資料庫存路徑，storage 存檔案 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 56（7-16） |
| 43：2-16 圖片從上傳到顯示 | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 57（7-17） |
| 44：2-17 欄位設計練習（20 分鐘） | 保留 | [第 7 章](04_Model與欄位設計.md#chapter-7)，p. 58（7-18） |
| 45：第 3 章 / 一對一、一對多、多對多 | 合併 | [第 8 章](05_模型關聯與Migration.md#chapter-8)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 46：3-1 關聯先看兩個方向的數量 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 5（8-1） |
| 47：3-2 LearnBoard：留言指向作者 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 6（8-2） |
| 48：3-3 外鍵值與關聯物件 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 7（8-3） |
| 49：3-4 on_delete 與刪除方向 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 8（8-4） |
| 50：3-5 一對一：帳號的額外資料 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 9（8-5） |
| 51：3-6 一對一的正反向都是單一物件 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 10（8-6） |
| 52：3-7 多對多：商品可以貼多個標籤 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 11（8-7） |
| 53：3-8 多對多的資料其實在第三張表 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 12（8-8） |
| 54：3-9 add、remove、set、clear | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 13（8-9） |
| 55：3-10 進階｜through：關係本身還有資料 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 14（8-10） |
| 56：3-11 CartItem 與 OrderItem 的建模意義 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 15（8-11） |
| 57：3-11B 訂單快照：保留購買當下的資料 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 16（8-12） |
| 58：3-12 關聯練習（20 分鐘） | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 17（8-13） |
| 59：第 4 章 / Meta、資料驗證與 migration | 合併 | [第 9 章](05_模型關聯與Migration.md#chapter-9)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 60：4-1 Model、表單與 Admin 的設定位置 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 24（9-1） |
| 61：4-2 ordering 與顯示名稱 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 25（9-2） |
| 62：4-3 進階｜db_table 與 indexes | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 26（9-3） |
| 63：4-4 完整的 Meta.constraints | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 27（9-4） |
| 64：4-4B Review 評價唯一約束 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 28（9-5） |
| 65：4-5 CheckConstraint：範圍與跨欄位規則 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 29（9-6） |
| 66：4-6 驗證不是只有一個入口 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 30（9-7） |
| 67：4-6B 專案初始化前的 User 決定 | 改寫 | [第 2 章](01_開發環境與專案建立.md#chapter-2)，p. 42（2-17） |
| 68：4-7 Model、migration 與資料表 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 31（9-8） |
| 69：4-7B 取得專案與修改模型的操作差異 / clone／取得既有 repository | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 32（9-9） |
| 70：4-7C migration 訊息與狀態檢查 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 33（9-10） |
| 71：4-8 新增欄位的操作與證據 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 34（9-11） |
| 72：4-8B 產生、檢查並套用 migration | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 35（9-12） |
| 73：4-9 既有資料讓變更更困難 | 保留 | [第 9 章](05_模型關聯與Migration.md#chapter-9)，p. 36（9-13） |
| 74：第 5 章 / ORM 操作：先看回傳值，再組查詢 | 合併 | [第 10 章](06_ORM與Admin.md#chapter-10)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 75：5-1 Manager、QuerySet、instance | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 5（10-1） |
| 76：5-2 建立與修改：記憶體不等於已存檔 | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 6（10-2） |
| 77：5-2B 建立商品前先取得必要關聯 | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 7（10-3） |
| 78：5-2C 刪除單筆練習商品 | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 8（10-4） |
| 79：5-3 篩選、排除、排序與切片 | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 9（10-5） |
| 80：5-4 常用 lookup 與 Q | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 10（10-6） |
| 81：5-5 values 與 values_list 的結果 / 每列像 {"id": 17, "name": "鍵盤"} | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 11（10-7） |
| 82：5-6 關聯查詢與 distinct | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 12（10-8） |
| 83：5-7 Lazy evaluation 與查詢成本 | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 13（10-9） |
| 84：5-7B N+1：列表逐筆讀取關聯的成本 | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 14（10-10） |
| 85：5-8 關聯預載取決於資料形狀 | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 15（10-11） |
| 86：5-9 aggregate 與 annotate / 整份集合 → 一個摘要字典 | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 16（10-12） |
| 87：5-9B 商品平均評分的查詢行為 | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 17（10-13） |
| 88：5-10 進階｜更新、刪除與原子運算 | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 18（10-14） |
| 89：5-11 get_or_create 與 update_or_create | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 19（10-15） |
| 90：5-11B seed_demo 重跑會發生什麼？ | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 20（10-16） |
| 91：5-12 ORM 操作練習（25 分鐘） | 保留 | [第 10 章](06_ORM與Admin.md#chapter-10)，p. 21（10-17） |
| 92：第 6 章 / Django Admin：可操作的資料管理後台 | 合併 | [第 11 章](06_ORM與Admin.md#chapter-11)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 93：6-1 Admin 在系統中的角色 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 27（11-1） |
| 94：6-2 第一次啟動 Admin | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 28（11-2） |
| 95：6-3 最小註冊與 ModelAdmin / app 的 admin.py；以下兩種擇一 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 29（11-3） |
| 96：6-4 LearnBoard：留言列表與搜尋 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 30（11-4） |
| 97：6-5 LearnMart：商品列表的三個設定 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 31（11-5） |
| 98：6-6 編輯表單：fields、fieldsets、readonly | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 32（11-6） |
| 99：6-7 Admin 的 slug 輸入提示 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 33（11-7） |
| 100：6-8 關聯選單、autocomplete 與查詢 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 34（11-8） |
| 101：6-9 訂單 Inline：同頁看父子資料 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 35（11-9） |
| 102：6-10 訂單明細唯讀的教學設計 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 36（11-10） |
| 103：6-11 staff、superuser、Group 與模型權限 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 37（11-11） |
| 104：6-12 進階｜權限與資料範圍 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 38（11-12） |
| 105：6-13 現有 UserAdmin 為何另有一個 class？ | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 39（11-13） |
| 106：6-14 進階｜Admin action：批次下架 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 40（11-14） |
| 107：6-15 Admin 操作實驗（35 分鐘） | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 41（11-15） |
| 108：6-15B 整合 migration 與 Admin 的精選欄位 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 42（11-16） |
| 109：6-16 Admin 常見問題排查 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 43（11-17） |
| 110：第 7 章 / 整合練習與後續課程 | 合併 | [第 11 章](06_ORM與Admin.md#chapter-11)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 111：7-1 一對一與多對多實作路線 | 保留 | [第 8 章](05_模型關聯與Migration.md#chapter-8)，p. 20（8-16） |
| 112：7-2 綜合設計：商品、標籤與管理後台 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 44（11-18） |
| 113：7-3 離堂檢核 | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 45（11-19） |
| 114：7-4 01、02、03 的銜接 | 合併 | [第 11 章](06_ORM與Admin.md#chapter-11)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 115：7-5 官方參考：Model 與 ORM | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 46（11-20） |
| 116：7-6 官方參考：關聯、檔案與 Admin | 保留 | [第 11 章](06_ORM與Admin.md#chapter-11)，p. 47（11-21） |

## C：原始 02_forms_auth_and_two_projects.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：Django 02 / 兩個專案的表單、身份驗證與工作流程 | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：兩個專案共用同一套安全骨架 | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 3：這份教材接續什麼？ | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 4：Model、表單與 Admin 的先備連結 | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 5：本冊最終成果 | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 6：閱讀標籤 | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 7：本冊章節地圖 | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 8：兩個專案的實作路線 | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 9：第一次操作建議搭配兩份補充 | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 10：第 1 章 / 完整表單生命週期 | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 11：為什麼不能直接相信 `request.POST`？ | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 5（15-1） |
| 12：HTML form 的四個核心部分 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 6（15-2） |
| 13：GET：查詢，不改變資料 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 7（15-3） |
| 14：GET 參數要保留在畫面上 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 8（15-4） |
| 15：POST：要求伺服器改變狀態 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 9（15-5） |
| 16：Form 與 ModelForm | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 10（15-6） |
| 17：<span class="label">教學用最小範例</span> 先從 Form 開始 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 11（15-7） |
| 18：Unbound form：還沒有收到資料 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 12（15-8） |
| 19：Bound form：已經收到資料 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 13（15-9） |
| 20：初學時先寫明確的 GET／POST 分支 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 14（15-10） |
| 21：為什麼不先教 `request.POST or None`？ | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 15（15-11） |
| 22：`is_valid()` 做了什麼？ | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 16（15-12） |
| 23：顯示錯誤，不要丟掉使用者輸入 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 17（15-13） |
| 24：自訂單一欄位驗證 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 18（15-14） |
| 25：跨欄位驗證使用 `clean()`（1／2） | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 19（15-15） |
| 26：跨欄位驗證使用 `clean()`（2／2） | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 20（15-16） |
| 27：ModelForm 的 `Meta` | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 22（15-18） |
| 28：為什麼 `seller` 不在 `fields`？ | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 23（15-19） |
| 29：`save()` 與 `save(commit=False)` | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 24（15-20） |
| 30：CSRF：防止跨站 mutation 濫用既有 session | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 25（15-21） |
| 31：PRG：成功 POST 後 redirect | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 26（15-22） |
| 32：Messages：跨 redirect 的一次性回饋 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 27（15-23） |
| 33：圖片上傳：HTML 必須改 encoding | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 28（15-24） |
| 34：Function View 要同時綁定 POST 與 FILES | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 29（15-25） |
| 35：Generic editing view 如何處理檔案？ | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 19（17-15） |
| 36：第 1 章概念檢核 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 35（15-31） |
| 37：第 1 章 LearnMart 實作 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 36（15-32） |
| 38：第 2 章 / 身份驗證、Session 與帳號流程 | 合併 | [第 16 章](10_帳號登入與Session.md#chapter-16)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 39：Authentication 與 Authorization | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 5（16-1） |
| 40：自訂 User 必須很早決定 | 改寫 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 6（16-2） |
| 41：三種 User 參照方式不要混為一談 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 7（16-3） |
| 42：LearnMart User 繼承 AbstractUser | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 8（16-4） |
| 43：Role 是商業角色，不是 Django admin 權限 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 9（16-5） |
| 44：教學版的 seller 註冊限制 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 10（16-6） |
| 45：密碼不是加密後可還原 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 11（16-7） |
| 46：建立 User 的正確方法 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 12（16-8） |
| 47：`create_user()` 不等於跑過所有 password validators | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 13（16-9） |
| 48：LearnMart RegistrationForm | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 14（16-10） |
| 49：註冊 View 的完整結果 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 15（16-11） |
| 50：Session：跨 request 記住登入狀態 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 16（16-12） |
| 51：為什麼 `request.user` 存在？ | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 17（16-13） |
| 52：`request.user` 的兩種狀態 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 18（16-14） |
| 53：LoginView：使用成熟的內建流程 | 改寫 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 19（16-15） |
| 54：`next`：登入後回到原本目的地 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 20（16-16） |
| 55：Logout 應使用 POST | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 21（16-17） |
| 56：Login redirects 在 settings 定義 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 22（16-18） |
| 57：302、403、404 的身份／權限語意 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 23（16-19） |
| 58：第 2 章概念檢核 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 24（16-20） |
| 59：第 2 章 LearnMart 實作 | 保留 | [第 16 章](10_帳號登入與Session.md#chapter-16)，p. 25（16-21） |
| 60：第 3 章 / Class-based View、Mixin 與物件權限 | 合併 | [第 17 章](11_CRUD與物件權限.md#chapter-17)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 61：先補 Django class 需要的 Python 語法 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 25（13-1） |
| 62：Override：改寫繼承來的方法 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 26（13-2） |
| 63：`super()`：保留父類別既有工作 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 27（13-3） |
| 64：`*args` 與 `**kwargs` 在 Django 常出現 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 28（13-4） |
| 65：Decorator 與 Mixin 的角色 | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 5（17-1） |
| 66：為什麼 URLconf 不能直接放 CBV class？ | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 29（13-5） |
| 67：CBV request 流程簡圖 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 30（13-6） |
| 68：目前 LearnMart ProductListView | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 31（13-7） |
| 69：`get_queryset()` 決定可見資料 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 32（13-8） |
| 70：`get_context_data()` 增加模板需要的資料 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 33（13-9） |
| 71：DetailView：單筆查詢仍可縮小 queryset | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 34（13-10） |
| 72：CreateView：成功表單的 hook | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 15（17-11） |
| 73：`get_absolute_url()` 與成功 redirect | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 9（17-5） |
| 74：三層授權模型 | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 6（17-2） |
| 75：LoginRequiredMixin 要放在 generic view 前 | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 7（17-3） |
| 76：SellerRequiredMixin：角色層 | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 13（17-9） |
| 77：角色正確仍不代表擁有物件 | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 14（17-10） |
| 78：UpdateView 應一開始就是 ownership-safe | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 16（17-12） |
| 79：IDOR：問題不是 ID 可猜，而是存取未被限制 | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 17（17-13） |
| 80：403、404、405 放在不同層 | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 18（17-14） |
| 81：Pagination 也是 CBV 的既有能力 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 35（13-11） |
| 82：CBV 常見錯誤 | 保留 | [第 13 章](07_資料列表搜尋與分頁.md#chapter-13)，p. 36（13-12） |
| 83：第 3 章概念檢核 | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 20（17-16） |
| 84：第 3 章 LearnMart 實作 | 保留 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 21（17-17） |
| 85：第 4 章 / 購物車、POST 操作與第一批流程測試 | 合併 | [第 18 章](12_購物車與流程測試.md#chapter-18)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 86：CartItem 的資料規則 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 6（18-2） |
| 87：Database constraint 防止重複 cart row | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 7（18-3） |
| 88：加入購物車必須是 POST | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 8（18-4） |
| 89：取得 Product 也要限制狀態 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 9（18-5） |
| 90：解析 quantity：瀏覽器限制不是安全規則 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 10（18-6） |
| 91：`get_or_create()` 有兩條路 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 11（18-7） |
| 92：目前累加行為與提示有一個細節 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 12（18-8） |
| 93：Cart 顯示只取目前 user 的資料 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 13（18-9） |
| 94：更新 cart item 先縮小 ownership | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 14（18-10） |
| 95：更新與移除都使用 POST | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 15（18-11） |
| 96：Context processor：每頁都需要 cart count | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 16（18-12） |
| 97：Context processor 必須在 settings 註冊 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 17（18-13） |
| 98：Context processor 的成本也會遍及每頁 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 18（18-14） |
| 99：Mutation route matrix（1／2） | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 19（18-15） |
| 100：Mutation route matrix（2／2） | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 20（18-16） |
| 101：開始寫流程測試：Arrange–Act–Assert | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 21（18-17） |
| 102：`TestCase` 與真實 transaction 測試 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 22（18-18） |
| 103：`setUp()` 每個 test method 前執行 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 23（18-19） |
| 104：測試匿名 cart redirect | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 24（18-20） |
| 105：測試 client 預設不強制 CSRF | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 25（18-21） |
| 106：測試登入後的 database state | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 26（18-22） |
| 107：`login()` 與 `force_login()` | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 27（18-23） |
| 108：第 4 章概念檢核 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 28（18-24） |
| 109：第 4 章 LearnMart 實作 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 29（18-25） |
| 110：第 5 章 / 訂單、結帳、Transaction 與鎖定 | 合併 | [第 19 章](13_訂單結帳與交易.md#chapter-19)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 111：為什麼需要 Order 與 OrderItem？ | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 5（19-1） |
| 112：Order 保存交易層資訊 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 6（19-2） |
| 113：OrderItem 為什麼同時有 FK 與快照？ | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 7（19-3） |
| 114：訂單總額也由伺服器保存快照 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 8（19-4） |
| 115：CheckoutForm 的 allowlist | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 9（19-5） |
| 116：Checkout 的入口先處理身份與 cart | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 10（19-6） |
| 117：`list(queryset)` 讓查詢立即執行 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 11（19-7） |
| 118：GET 與 POST 在 checkout 扮演不同角色 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 12（19-8） |
| 119：POST 先建立 bound CheckoutForm | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 13（19-9） |
| 120：寫入前再次檢查庫存 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 14（19-10） |
| 121：`commit=False` 補上 buyer 與 total | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 15（19-11） |
| 122：建立 OrderItem 快照 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 16（19-12） |
| 123：扣庫存並清 cart | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 17（19-13） |
| 124：最後 redirect 到 buyer-scoped 訂單 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 18（19-14） |
| 125：`transaction.atomic` 的核心保證 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 19（19-15） |
| 126：圖解：Checkout 的成功路徑與 rollback 路徑 | 改寫 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 20（19-16） |
| 127：為什麼 validation 要盡量在寫入前？ | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 21（19-17） |
| 128：Atomicity 與 locking 是不同問題 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 22（19-18） |
| 129：`select_for_update()` 的意圖與範圍 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 23（19-19） |
| 130：SQLite 不提供這個 row-lock 保證 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 24（19-20） |
| 131：優先明確鎖定 Product | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 25（19-21） |
| 132：Buyer 只能看自己的 Order | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 26（19-22） |
| 133：Snapshot template 不依賴目前 Product 名稱／價格 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 27（19-23） |
| 134：目前 checkout test 已保護哪些行為？ | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 28（19-24） |
| 135：Order privacy test 是 IDOR regression test | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 29（19-25） |
| 136：第 5 章概念檢核 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 30（19-26） |
| 137：第 5 章 LearnMart 實作 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 31（19-27） |
| 138：第 6 章 / 賣家出貨、評價與多方交易限制 | 合併 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 139：Seller 如何找到有自己商品的訂單？ | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 5（20-1） |
| 140：Seller order list 還有一個 N+1 觀察點 | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 6（20-2） |
| 141：出貨操作的四層檢查 | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 7（20-3） |
| 142：目前只實作 PENDING → SHIPPED | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 8（20-4） |
| 143：狀態轉換要定義五件事 | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 9（20-5） |
| 144：多賣家訂單的核心限制 | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 10（20-6） |
| 145：限制還會影響 Review | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 11（20-7） |
| 146：Review 規則要分層描述 | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 12（20-8） |
| 147：Eligibility 在 View 查詢 | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 13（20-9） |
| 148：Rating 1–5 由 validators／form 驗證 | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 14（20-10） |
| 149：每人每商品一列由 database unique constraint | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 15（20-11） |
| 150：`update_or_create()` 讓重送變成編輯 | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 16（20-12） |
| 151：評價輸出仍需 template escaping | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 17（20-13） |
| 152：出貨與 Review 應有哪些測試？ | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 18（20-14） |
| 153：第 6 章概念檢核 | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 19（20-15） |
| 154：第 6 章 LearnMart 實作 | 保留 | [第 20 章](14_出貨評價與狀態規則.md#chapter-20)，p. 20（20-16） |
| 155：第 7 章 / 安全與回歸測試整合 | 合併 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 156：安全不是最後才加的一頁 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 5（21-1） |
| 157：Trust boundary 地圖 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 6（21-2） |
| 158：圖解：信任邊界與五層伺服器防線 | 改寫 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 7（21-3） |
| 159：XSS：Template autoescaping 的邊界 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 8（21-4） |
| 160：Raw HttpResponse 不會套 Template autoescaping | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 9（21-5） |
| 161：BoardPost 是 stored XSS 的實際觀察點 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 10（21-6） |
| 162：SQL injection：ORM value 會參數化 / 危險示意，不要用 f-string 拼接 user input | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 11（21-7） |
| 163：Dynamic field name 仍需要 allowlist | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 12（21-8） |
| 164：CSRF、Login、Role、Ownership 不可互相替代 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 13（21-9） |
| 165：Upload：ImageField 不是完整安全策略 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 14（21-10） |
| 166：開發 settings 不等於 production baseline | 保留 | [第 22 章](16_部署設定與正式環境.md#chapter-22)，p. 17（22-13） |
| 167：`check` 與 `check --deploy` 不同 | 保留 | [第 24 章](16_部署設定與正式環境.md#chapter-24)，p. 39（24-8） |
| 168：現有六個測試保護什麼？ | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 15（21-11） |
| 169：測試矩陣：一個 workflow 至少看五面 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 16（21-12） |
| 170：Response 與 database assertion 都重要 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 17（21-13） |
| 171：`refresh_from_db()` 避免看舊 object | 合併 | [第 18 章](12_購物車與流程測試.md#chapter-18)；refresh_from_db 併入資料庫狀態驗證 |
| 172：Rollback test 要讓失敗發生在寫入之後 | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 32（19-28） |
| 173：一次跑完整與單一測試 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 18（21-14） |
| 174：Migration drift 不是 behavior test | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 19（21-15） |
| 175：Security regression 的優先順序 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 20（21-16） |
| 176：課堂版與正式商城的界線 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 21（21-17） |
| 177：第 7 章概念檢核 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 22（21-18） |
| 178：第 7 章 LearnMart 實作 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 23（21-19） |
| 179：空白頁 | 合併 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)；移除連續分隔線造成的空白頁 |
| 180：LearnBoard 對照實作 / 表單與 server-owned author | 改寫 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 8（17-4） |
| 181：LearnBoard 對照實作 / 兩種 ownership 防線 | 改寫 | [第 17 章](11_CRUD與物件權限.md#chapter-17)，p. 10（17-6） |
| 182：LearnBoard 對照實作 / 測試矩陣如何遷移到商城？ | 改寫 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 34（18-30） |
| 183：全冊整合：兩個專案的兩條旅程 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 24（21-20） |
| 184：你現在應該能回答 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 25（21-21） |
| 185：建議驗證命令 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 26（21-22） |
| 186：Django 02 補充 Lab / 從 HTML Form 到 Database Change | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 187：1. POST flow 先畫出來 | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 30（15-26） |
| 188：2. HTML 有欄位，不代表 server 信任它 | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；HTML 欄位信任邊界併入 request.POST／fields 白名單 |
| 189：3. 先觀察 request.POST | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 31（15-27） |
| 190：4. Form lifecycle 要會逐步問 | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；表單生命週期併入 bound／is_valid／錯誤回顯 |
| 191：5. 驗證錯誤不等於 exception | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 32（15-28） |
| 192：6. CSRF 失敗時先看哪裡？ | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 33（15-29） |
| 193：7. Browser DevTools 是表單 debugger | 保留 | [第 15 章](09_表單與資料驗證.md#chapter-15)，p. 34（15-30） |
| 194：8. PRG：為什麼成功後 redirect？ | 合併 | [第 15 章](09_表單與資料驗證.md#chapter-15)；PRG 解釋併入成功 POST 後 redirect |
| 195：9. LoginRequired：302 不一定是錯 | 合併 | [第 16 章](10_帳號登入與Session.md#chapter-16)；登入轉址併入 next 與身份狀態碼 |
| 196：10. `request.user` 從哪裡來？ | 合併 | [第 16 章](10_帳號登入與Session.md#chapter-16)；request.user 來源併入 session／middleware |
| 197：11. Authentication ≠ Authorization | 合併 | [第 16 章](10_帳號登入與Session.md#chapter-16)；身份與授權差異併入帳號章開場 |
| 198：12. 403 與 404 的教學差別 | 合併 | [第 17 章](11_CRUD與物件權限.md#chapter-17)；403／404 併入物件擁有權與回應語意 |
| 199：13. 測試的 Arrange / Act / Assert / Arrange | 合併 | [第 18 章](12_購物車與流程測試.md#chapter-18)；AAA 併入開始寫流程測試 |
| 200：14. `self.client.login` vs `force_login` | 合併 | [第 18 章](12_購物車與流程測試.md#chapter-18)；login／force_login 併入測試登入方法 |
| 201：15. 每個重要 POST 至少驗證兩件事 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 30（18-26） |
| 202：16. `refresh_from_db()` 為什麼重要？ | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 31（18-27） |
| 203：17. Transaction 測試要驗證 rollback | 保留 | [第 19 章](13_訂單結帳與交易.md#chapter-19)，p. 33（19-29） |
| 204：18. 單支測試定位 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 32（18-28） |
| 205：19. Test failure 常見類型 | 保留 | [第 18 章](12_購物車與流程測試.md#chapter-18)，p. 33（18-29） |
| 206：20. 安全測試不是「掃描器章節」 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 27（21-23） |
| 207：21. 每個 lab 的最終 checklist | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 28（21-24） |
| 208：下一步 | 保留 | [第 21 章](15_安全與回歸測試整合.md#chapter-21)，p. 29（21-25） |
| 209：Django Template Language / 實用工具箱 | 合併 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 210：DTL 的定位 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 6（14-2） |
| 211：Filter 可以串接 | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 18（4-14） |
| 212：`default` vs `default_if_none` | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 19（4-15） |
| 213：日期格式 `date` | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 20（4-16） |
| 214：只顯示時間：`time` | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 21（4-17） |
| 215：相對時間：`timesince` | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 7（14-3） |
| 216：未來還有多久：`timeuntil` | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 8（14-4） |
| 217：Template 裡取得現在時間：`{% now %}` | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 9（14-5） |
| 218：更自然的時間：`humanize` | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 10（14-6） |
| 219：大數字：`intcomma` / `intword` | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 11（14-7） |
| 220：長文字：`truncatechars` | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 22（4-18） |
| 221：長文字：`truncatewords` | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 23（4-19） |
| 222：HTML 截斷版本要小心 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 12（14-8） |
| 223：純文字換行：`linebreaks` | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 24（4-20） |
| 224：檔案大小：`filesizeformat` | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 13（14-9） |
| 225：小數格式：`floatformat` | 保留 | [第 4 章](03_Template與頁面呈現.md#chapter-4)，p. 25（4-21） |
| 226：`length` / `wordcount` | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 14（14-10） |
| 227：List helpers | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 15（14-11） |
| 228：`dictsort` | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 16（14-12） |
| 229：`yesno` | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 17（14-13） |
| 230：`pluralize` | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 18（14-14） |
| 231：`urlize` / `urlizetrunc` | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 19（14-15） |
| 232：`{% with %}`：替長 lookup 取名字 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 20（14-16） |
| 233：`{% firstof %}`：多個 fallback | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 21（14-17） |
| 234：`{% cycle %}`：輪流值 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 22（14-18） |
| 235：`{% ifchanged %}`：分組顯示 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 23（14-19） |
| 236：`{% regroup %}`：Template 層分組 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 24（14-20） |
| 237：`{% querystring %}`：分頁超實用 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 25（14-21） |
| 238：搜尋＋分頁的典型寫法 | 改寫 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 26（14-22） |
| 239：`url` tag：不要手拼路徑 | 合併 | [第 4 章](03_Template與頁面呈現.md#chapter-4)；url tag 併入命名路由與 Template 基礎 |
| 240：`json_script`：安全把資料交給 JS | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 27（14-23） |
| 241：Autoescape 是預設安全線 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 28（14-24） |
| 242：`safe` 要非常克制 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 29（14-25） |
| 243：`striptags／safe` 不是 sanitizer | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 30（14-26） |
| 244：Template 裡不要呼叫帶參數方法 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 31（14-27） |
| 245：什麼時候做 custom filter？ | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 32（14-28） |
| 246：什麼時候做 inclusion tag？ | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 33（14-29） |
| 247：LearnBoard 可以立刻用的補強 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 34（14-30） |
| 248：LearnMart 可以立刻用的補強 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 35（14-31） |
| 249：LearnJournal 可以立刻用的補強 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 36（14-32） |
| 250：判斷「該放哪一層」 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 37（14-33） |
| 251：本章實作題 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 38（14-34） |
| 252：參考資料 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 39（14-35） |
| 253：最後記住三件事 | 保留 | [第 14 章](08_DTL進階與元件整理.md#chapter-14)，p. 40（14-36） |

## D0：原始 00_overview.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：03 Deployment / Operations / 從「本機可跑」到「可部署、可維護」 | 合併 | [第 22 章](16_部署設定與正式環境.md#chapter-22)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：為什麼做成共用單元？ | 保留 | [第 22 章](16_部署設定與正式環境.md#chapter-22)，p. 5（22-1） |
| 3：本機與 production 的差別 | 保留 | [第 22 章](16_部署設定與正式環境.md#chapter-22)，p. 6（22-2） |
| 4：這個單元不綁供應商 | 保留 | [第 22 章](16_部署設定與正式環境.md#chapter-22)，p. 7（22-3） |
| 5：建議順序 | 合併 | [第 22 章](16_部署設定與正式環境.md#chapter-22)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 6：配套手冊 | 合併 | [第 22 章](16_部署設定與正式環境.md#chapter-22)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |

## D1：原始 01_settings_and_environment.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：P2-1 Settings / Environment Variables | 合併 | [第 22 章](16_部署設定與正式環境.md#chapter-22)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：哪些值不該硬編碼？ | 保留 | [第 22 章](16_部署設定與正式環境.md#chapter-22)，p. 9（22-5） |
| 3：Classroom default vs production override | 保留 | [第 22 章](16_部署設定與正式環境.md#chapter-22)，p. 10（22-6） |
| 4：讀環境變數 | 保留 | [第 22 章](16_部署設定與正式環境.md#chapter-22)，p. 12（22-8） |
| 5：不要提交 `.env` | 保留 | [第 22 章](16_部署設定與正式環境.md#chapter-22)，p. 13（22-9） |
| 6：ALLOWED_HOSTS | 保留 | [第 22 章](16_部署設定與正式環境.md#chapter-22)，p. 14（22-10） |
| 7：Settings split 要不要做？ | 保留 | [第 22 章](16_部署設定與正式環境.md#chapter-22)，p. 15（22-11） |
| 8：本章檢核 | 保留 | [第 22 章](16_部署設定與正式環境.md#chapter-22)，p. 16（22-12） |

## D2：原始 02_static_media_database.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：P2-2 Static / Media / Database | 合併 | [第 23 章](16_部署設定與正式環境.md#chapter-23)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：`runserver` 幫你做了很多事 | 保留 | [第 23 章](16_部署設定與正式環境.md#chapter-23)，p. 21（23-1） |
| 3：`collectstatic` | 保留 | [第 23 章](16_部署設定與正式環境.md#chapter-23)，p. 22（23-2） |
| 4：Media 不等於 Static | 保留 | [第 23 章](16_部署設定與正式環境.md#chapter-23)，p. 23（23-3） |
| 5：上傳安全 | 保留 | [第 23 章](16_部署設定與正式環境.md#chapter-23)，p. 24（23-4） |
| 6：SQLite 到 PostgreSQL | 保留 | [第 23 章](16_部署設定與正式環境.md#chapter-23)，p. 25（23-5） |
| 7：切 DB 不等於搬資料 | 保留 | [第 23 章](16_部署設定與正式環境.md#chapter-23)，p. 26（23-6） |
| 8：`dumpdata` / `loaddata` 的定位 | 保留 | [第 23 章](16_部署設定與正式環境.md#chapter-23)，p. 27（23-7） |
| 9：本章檢核 | 保留 | [第 23 章](16_部署設定與正式環境.md#chapter-23)，p. 28（23-8） |

## D3：原始 03_security_and_check_deploy.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：P2-3 Security / `check --deploy` | 合併 | [第 24 章](16_部署設定與正式環境.md#chapter-24)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：先跑 Django 自己的檢查 | 保留 | [第 24 章](16_部署設定與正式環境.md#chapter-24)，p. 32（24-1） |
| 3：DEBUG 必須關 | 保留 | [第 24 章](16_部署設定與正式環境.md#chapter-24)，p. 33（24-2） |
| 4：HTTPS 與 secure cookies | 保留 | [第 24 章](16_部署設定與正式環境.md#chapter-24)，p. 34（24-3） |
| 5：CSRF / XSS / Clickjacking | 保留 | [第 24 章](16_部署設定與正式環境.md#chapter-24)，p. 35（24-4） |
| 6：Security headers | 保留 | [第 24 章](16_部署設定與正式環境.md#chapter-24)，p. 36（24-5） |
| 7：Rate limiting / brute force | 保留 | [第 24 章](16_部署設定與正式環境.md#chapter-24)，p. 37（24-6） |
| 8：本章檢核 | 保留 | [第 24 章](16_部署設定與正式環境.md#chapter-24)，p. 38（24-7） |

## D4：原始 04_process_proxy_logging.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：P2-4 Process / Reverse Proxy / Logging | 合併 | [第 25 章](17_服務運行與發布維護.md#chapter-25)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：Production request path | 保留 | [第 25 章](17_服務運行與發布維護.md#chapter-25)，p. 5（25-1） |
| 3：Reverse proxy 常做什麼？ | 保留 | [第 25 章](17_服務運行與發布維護.md#chapter-25)，p. 6（25-2） |
| 4：WSGI / ASGI server | 保留 | [第 25 章](17_服務運行與發布維護.md#chapter-25)，p. 7（25-3） |
| 5：Process manager 要解決什麼？ | 保留 | [第 25 章](17_服務運行與發布維護.md#chapter-25)，p. 8（25-4） |
| 6：Log 不只 `print()` | 保留 | [第 25 章](17_服務運行與發布維護.md#chapter-25)，p. 9（25-5） |
| 7：Django logging 心智模型 | 保留 | [第 25 章](17_服務運行與發布維護.md#chapter-25)，p. 10（25-6） |
| 8：可觀測性 | 保留 | [第 25 章](17_服務運行與發布維護.md#chapter-25)，p. 11（25-7） |
| 9：Health check | 保留 | [第 25 章](17_服務運行與發布維護.md#chapter-25)，p. 12（25-8） |
| 10：本章檢核 | 保留 | [第 25 章](17_服務運行與發布維護.md#chapter-25)，p. 13（25-9） |

## D5：原始 05_migrations_backup_recovery.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：P2-5 Migrations / Backup / Recovery | 合併 | [第 26 章](17_服務運行與發布維護.md#chapter-26)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：先備回顧：資料模型與檔案 | 保留 | [第 26 章](17_服務運行與發布維護.md#chapter-26)，p. 17（26-1） |
| 3：Migration 是版本化 schema 變更 | 保留 | [第 26 章](17_服務運行與發布維護.md#chapter-26)，p. 18（26-2） |
| 4：Deploy 順序要能相容 | 保留 | [第 26 章](17_服務運行與發布維護.md#chapter-26)，p. 19（26-3） |
| 5：Data migration 也會失敗 | 保留 | [第 26 章](17_服務運行與發布維護.md#chapter-26)，p. 20（26-4） |
| 6：Backup 的最低標準 | 保留 | [第 26 章](17_服務運行與發布維護.md#chapter-26)，p. 21（26-5） |
| 7：RPO / RTO | 保留 | [第 26 章](17_服務運行與發布維護.md#chapter-26)，p. 22（26-6） |
| 8：Rollback 不只是 git revert | 保留 | [第 26 章](17_服務運行與發布維護.md#chapter-26)，p. 23（26-7） |
| 9：Classroom recovery drill / 做一個破壞性操作 | 保留 | [第 26 章](17_服務運行與發布維護.md#chapter-26)，p. 24（26-8） |
| 10：本章檢核 | 保留 | [第 26 章](17_服務運行與發布維護.md#chapter-26)，p. 25（26-9） |

## D6：原始 06_ci_and_release_checklist.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：P2-6 CI / Release Checklist | 合併 | [第 27 章](17_服務運行與發布維護.md#chapter-27)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：最小 CI gate | 保留 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 29（27-1） |
| 3：為什麼 `makemigrations --check`？ | 保留 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 30（27-2） |
| 4：CI 不應保存 production secrets | 保留 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 31（27-3） |
| 5：Release 前 checklist | 保留 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 32（27-4） |
| 6：Release 後驗證 | 保留 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 33（27-5） |
| 7：監看 deployment | 保留 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 34（27-6） |
| 8：Roll forward vs rollback | 保留 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 35（27-7） |
| 9：本章檢核 | 保留 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 36（27-8） |

## D7：原始 07_summary.md（已整合移除）

| 原頁／標題 | 處理 | 新位置／原因 |
|---|---|---|
| 1：Deployment / Operations Summary | 合併 | [第 27 章](17_服務運行與發布維護.md#chapter-27)；原封面／課程導覽改寫為新章首、README 與每份先備／驗收／銜接 |
| 2：Production readiness 地圖 | 保留 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 37（27-9） |
| 3：三個專案各自回扣 | 改寫 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 38（27-10） |
| 4：最後驗證 | 保留 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 39（27-11） |
| 5：完成這門課後應具備的能力 | 改寫 | [第 27 章](17_服務運行與發布維護.md#chapter-27)，p. 40（27-12） |
