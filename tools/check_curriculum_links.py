#!/usr/bin/env python3
"""Validate local curriculum links and common Marp command examples.

This script intentionally uses only the Python standard library so it can run
in a fresh GitHub Actions runner without installing the Django projects.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
MARP_COMMAND_RE = re.compile(r"(?:^|\s)marp\s+([^\s]+\.md)(?:\s|$)")

# These are the stable entry points advertised to students and instructors.
# If a curriculum refactor moves one, update documentation and this manifest
# in the same change so CI makes the navigation decision explicit.
REQUIRED_PATHS = [
    "README.md",
    "slides/README.md",
    "slides/SOURCE_MAP.md",
    "slides/00_python_syntax_essentials/00_python_syntax_essentials.md",
    "slides/00_html_css_page_basics/00_html_css_page_basics.md",
    "slides/01_django_foundations_and_two_projects/01_django_foundations_and_two_projects.md",
    "slides/02_forms_auth_and_two_projects/00_overview.md",
    "slides/learnboard_01_django_foundations_and_message_board/00_overview.md",
    "slides/learnboard_02_forms_auth_and_board_workflows/00_overview.md",
    "slides/learnmart_01_django_foundations_and_data_backed_catalog/00_overview.md",
    "slides/learnmart_02_forms_auth_and_marketplace_workflows/00_overview.md",
    "slides/learnjournal_01_content_model_and_publishing/00_overview.md",
    "slides/workbooks/learnboard_01_django_foundations_and_message_board_workbook.md",
    "slides/workbooks/learnboard_02_forms_auth_and_board_workflows_workbook.md",
    "slides/workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md",
    "slides/workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md",
    "slides/workbooks/learnjournal_01_content_model_and_publishing_workbook.md",
]

SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:")


def clean_target(raw: str) -> str | None:
    target = raw.strip().strip("<>")
    # Markdown links may contain an optional title after whitespace. Curriculum
    # links in this repository do not rely on spaces in filenames.
    target = target.split(maxsplit=1)[0]
    if not target or target.startswith("#") or target.startswith(SKIP_SCHEMES):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    return target or None


def resolve_target(source: Path, target: str) -> Path:
    if target.startswith("/"):
        return ROOT / target.lstrip("/")
    return source.parent / target


def check_markdown_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    for match in MARKDOWN_LINK_RE.finditer(text):
        target = clean_target(match.group(1))
        if target is None:
            continue
        resolved = resolve_target(path, target)
        if not resolved.exists():
            rel = path.relative_to(ROOT)
            errors.append(f"{rel}: broken Markdown link -> {target}")

    # Catch command examples such as `marp ../slides/.../01_chapter_01.md --pdf`.
    # Resolve them from the directory containing the Markdown document, which is
    # how the surrounding README instructions are written in this repository.
    for match in MARP_COMMAND_RE.finditer(text):
        target = clean_target(match.group(1).strip("'\"`"))
        if target is None:
            continue
        resolved = resolve_target(path, target)
        if not resolved.exists():
            rel = path.relative_to(ROOT)
            errors.append(f"{rel}: Marp example points to missing file -> {target}")

    return errors


def main() -> int:
    errors: list[str] = []

    for required in REQUIRED_PATHS:
        if not (ROOT / required).exists():
            errors.append(f"required curriculum entry point is missing: {required}")

    markdown_files = sorted(
        path for path in ROOT.rglob("*.md") if ".git" not in path.parts and ".venv" not in path.parts
    )
    for path in markdown_files:
        errors.extend(check_markdown_file(path))

    if errors:
        print("Curriculum link check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Curriculum link check passed ({len(markdown_files)} Markdown files checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
