from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS = {
    ROOT / "slides/workbooks/learnboard_01_django_foundations_and_message_board_workbook.md": (
        "大於等於 5.2 且小於 5.3 的版本，例如 5.2、5.2.1。不接受 5.1.x，也不接受 5.3.0。實際安裝哪個精確版本由 `uv.lock` 決定。",
        "大於等於 6.1.1 且小於 6.2 的版本，例如 6.1.1、6.1.2。不接受 6.0.x，也不接受 6.2.0。實際安裝哪個精確版本由 `uv.lock` 決定。",
    ),
    ROOT / "slides/workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md": (
        "同時符合大於等於 5.2 且小於 5.3 的版本，例如 5.2、5.2.1、5.2.9。它不接受 5.1.x，也不接受 5.3.0。實際安裝哪個精確版本再由 `uv.lock` 決定。",
        "同時符合大於等於 6.1.1 且小於 6.2 的版本，例如 6.1.1、6.1.2。它不接受 6.0.x，也不接受 6.2.0。實際安裝哪個精確版本再由 `uv.lock` 決定。",
    ),
}

for path, (old, new) in REPLACEMENTS.items():
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"Expected stale version explanation not found: {path}")
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"fixed: {path.relative_to(ROOT)}")

# This is a one-off migration helper; remove it in the same generated commit.
Path(__file__).unlink()
