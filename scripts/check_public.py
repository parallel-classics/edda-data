#!/usr/bin/env python3
"""Check that nothing private is about to enter this public repository.

Usage:
    python -I scripts/check_public.py                 # every tracked file in the working tree
    python -I scripts/check_public.py --staged        # what `git commit` would record (pre-commit hook)
    python -I scripts/check_public.py --range A..B    # the lines and files added by the commits in A..B (pre-push, CI)
    python -I scripts/check_public.py --history       # the lines and files added by every commit on every ref
    python -I scripts/check_public.py --install-hooks # point git at .githooks/ in this clone

It looks for: secrets (key and token shapes, private keys, service-account files), email addresses outside the
allowlist, paths of somebody's own computer, links to repositories that are not public, account ids in review
exports, files outside the known folders and file types, and files that are unexpectedly large or binary.

Exit code 0 when clean, 1 when something was found, 2 on a usage error. Standard library only.

Extra terms that must never appear can be kept out of the repository, one regular expression per line, in
`.git/info/public-deny` of a clone or in the file named by the PUBLIC_DENY_FILE environment variable.

When `gitleaks` is on the PATH it is run as well (working tree, staged and range modes); CI always runs it.
A line that is a known false positive can carry the marker `public-ok` with the reason next to it; in JSON
data use the ALLOW table below instead.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys

# ---- what the repository may contain -------------------------------------------------------------------------

TOP_LEVEL = {
    ".gitattributes", ".github", ".githooks", ".gitignore", "CHANGELOG.md", "CITATION.cff",
    "CLAUDE.md", "CONTRIBUTING.md", "LICENSE", "README.md", "aligned", "auto", "docs", "entities", "guide",
    "images", "intros", "overlays", "paths", "reviews", "scripts", "sources",
}
EXTENSIONS = {
    "json", "md", "txt", "txtl", "html", "htm", "py", "cff", "jpg", "webp", "png", "svg", "yml", "toml",
    "gitkeep", "gitignore", "gitattributes", "",
}
BINARY_EXT = {"jpg", "webp", "png"}
MAX_BYTES = {"default": 3_000_000, "jpg": 12_000_000, "webp": 6_000_000, "png": 6_000_000, "json": 8_000_000,
             "html": 3_000_000}

BAD_NAMES = re.compile(
    r"(^|/)(\.env(\..*)?|.*\.pem|.*\.key|.*\.p12|.*\.pfx|.*\.keystore|id_(rsa|dsa|ecdsa|ed25519)(\.pub)?|"
    r".*service[-_]?account.*\.json|.*firebase-adminsdk.*\.json|credentials.*\.json|client_secret.*\.json|"
    r".*\.sqlite3?|.*\.db|\.npmrc|\.netrc|\.claude(/.*)?|.*\.log|.*\.csv|.*\.xlsx?|.*\.zip|.*\.tgz|.*\.tar(\..*)?)$",
    re.I)

# ---- what a line may not contain -----------------------------------------------------------------------------

EMAIL_OK = {"rights@openedda.is", "hello@openedda.is", "noreply@anthropic.com", "noreply@github.com"}
EMAIL_OK_DOMAINS = ("users.noreply.github.com", "example.org", "example.com")
# Emails that belong to a named file (the maintainer's address is public only in CITATION.cff).
EMAIL_OK_IN = {"CITATION.cff": None}  # None = any address in that file

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY")),
    ("service-account file", re.compile(r'"type"\s*:\s*"service_account"|"private_key(_id)?"\s*:')),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Google OAuth token", re.compile(r"\bya29\.[0-9A-Za-z_\-]{20,}")),
    ("Google OAuth client secret", re.compile(r"\bGOCSPX-[0-9A-Za-z_\-]{20,}")),
    ("GitHub token", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[0-9A-Za-z]{30,}\b|\bgithub_pat_[0-9A-Za-z_]{30,}\b")),
    ("API key (sk-)", re.compile(r"\bsk-(ant-|proj-)?[0-9A-Za-z_\-]{24,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[0-9A-Za-z\-]{10,}\b")),
    ("AWS key id", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("Stripe key", re.compile(r"\b(sk|rk|pk)_live_[0-9A-Za-z]{16,}\b")),
    ("JSON web token", re.compile(r"\beyJ[0-9A-Za-z_\-]{10,}\.eyJ[0-9A-Za-z_\-]{10,}\.[0-9A-Za-z_\-]{10,}")),
    ("secret assignment", re.compile(
        r"(?i)\b(api[_-]?key|secret|token|passwd|password|client[_-]?secret)\b\s*[=:]\s*[\"'][^\"'\s]{12,}[\"']")),
    ("path on a personal computer", re.compile(
        r"(?i)\b[a-z]:[\\/]+users[\\/]|/mnt/[a-z]/users/|(?<![\w.])/home/[a-z][\w.\-]*/|(?<![\w.])/Users/[A-Za-z][\w.\-]*/")),
    ("link to a repository that is not public", re.compile(
        r"(?i)github\.com[/:]parallel-classics/(?!edda-data\b)[\w.\-]+")),
    ("private artifact or console link", re.compile(
        r"(?i)claude\.ai/(artifact|code|chat|share|project)|console\.(firebase|cloud)\.google\.com|"
        r"docs\.google\.com/|drive\.google\.com/|mail\.google\.com/")),
]
EMAIL = re.compile(r"(?<![\w.+\-/])[A-Za-z0-9][\w.+\-]*@[A-Za-z0-9][A-Za-z0-9\-]*(\.[A-Za-z0-9\-]+)+(?![\w\-])")
# Account ids must not appear in the review exports.
UID_KEY = re.compile(r'"(uid|user_id|userId|email|reviewer_uid|account)"\s*:')
NOT_A_TLD = {"jpg", "jpeg", "webp", "png", "svg", "json", "md", "txt", "html", "htm", "py"}
OK_MARK = "public-ok"

# Known, looked-at exceptions: (path regex, finding kind, text regex). Keep each one narrow and say why.
ALLOW: list[tuple[re.Pattern[str], str, re.Pattern[str]]] = [
    # This script describes the shapes it looks for.
    (re.compile(r"^scripts/check_public\.py$"), "*", re.compile(r"")),
    # The address this source publishes for notices of use; it is part of the provenance record.
    (re.compile(r"^sources/is/netutgafan/README\.md$"), "email address", re.compile(r"netut@snerpa\.is")),
]


def load_extra_terms() -> list[tuple[str, re.Pattern[str]]]:
    out = []
    paths = [os.environ.get("PUBLIC_DENY_FILE") or ""]
    try:
        common = git("rev-parse", "--git-common-dir").strip()
        paths.append(os.path.join(common, "info", "public-deny"))
    except subprocess.CalledProcessError:
        pass
    for p in paths:
        if p and os.path.isfile(p):
            with open(p, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        out.append(("local deny-list term", re.compile(line)))
    return out


# ---- git helpers ---------------------------------------------------------------------------------------------

def git(*args: str, text: bool = True):
    return subprocess.run(["git", *args], check=True, capture_output=True,
                          **({"text": True, "encoding": "utf-8", "errors": "replace"} if text else {})).stdout


def ext_of(path: str) -> str:
    base = path.rsplit("/", 1)[-1]
    if base.startswith(".") and base.count(".") == 1:
        return base[1:]
    return base.rsplit(".", 1)[-1].lower() if "." in base else ""


class Findings:
    def __init__(self) -> None:
        self.items: list[tuple[str, str, str, str]] = []
        self.seen: set[tuple[str, str, str]] = set()
        self.notes: set[str] = set()

    def add(self, where: str, path: str, kind: str, detail: str) -> None:
        key = (path, kind, detail)
        if key in self.seen:
            return
        self.seen.add(key)
        self.items.append((where, path, kind, detail))


def allowed(path: str, kind: str, text: str) -> bool:
    for prx, k, trx in ALLOW:
        if (k == "*" or k == kind) and prx.search(path) and trx.search(text):
            return True
    return False


def redact(s: str) -> str:
    s = s.strip()
    return s if len(s) <= 12 else s[:6] + "…" + s[-3:]


def check_path(f: Findings, where: str, path: str, size: int | None) -> None:
    top = path.split("/", 1)[0]
    ext = ext_of(path)
    if top not in TOP_LEVEL:
        f.add(where, path, "new top-level file or folder", top)
    if ext not in EXTENSIONS:
        f.add(where, path, "file type not seen in this repository", "." + ext)
    if BAD_NAMES.search(path) and not allowed(path, "file name", path):
        f.add(where, path, "file name that usually holds something private", path.rsplit("/", 1)[-1])
    if size is not None and size > MAX_BYTES.get(ext, MAX_BYTES["default"]):
        f.add(where, path, "unexpectedly large file", f"{size:,} bytes")


def check_line(f: Findings, where: str, path: str, line: str, extra) -> None:
    if OK_MARK in line:
        return
    for kind, rx in PATTERNS + extra:
        m = rx.search(line)
        if m and not allowed(path, kind, line):
            f.add(where, path, kind, redact(m.group(0)) if "key" in kind or "token" in kind or "secret" in kind
                  else m.group(0)[:80])
    if "@" in line:
        for m in EMAIL.finditer(line):
            addr = m.group(0).rstrip(".").lower()
            if addr.rsplit(".", 1)[-1] in NOT_A_TLD:  # a file name such as odin@dusk-600.jpg
                continue
            if addr in EMAIL_OK or addr.endswith(EMAIL_OK_DOMAINS) or path in EMAIL_OK_IN:
                continue
            if not allowed(path, "email address", line):
                f.add(where, path, "email address", addr)
    if path.startswith("reviews/") and UID_KEY.search(line) and not allowed(path, "account id", line):
        f.add(where, path, "account id in a review export", UID_KEY.search(line).group(0))


def check_blob(f: Findings, where: str, path: str, data: bytes, extra) -> None:
    ext = ext_of(path)
    check_path(f, where, path, len(data))
    if ext in BINARY_EXT:
        return
    if b"\0" in data[:8192]:
        f.add(where, path, "binary content in a text file type", "." + ext)
        return
    for line in data.decode("utf-8", "replace").splitlines():
        check_line(f, where, path, line, extra)


# ---- modes ---------------------------------------------------------------------------------------------------

def scan_tree(f: Findings, extra) -> int:
    paths = [p for p in git("ls-files", "-z").split("\0") if p]
    for p in paths:
        if not os.path.isfile(p):
            continue
        if ext_of(p) in BINARY_EXT:
            check_path(f, "tree", p, os.path.getsize(p))
            continue
        with open(p, "rb") as fh:
            check_blob(f, "tree", p, fh.read(), extra)
    return len(paths)


def scan_staged(f: Findings, extra) -> int:
    paths = [p for p in git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split("\0") if p]
    for p in paths:
        data = git("show", ":" + p, text=False)
        check_blob(f, "staged", p, data, extra)
    return len(paths)


def scan_log(f: Findings, extra, rev_args: list[str]) -> int:
    """Added lines and added paths of the commits selected by rev_args; also their messages and identities."""
    proc = subprocess.Popen(
        ["git", "log", "-p", "-U0", "--no-color", "--no-renames", "--no-textconv",
         "--format=%x01commit %H%n%x01id %an <%ae> | %cn <%ce>%n%x01msg %s%n%b%x01end", *rev_args],
        stdout=subprocess.PIPE)
    assert proc.stdout is not None
    commit = "?"
    path = None
    in_msg = False
    n = 0
    for raw in proc.stdout:
        line = raw.decode("utf-8", "replace").rstrip("\n")
        if line.startswith("\x01commit "):
            commit = line[8:16]
            n += 1
            path = None
            continue
        if line.startswith("\x01id "):
            for m in EMAIL.finditer(line):
                addr = m.group(0).lower()
                if not (addr.endswith(EMAIL_OK_DOMAINS) or addr in EMAIL_OK):
                    f.notes.add(f"note: commits carry the address {addr} as author or committer; it is public with "
                                "the commit. A GitHub noreply address keeps a personal one out of the history.")
            continue
        if line.startswith("\x01msg "):
            in_msg = True
            line = line[5:]
        if in_msg:
            if line.endswith("\x01end"):
                in_msg = False
                line = line[:-4]
            check_line(f, commit, "(commit message)", line, extra)
            continue
        if line.startswith("diff --git "):
            path = None
            continue
        if line.startswith("+++ "):
            path = None if line[4:] == "/dev/null" else line[6:]
            if path:
                check_path(f, commit, path, None)
            continue
        if line.startswith("Binary files ") and " b/" in line:
            p = line.split(" b/", 1)[1].rsplit(" differ", 1)[0]
            check_path(f, commit, p, None)
            if ext_of(p) not in BINARY_EXT:
                f.add(commit, p, "binary content in a text file type", "." + ext_of(p))
            continue
        if path and line.startswith("+") and not line.startswith("+++"):
            if ext_of(path) not in BINARY_EXT:
                check_line(f, commit, path, line[1:], extra)
    proc.wait()
    return n


def scan_sizes(f: Findings, rev_args: list[str]) -> None:
    """Sizes of every blob reachable from the selected commits."""
    objs = subprocess.run(["git", "rev-list", "--objects", *rev_args], check=True, capture_output=True).stdout
    out = subprocess.run(["git", "cat-file", "--batch-check=%(objecttype) %(objectsize) %(rest)"], input=objs,
                         check=True, capture_output=True).stdout.decode("utf-8", "replace")
    for line in out.splitlines():
        parts = line.split(" ", 2)
        if len(parts) == 3 and parts[0] == "blob" and parts[2]:
            size, p = int(parts[1]), parts[2]
            if size > MAX_BYTES.get(ext_of(p), MAX_BYTES["default"]):
                f.add("history", p, "unexpectedly large file", f"{size:,} bytes")


def run_gitleaks(mode: str, rev: str | None) -> int:
    exe = shutil.which("gitleaks")
    if not exe:
        print("check_public: gitleaks is not installed here; the project's own checks ran, CI runs gitleaks.")
        return 0
    base = [exe, "--no-banner", "--redact", "--exit-code", "1"]
    if mode == "staged":
        cmd = base[:1] + ["git", "--staged"] + base[1:] + ["."]
    elif mode == "tree":
        cmd = base[:1] + ["dir"] + base[1:] + ["."]
    else:
        cmd = base[:1] + ["git"] + base[1:] + (["--log-opts", rev] if rev else ["--log-opts", "--all"]) + ["."]
    return subprocess.run(cmd).returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--staged", action="store_true")
    g.add_argument("--range", metavar="A..B")
    g.add_argument("--history", action="store_true")
    g.add_argument("--install-hooks", action="store_true")
    ap.add_argument("--no-gitleaks", action="store_true")
    a = ap.parse_args()

    os.chdir(git("rev-parse", "--show-toplevel").strip())
    if a.install_hooks:
        git("config", "core.hooksPath", ".githooks")
        print("git hooks: core.hooksPath = .githooks (pre-commit and pre-push run scripts/check_public.py)")
        return 0

    extra = load_extra_terms()
    f = Findings()
    if a.staged:
        mode, n, what = "staged", scan_staged(f, extra), "staged files"
    elif a.range:
        mode, n, what = "range", scan_log(f, extra, [a.range]), f"commits in {a.range}"
        scan_sizes(f, [a.range])
    elif a.history:
        mode, n, what = "history", scan_log(f, extra, ["--all"]), "commits on all refs"
        scan_sizes(f, ["--all"])
    else:
        mode, n, what = "tree", scan_tree(f, extra), "tracked files"

    for where, path, kind, detail in f.items:
        print(f"{where}: {path}: {kind}: {detail}")
    for note in sorted(f.notes):
        print(note)
    rc = 1 if f.items else 0
    if not a.no_gitleaks:
        rc = max(rc, 1 if run_gitleaks(mode, a.range) else 0)
    if rc:
        print(f"check_public: FAILED ({len(f.items)} finding(s) in {n} {what}). Nothing private goes into a "
              "public repository: fix it, or if it is a false positive add a narrow ALLOW entry with the reason.")
    else:
        print(f"check_public: OK ({n} {what}" + (f", {len(extra)} local deny-list term(s)" if extra else "") + ")")
    return rc


if __name__ == "__main__":
    sys.exit(main())
