/**
 * Marp CLI 全案共用設定
 * 用於在終端機執行 `npx @marp-team/marp-cli --pdf ...` 時自動載入專屬主題
 */
export default {
  themeSet: 'slides/themes/django-teal.css',
  allowLocalFiles: true,
  pdf: {
    printBackground: true,
  },
}
