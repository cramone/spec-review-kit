#!/usr/bin/env python3
"""
compliance_coverage — validate every spec-section and ADR anchor cited by every mapping file
under the compliance subtree.

Compliance mapping files cite spec and ADR sections through markdown links. A citation is
legitimate only if its target file + anchor actually resolve. This script walks every
compliance file, extracts every link that points into the spec, ADR, or dependency-gaps
subtree, and verifies the file exists and the fragment resolves to a heading in that file.

Three checks, every one hard zero — any hit fails the run:

  file-missing   target file does not exist
  anchor-missing fragment does not resolve to a heading in the target file
  dead-platform  dependency-gap link whose F0nn file does not exist

Compliance files themselves are not spec-purity-checked (docs_guard excludes the compliance
subtree). This script is the complement — it validates the citations in compliance files
point at real spec state.

Config is loaded from `.spec-review.toml` at the repo root. When `compliance.enabled = false`,
this script exits 0 as a no-op.

  python .github/scripts/compliance_coverage.py              # check, exit 1 on any hit
  python .github/scripts/compliance_coverage.py --report     # additional per-standard coverage report
"""

from __future__ import annotations
import argparse, re, sys, tomllib
from dataclasses import dataclass
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


# ─────────────────────────────── config loader ───────────────────────────────

@dataclass(frozen=True)
class Config:
    root: Path
    docs: Path
    spec: Path
    adrs: Path
    compliance: Path
    dep_gaps: Path | None
    enabled: bool
    tracked_subtrees: tuple[str, ...]


def _find_config_root() -> Path:
    candidates = [Path(__file__).resolve().parents[2], Path.cwd().resolve()]
    seen: set[Path] = set()
    for start in candidates:
        for p in [start, *start.parents]:
            if p in seen:
                continue
            seen.add(p)
            if (p / ".spec-review.toml").exists():
                return p
    sys.stderr.write(
        "compliance_coverage: no .spec-review.toml found at repo root.\n"
    )
    sys.exit(2)


def load_config() -> Config:
    root = _find_config_root()
    data = tomllib.loads((root / ".spec-review.toml").read_text(encoding="utf-8"))
    paths = data.get("paths", {})
    comp = data.get("compliance", {})

    spec = root / paths.get("spec", "docs/spec")
    adrs = root / paths.get("adrs", "docs/adrs")
    compliance = root / paths.get("compliance", "docs/compliance")
    dep_gaps = (root / paths["dependency_gaps"]) if paths.get("dependency_gaps") else None

    docs = spec.parent if spec.exists() else root / "docs"

    subs: list[str] = []
    for p in (spec, adrs, dep_gaps):
        if p is None:
            continue
        try:
            subs.append(p.relative_to(docs).as_posix() + "/")
        except ValueError:
            # Path outside the docs root — ignore for subtree tracking.
            pass

    return Config(
        root=root, docs=docs, spec=spec, adrs=adrs,
        compliance=compliance, dep_gaps=dep_gaps,
        enabled=bool(comp.get("enabled", False)),
        tracked_subtrees=tuple(subs),
    )


# ─────────────────────────────── shared helpers ───────────────────────────────

def slug(heading: str) -> str:
    """GitHub-style heading slug — matches docs_guard.slug() exactly."""
    s = re.sub(r"`|\*\*|\*|~~", "", heading.strip().lower())
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s", "-", s).strip("-")


FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def _lines_outside_fences(path: Path):
    char, length = "", 0
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
        m = FENCE.match(line)
        if not char:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                char, length = m.group(1)[0], len(m.group(1))
            yield n, line
        else:
            if m and m.group(1)[0] == char and len(m.group(1)) >= length and not m.group(2).strip():
                char, length = "", 0


def _anchors_in(path: Path) -> set[str]:
    anchors: set[str] = set()
    for _, line in _lines_outside_fences(path):
        h = re.match(r"^\s*>?\s*#{1,6}\s+(.*)$", line)
        if h:
            anchors.add(slug(h.group(1)))
        anchors.update(x.lower() for x in re.findall(r'<a\s+id="([^"]+)"', line))
    return anchors


LINK = re.compile(r"\]\(([^)\s]+)\)")


def check(cfg: Config):
    """Yield (file, line, link, reason) for every unresolved citation."""
    if not cfg.compliance.exists():
        return
    anchors_cache: dict[Path, set[str]] = {}

    for f in sorted(cfg.compliance.rglob("*.md")):
        for n, line in _lines_outside_fences(f):
            for link in LINK.findall(line):
                if link.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                path, _, frag = link.partition("#")
                target = (f.parent / path).resolve() if path else f.resolve()
                try:
                    rel = target.relative_to(cfg.docs)
                except ValueError:
                    continue
                rel_str = rel.as_posix()
                if not any(rel_str.startswith(s) for s in cfg.tracked_subtrees):
                    continue
                if not target.exists():
                    yield f.relative_to(cfg.root).as_posix(), n, link, "file-missing"
                    continue
                if frag:
                    if target not in anchors_cache:
                        anchors_cache[target] = _anchors_in(target)
                    if frag.lower() not in anchors_cache[target]:
                        yield f.relative_to(cfg.root).as_posix(), n, link, "anchor-missing"


def report(cfg: Config):
    """Emit a coverage summary per compliance file."""
    if not cfg.compliance.exists():
        print(f"{cfg.compliance.relative_to(cfg.root).as_posix()}/ not present")
        return

    print()
    print("Compliance coverage per standard")
    print("-" * 60)
    for f in sorted(cfg.compliance.rglob("*.md")):
        if f.name == "INDEX.md":
            continue
        rows_total = 0
        rows_mapped = 0
        rows_tbd = 0
        in_table = False
        header_seen = False
        for _, line in _lines_outside_fences(f):
            s = line.strip()
            if s.startswith("|") and s.endswith("|"):
                if not header_seen:
                    header_seen = True
                    in_table = True
                    continue
                if re.match(r"^\|\s*[-:]+", s):
                    continue
                rows_total += 1
                if "tbd" in s.lower() or "|  |" in s:
                    rows_tbd += 1
                else:
                    rows_mapped += 1
            else:
                if in_table:
                    in_table = False
                    header_seen = False
        rel = f.relative_to(cfg.root).as_posix()
        if rows_total:
            print(f"  {rel:50} {rows_mapped:>3}/{rows_total:<3} rows mapped")
        else:
            print(f"  {rel:50} (no mapping table)")
    print()


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate compliance mapping citations resolve.")
    ap.add_argument("--report", action="store_true", help="emit per-standard coverage summary")
    args = ap.parse_args()

    cfg = load_config()
    if not cfg.enabled:
        print("compliance_coverage: disabled in .spec-review.toml ([compliance] enabled = false)")
        return 0

    hits = list(check(cfg))
    for reason in ("file-missing", "anchor-missing"):
        n = sum(1 for _, _, _, r in hits if r == reason)
        print(f"[{'FAIL' if n else 'ok':4}] {reason:16} {n:4}")

    if hits:
        print()
        for file, line, link, reason in hits[:25]:
            print(f"   {file}:{line}  [{reason}]\n     {link}")
        if len(hits) > 25:
            print(f"   … and {len(hits) - 25} more")

    if args.report:
        report(cfg)

    if hits:
        print()
        print(f"compliance_coverage: FAIL — {len(hits)} unresolved citation(s).")
        print("Fix: either update the compliance mapping to cite an existing spec/ADR section, or land the spec change the citation anticipates.")
        return 1

    print("\ncompliance_coverage: pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
