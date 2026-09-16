from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_SUFFIXES = {".md", ".py", ".toml", ".yml", ".yaml", ".txt"}
FORBIDDEN = {
    "Django 5.2": "use the Django 6.1.1 teaching baseline",
    "Python 3.13": "use the Python 3.14.7 teaching baseline",
    "django>=5.2": "use django>=6.1.1,<6.2",
    "docs.djangoproject.com/en/5.2": "link to Django 6.1 documentation",
    'python-version: "3.13"': 'use python-version: "3.14.7"',
}

errors: list[str] = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
        continue
    if ".git" in path.parts or "migrations" in path.parts:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for needle, guidance in FORBIDDEN.items():
        if needle in text:
            errors.append(f"{path.relative_to(ROOT)}: found {needle!r}; {guidance}")

if errors:
    print("Version baseline check failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("Version baseline check passed: Django 6.1.1 / Python 3.14.7 references are current.")
