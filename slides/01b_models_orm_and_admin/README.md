# Django 01B：資料模型、ORM 與 Django Admin

主教材：[01b_models_orm_and_admin.md](01b_models_orm_and_admin.md)，共 104 頁（含封面）。沿用 `django-teal`、16:9、可編輯 Marp；不需要先讀懂 LearnBoard 或 LearnMart 才能開始。

## 閱讀順序與定位

建議在 [01 共通基礎](../01_django_foundations_and_two_projects/01_django_foundations_and_two_projects.md) 第 3 章後使用。先完成本冊從空目錄開始的 catalog 練習，再學詳細觀念與專案對照。原 01 第 4～5 章保留為摘要複習，回到第 6～7 章組合頁面；後續讀 [02 表單與工作流程](../02_forms_auth_and_two_projects/02_forms_auth_and_two_projects.md)、[03 migration 與備份](../03_deployment_and_operations/05_migrations_backup_recovery.md)。

Django 概念是主線，LearnBoard／LearnMart 是具體案例，不以兩個專案用到的功能限制教學範圍。原專案教材保留，方便回查；本冊抽取相關內容後重新拆解、補上解釋與練習，並非刪除或搬走原檔。

## 內容索引

| 章節 | 內容 | 初學者應能完成 |
|---|---|---|
| 0 | 獨立練習專案、完整 Category／Product、migration、shell、Admin、media | 從空目錄到第一筆可管理的資料 |
| 1 | Model 對應、pk／id、自訂主鍵、unique、複合唯一 | 分辨身分與業務唯一規則 |
| 2 | 文字、數字、真假、時間、slug、圖片、參數與驗證 | 按需求選型別並解釋空值／預設值 |
| 3 | FK、一對一、多對多、正反向查詢、on_delete、through | 說明兩個方向的數量與回傳型別 |
| 4 | Model.Meta／ModelForm.Meta／ModelAdmin、排序、索引、約束、migration | 知道規則放哪裡、如何套用 |
| 5 | CRUD、lookup、Q、排序、切片、values、lazy、預載、聚合 | 組合查詢並觀察結果與成本 |
| 6 | Admin 註冊、列表、搜尋、篩選、編輯、唯讀、Inline、權限、UserAdmin、action | 管理資料並驗證不同帳號的權限 |
| 7 | 關聯實作、綜合驗收、離堂檢核、官方來源 | 以可觀察結果解釋設計 |

初次授課先完成基本必學頁；索引、through、原子更新、物件權限客製與 action 均標為進階。第 0 章可分段穿插第 1～4 章，不要求初學者先記住所有參數。

## 案例抽入與擴充對照

| 原始來源 | 抽入／擴充的位置 | 處理方式 |
|---|---|---|
| [LearnBoard 01 第 4 章](../learnboard_01_django_foundations_and_message_board/04_chapter_04.md) | 2-4、2-11、3-2～3-4、4-9、6-4 | 文字、時間、可空作者、SET_NULL、migration 與留言 Admin 分頁解釋 |
| [LearnMart 01 第 3 章](../learnmart_01_django_foundations_and_data_backed_catalog/03_chapter_03.md) | 2-16 | 有圖／無圖、url 存取與顯示邊界 |
| [LearnMart 01 第 4 章](../learnmart_01_django_foundations_and_data_backed_catalog/04_chapter_04.md) | 2-15、3-4、3-11 | 圖片 storage、關聯保護與訂單歷史 |
| [LearnMart 01 第 5 章](../learnmart_01_django_foundations_and_data_backed_catalog/05_chapter_05.md) | 1-6、3-11、4-4、5-8、5-11 | 購物車／評價唯一性、快照、列表與詳情預載 |
| [LearnBoard models.py](../../learnboard/board/models.py)／[admin.py](../../learnboard/board/admin.py) | 2-4、3-2、6-4 | 依現有程式確認節錄與解釋 |
| [LearnMart models.py](../../learnmart/marketplace/models.py)／[admin.py](../../learnmart/marketplace/admin.py) | Category／Product／CartItem／OrderItem 與第 6 章 | 區分現有實作、刪節片段與新增教學設計 |

Profile、Tag、ProductTag、UUID 主鍵、CheckConstraint、索引、進階 Admin 設定是新增教學範例，不宣稱已存在於兩個專案。既有 auth 的 Group／permissions 自身含多對多，與業務 models 沒宣告 Tag 的敘述不衝突。

## 範例操作約定

- 第 0 章 `catalog` 是獨立、完整的最小練習；後面 `marketplace`／`board` 範例需切到對應專案。
- 每段都有模型名稱與用途。完整類別可照步驟建立；「節錄」只呈現該頁概念，不是可整檔覆蓋的程式。
- 第 3 章 Profile／Tag 放進 LearnMart 的新 `practice` app；第 7 章給出安裝與 migration 路線。
- 自動 M2M 與 `through` 是兩種 schema 版本；不要直接覆寫已有關係資料。
- 原始教學專案的程式、資料庫與 migration 不因本次教材修改而變更。

## 官方依據

以專案宣告的 Django 6.1 系列為文件基準。每頁的 Marp speaker notes 附主題文件，最後兩頁提供可點擊的官方參考。

- [Models](https://docs.djangoproject.com/en/6.1/topics/db/models/)
- [Model fields](https://docs.djangoproject.com/en/6.1/ref/models/fields/)
- [Model Meta](https://docs.djangoproject.com/en/6.1/ref/models/options/)
- [Constraints](https://docs.djangoproject.com/en/6.1/ref/models/constraints/)
- [Queries](https://docs.djangoproject.com/en/6.1/topics/db/queries/)
- [Model instances](https://docs.djangoproject.com/en/6.1/ref/models/instances/)
- [Many-to-many](https://docs.djangoproject.com/en/6.1/topics/db/examples/many_to_many/)
- [Time zones](https://docs.djangoproject.com/en/6.1/topics/i18n/timezones/)
- [File uploads](https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/)
- [Admin](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/)
- [Admin actions](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/actions/)
- [Authentication and permissions](https://docs.djangoproject.com/en/6.1/topics/auth/default/)
