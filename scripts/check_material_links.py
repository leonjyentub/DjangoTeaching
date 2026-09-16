#!/usr/bin/env python3
"""Check local links in Markdown teaching materials.

This checker intentionally uses only the Python standard library so it can run
locally and in GitHub Actions without installing extra packages.

It validates Markdown links/images that point to repository-local files or
folders. External URLs, mailto links and in-page anchors are ignored.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "data"}
DEFAULT_EXCLUDES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "output",
    "__pycache__",
}


@dataclass(frozen=True)
class BrokenLink:
    source: Path
    line: int
    target: str
    resolved: Path


def strip_optional_title(raw_target: str) -> str:
    """Return the destination portion from `(path "optional title")`.

    Angle-bracket destinations may contain spaces. For ordinary Markdown links
    we split on the first whitespace because repository paths in this project do
    not intentionally contain spaces.
    """

    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split(maxsplit=1)[0] if target else ""


def is_local_destination(destination: str) -> bool:
    if not destination or destination.startswith("#"):
        return False
    parsed = urlsplit(destination)
    if parsed.scheme.lower() in SKIP_SCHEMES or parsed.netloc:
        return False
    return True


def resolve_destination(source: Path, destination: str, root: Path) -> Path:
    parsed = urlsplit(destination)
    decoded_path = unquote(parsed.path)
    if decoded_path.startswith("/"):
        return (root / decoded_path.lstrip("/")).resolve()
    return (source.parent / decoded_path).resolve()


def target_exists(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    if path.exists():
        return True
    # Treat a directory-style Markdown link as valid if it resolves to a
    # conventional README/index file. This mirrors GitHub's browsing behavior.
    if path.suffix == "":
        return (path / "README.md").exists() or (path / "index.md").exists()
    return False


def iter_markdown_files(root: Path, excludes: set[str]):
    for path in root.rglob("*.md"):
        if any(part in excludes for part in path.relative_to(root).parts):
            continue
        yield path


def check_file(path: Path, root: Path) -> list[BrokenLink]:
    broken: list[BrokenLink] = []
    in_fence = False
    fence_marker = ""

    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            continue
        if in_fence:
            continue

        for match in LINK_RE.finditer(line):
            destination = strip_optional_title(match.group(1))
            if not is_local_destination(destination):
                continue
            resolved = resolve_destination(path, destination, root)
            if not target_exists(resolved, root):
                broken.append(BrokenLink(path, line_no, destination, resolved))

    return broken


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Directory name to skip; can be specified more than once.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    excludes = DEFAULT_EXCLUDES | set(args.exclude)
    markdown_files = sorted(iter_markdown_files(root, excludes))
    broken: list[BrokenLink] = []

    for path in markdown_files:
        broken.extend(check_file(path, root))

    if broken:
        print(f"Found {len(broken)} broken local Markdown link(s):")
        for item in broken:
            source = item.source.relative_to(root)
            try:
                resolved = item.resolved.relative_to(root)
            except ValueError:
                resolved = item.resolved
            print(f"- {source}:{item.line}: {item.target!r} -> {resolved}")
        return 1

    print(f"OK: checked {len(markdown_files)} Markdown file(s); no broken local links found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
