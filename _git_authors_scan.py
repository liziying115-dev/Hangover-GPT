#!/usr/bin/env python3
"""Walk git commit chain from HEAD and print unique author/committer identities."""
from __future__ import annotations

import re
import subprocess
import zlib
from pathlib import Path

REPO = Path(__file__).resolve().parent
GIT_DIR = REPO / ".git"


def read_commit(sha: str) -> str | None:
    """Return decompressed commit body (after header line) or None."""
    if len(sha) != 40:
        return None
    obj_path = GIT_DIR / "objects" / sha[:2] / sha[2:]
    if not obj_path.is_file():
        return None
    raw = obj_path.read_bytes()
    data = zlib.decompress(raw)
    if not data.startswith(b"commit "):
        return None
    null = data.index(b"\0")
    return data[null + 1 :].decode("utf-8", errors="replace")


def parent_shas(body: str) -> list[str]:
    parents: list[str] = []
    for line in body.splitlines():
        if line.startswith("parent "):
            parents.append(line.split()[1])
    return parents


def main() -> None:
    head = (GIT_DIR / "refs" / "heads" / "main").read_text().strip()
    seen: set[str] = set()
    stack = [head]
    authors: set[str] = set()
    committers: set[str] = set()

    while stack:
        sha = stack.pop()
        if sha in seen:
            continue
        seen.add(sha)
        body = read_commit(sha)
        if body is None:
            # Try git cat-file if object is packed (not in loose store)
            try:
                out = subprocess.check_output(
                    ["git", "-C", str(REPO), "cat-file", "-p", sha],
                    stderr=subprocess.DEVNULL,
                )
                body = out.decode("utf-8", errors="replace")
            except (OSError, subprocess.CalledProcessError):
                continue
        for line in body.splitlines():
            if line.startswith("author "):
                authors.add(line[len("author ") :])
            elif line.startswith("committer "):
                committers.add(line[len("committer ") :])
        for p in parent_shas(body):
            stack.append(p)

    out_path = REPO / "_git_authors_result.txt"
    lines = ["=== Authors ===", *sorted(authors), "", "=== Committers ===", *sorted(committers)]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
