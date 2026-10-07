#!/usr/bin/env python3
"""
docs-guard — enforces the spec-purity rules in CLAUDE.md § "Spec files state the specified system".

Ten checks, every one hard zero — any hit fails the run:

  citations     an id cited but not defined inside docs/              docs/
  build-status  whether code exists / is wired / is deployed          docs/spec/
  dates         a date in spec prose, full or year-month              docs/spec/
  editorial     change history, tracking, open questions, notes       docs/spec/
                to a reader, attribution, decision rationale
  future-work   "will be built", "going to", "plans to"               docs/spec/
  backcompat    "for now", "legacy support", "backward compat"        docs/spec/
  links         relative links and heading anchors that resolve       docs/
  references    a bare `<name>.md` that resolves to a real file       docs/spec/
  truncation    a `](` with no closing paren on the line              docs/
  structure     closed code fences, consistent table columns          docs/

docs/review/ and docs/compliance/ are out of scope for every check — they carry citations, dates
and review state that spec files cannot.

Config is loaded from `.spec-review.toml` at the repo root. Paths, allowlist tokens, enabled
checks and reference-allow entries all live there — a repo customises its vocabulary without
forking the detector.

  python .github/scripts/docs_guard.py                 # check, exit 1 on any hit
  python .github/scripts/docs_guard.py --check citations,links

There is no baseline. A hit is fixed at its source: reword the spec, or — if the detector is
wrong — adjust the config or fix the detector.

Scope note: `dates`, `build-status`, `editorial`, `future-work` and `backcompat` run over the
spec subtree only. An ADR legitimately records when a decision was taken, who took it, what was
rejected and the state the decision replaced; a spec file states current design and nothing else.
"""

from __future__ import annotations
import argparse, difflib, os, re, sys, tomllib
from dataclasses import dataclass
from pathlib import Path

# The report uses box-drawing characters. A Windows console defaults to cp1252, where printing
# them raises UnicodeEncodeError — so the guard would crash on the failure path, after announcing
# a violation but before naming where it is. The exit code stays 1 either way; what is lost is
# the part a human needs. Linux CI already runs UTF-8, so this is a no-op there.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # not a reconfigurable text stream
        pass


# ─────────────────────────────── config loader ───────────────────────────────

@dataclass(frozen=True)
class Config:
    root: Path
    docs: Path
    spec: Path
    adrs: Path
    exclude: tuple[Path, ...]
    allow_families: frozenset[str]
    allow_tokens: frozenset[str]
    reference_allow: frozenset[str]
    checks_enabled: tuple[str, ...]


def _find_config_root() -> Path:
    """Walk up from the script location, then from cwd, looking for .spec-review.toml."""
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
        "docs-guard: no .spec-review.toml found at repo root.\n"
        "            run `/init-spec-review` to scaffold one, or copy from\n"
        "            kit/_config/spec-review.example.toml in the spec-review-kit repo.\n"
    )
    sys.exit(2)


def load_config() -> Config:
    root = _find_config_root()
    data = tomllib.loads((root / ".spec-review.toml").read_text(encoding="utf-8"))

    paths = data.get("paths", {})
    spec = root / paths.get("spec", "docs/spec")
    adrs = root / paths.get("adrs", "docs/adrs")

    # docs root is inferred as the common parent of spec/adrs.
    docs = root / "docs"
    if spec.exists():
        docs = spec.parent

    exclude = tuple(
        root / p for key in ("review", "compliance")
        if (p := paths.get(key))
    )

    g = data.get("guard", {})
    families = frozenset(g.get("allow_families", []))
    tokens_grouped = g.get("allow_tokens", {})
    tokens = frozenset(t for group in tokens_grouped.values() for t in group)
    ref_allow = frozenset(g.get("references", {}).get("allow", []))
    checks = tuple(g.get("checks", {}).get("enabled", list(CHECK_NAMES)))

    return Config(
        root=root, docs=docs, spec=spec, adrs=adrs, exclude=exclude,
        allow_families=families, allow_tokens=tokens,
        reference_allow=ref_allow, checks_enabled=checks,
    )


# Names are declared ahead of load_config so defaults can reference them.
CHECK_NAMES = (
    "citations", "build-status", "dates", "editorial", "future-work",
    "backcompat", "links", "references", "truncation", "structure",
)


# ─────────────────────────────── shared helpers ───────────────────────────────

ID = re.compile(r"\b([A-Z][A-Za-z]{0,5})-([0-9]+(?:\.[0-9]+)?)\b")

# The separator is not what makes an id an id. A hyphen-only pattern cannot see `W29` or `S12`,
# which is how such tokens have sat in review folders while a citation check reported clean.
ID_NOSEP = re.compile(r"\b([A-Z]{1,5})([0-9]{1,4})\b")

# A .NET format specifier sits straight after `name:` — `{shard:D2}`, `{Version:D10}`,
# `(tenantId, versionNumber:D10, …)`. Recognising the position, not the token, covers every
# width a key template will ever use. The allow-token list keeps a specifier named bare in prose.
FORMAT_SPEC_BEFORE = re.compile(r"\w:$")


def md_files(cfg: Config, base: Path):
    return sorted(
        p for p in base.rglob("*.md")
        if not any(p.is_relative_to(x) for x in cfg.exclude)
    )


# CommonMark fences: a run of three or more backticks or tildes opens one, and only a run of
# the SAME character, at least as long, with nothing after it, closes it. Toggling on any ```
# or ~~~ line let a ~~~ inside a ``` block (or a ```` fence wrapping a ``` example) flip the
# state, so the checks read code as prose and prose as code. A backtick fence's info string
# may not itself contain a backtick — that is inline code, not a fence.
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def _walk(path: Path, eof: dict | None = None):
    """Yield (lineno, text, opener): opener is the line of the enclosing fence, 0 outside one.
    Delimiter lines count as inside. On return, eof["open_at"] is the line of a fence never closed."""
    char, length, open_at = "", 0, 0
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
        m = FENCE.match(line)
        if not char:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                char, length, open_at = m.group(1)[0], len(m.group(1)), n
            yield n, line, open_at
        else:
            yield n, line, open_at
            if m and m.group(1)[0] == char and len(m.group(1)) >= length and not m.group(2).strip():
                char, length, open_at = "", 0, 0
    if eof is not None:
        eof["open_at"] = open_at


def lines_outside_fences(path: Path):
    for n, line, opener in _walk(path):
        if not opener:
            yield n, line


# A link target is a path or heading slug, not prose: `[why a jti store was wrong](…#…-not-merely-unbuilt)`
# names a heading, and the words in the slug are that heading's, not a claim this file makes.
def strip_link_targets(line: str) -> str:
    return re.sub(r"\]\([^)\s]*\)", "]()", line)


def rel(cfg: Config, path: Path) -> str:
    return path.relative_to(cfg.root).as_posix()


def slug(heading: str) -> str:
    s = re.sub(r"`|\*\*|\*|~~", "", heading.strip().lower())
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s", "-", s).strip("-")   # each space its own hyphen, as GitHub does


# ─────────────────────────────────── checks ───────────────────────────────────

def check_citations(cfg: Config):
    """An id is legitimate only if something inside docs/ defines it."""
    occ: dict[str, list] = {}
    for f in md_files(cfg, cfg.docs):
        for n, line in lines_outside_fences(f):
            for m in ID.finditer(line):
                if m.group(1) in cfg.allow_families:
                    continue
                occ.setdefault(m.group(0), []).append((f, n, line))
            for m in ID_NOSEP.finditer(line):
                if m.group(0) in cfg.allow_tokens or m.group(1) in cfg.allow_families:
                    continue
                if FORMAT_SPEC_BEFORE.search(line, 0, m.start()):
                    continue
                occ.setdefault(m.group(0), []).append((f, n, line))

    def defines(tok: str, line: str) -> bool:
        t = re.escape(tok)
        return any(re.search(p, line) for p in (
            rf"^#{{1,6}}\s*(\*\*)?`?{t}`?\b",                 # heading
            rf"^\s*[-*+]\s*(\*\*)?`?{t}`?(\*\*)?\s*[:—–-]",   # list definition
            rf"^\s*\|\s*(\*\*)?`?{t}`?(\*\*)?\s*\|",          # first table cell
            rf"^\s*(\*\*)?`?{t}`?(\*\*)?\s*[:—–]",            # line-leading definition
            rf'<a\s+id="[^"]*{t}',                            # explicit anchor
        ))

    for tok, sites in occ.items():
        if any(defines(tok, ln) for _, _, ln in sites):
            continue
        for f, n, line in sites:
            yield rel(cfg, f), n, tok, line.strip()


BUILD_STATUS = [
    r"\bnever (?:built|implemented|shipped|wired|deployed|provisioned)\b",
    # `registered` is deliberately absent: "an event that is published but not registered never
    # reaches the projectors" is a rule about the message bus, not a claim about what exists yet.
    r"\bnot (?:yet )?(?:built|implemented|wired|provisioned|deployed|shipped)\b",
    r"\b(?:specified|designed),? (?:and )?(?:not|un)(?:built|implemented|shipped)\b",
    r"\bzero hits\b|\bappears nowhere\b|\brepo-wide grep\b",
    r"\bnothing deploys\b|\bis a `?501`? stub\b",
    r"\bskeleton only\b|\bunbuilt\b",
    r"\blive in production\b|\bas (?:deployed|shipped)\b|\bin production today\b",
    r"\bnot enforced in code\b|\bno code (?:performs|does|reads)\b",
    # `deferred` is domain vocabulary in some platforms. Only the delivery sense is build status,
    # so match the delivery phrasing rather than the bare word.
    r"\bdeferred\s+(?:to|until)\s+(?:a\s+)?(?:later|future|subsequent|post-)\w*\b",
    r"\bdeferred\s+(?:indefinitely|for now|to the backlog)\b",
    r"🟡\s*deferred\b",
]


def check_build_status(cfg: Config):
    pat = re.compile("|".join(BUILD_STATUS), re.I)
    for f in md_files(cfg, cfg.spec):
        for n, line in lines_outside_fences(f):
            for m in pat.finditer(strip_link_targets(line)):
                yield rel(cfg, f), n, m.group(0).strip(), line.strip()


# NOT \b-delimited: `_` is a word character, so \b fails against `_Last reviewed: 2026-08-21_`
# — the single most common date form in spec history. Use explicit lookarounds.
#
# The year-month alternative matters: a partial date is still a date, and matching only full
# forms let "reconciled against code in 2026-08" sit while `dates` reported a clean zero.
# The full-date branch runs first; the trailing `(?![\d-])` stops the year-month branch biting
# into it.
DATE = re.compile(
    r"(?<![\d-])20[0-9]{2}-[0-9]{2}-[0-9]{2}(?![\d-])"
    r"|(?<![A-Za-z])(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+20[0-9]{2}(?![\d])"
    r"|(?<![\d-])20[0-9]{2}-(?:0[1-9]|1[0-2])(?![\d-])"
)


# A date inside a code span is a value — `RetentionStartedAt: 2026-08-14`, `2033-12-31` — the
# same as a date in a fenced payload. A spec that computes due dates needs worked values. The
# span is the line between data and narration; `editorial` catches narration verbs in case a
# stamp is ever dressed up as a value.
def strip_code_spans(line: str) -> str:
    return re.sub(r"`[^`]*`", " ", line)


def check_dates(cfg: Config):
    """No date in spec prose. Git is the review record; a date written as a value goes in a code span."""
    for f in md_files(cfg, cfg.spec):
        for n, line in lines_outside_fences(f):
            for m in DATE.finditer(strip_code_spans(line)):
                yield rel(cfg, f), n, m.group(0), line.strip()


def _suggest_path(cfg: Config, f: Path, path: str, frag: str, paths: set) -> str:
    tail = re.sub(r"^(?:\.\.?/)+", "", path)
    hits = sorted(p for p in paths if p == tail or p.endswith("/" + tail))
    if not hits:
        name = tail.rsplit("/", 1)[-1]
        hits = sorted(p for p in paths if p.rsplit("/", 1)[-1] == name)
    if len(hits) != 1:
        return "target file does not exist" + (f" — {len(hits)} files share its name" if hits else "")
    fixed = Path(os.path.relpath(cfg.root / hits[0], f.parent)).as_posix()
    if not fixed.startswith("."):
        fixed = "./" + fixed
    return f"target file does not exist — did you mean {fixed}{'#' + frag if frag else ''}"


def check_links(cfg: Config):
    paths, _ = _index(cfg)
    anchors: dict[Path, set] = {}
    for f in md_files(cfg, cfg.docs):
        a: set[str] = set()
        for _, line in lines_outside_fences(f):
            h = re.match(r"^\s*>?\s*#{1,6}\s+(.*)$", line)
            if h:
                a.add(slug(h.group(1)))
            a.update(x.lower() for x in re.findall(r'<a\s+id="([^"]+)"', line))
        anchors[f.resolve()] = a

    for f in md_files(cfg, cfg.docs):
        for n, line in lines_outside_fences(f):
            for link in re.findall(r"\]\(([^)\s]+)\)", line):
                if link.startswith(("http://", "https://", "mailto:")):
                    continue
                path, _, frag = link.partition("#")
                if path and not (f.parent / path).exists():
                    yield rel(cfg, f), n, link, _suggest_path(cfg, f, path, frag, paths)
                    continue
                target = f.resolve() if not path else (f.parent / path).resolve()
                if frag and target in anchors and frag.lower() not in anchors[target]:
                    near = difflib.get_close_matches(frag.lower(), anchors[target], n=1, cutoff=0.6)
                    yield rel(cfg, f), n, link, "anchor does not resolve" + (f" — did you mean #{near[0]}" if near else "")


# A filename written as prose or in a table cell is not a link, so `links` cannot see it. The
# leading class excludes `.`, `*` and `>` so that placeholder forms (`<agg>.write-model.md`,
# `*.read-model.md`) are not read as filenames beginning at the dot. A token must start with
# a word character to be a name at all.
MD_TOKEN = re.compile(r"(?<![\w./*>-])(?:[\w.-]+/)*[\w-][\w.-]*\.md(?![\w])")

SKIP_DIRS = {".git", "node_modules", "cdk.out", "bin", "obj", "__pycache__"}


def _index(cfg: Config):
    paths = {
        p.relative_to(cfg.root).as_posix() for p in cfg.root.rglob("*.md")
        if not SKIP_DIRS & set(p.relative_to(cfg.root).parts)
    }
    return paths, {p.rsplit("/", 1)[-1] for p in paths}


def check_references(cfg: Config):
    """A bare `<name>.md` written in a spec file must name a file that exists.

    `links` requires markdown link syntax, so a filename in a table cell or in prose is invisible
    to it — which is how pointers to deleted files can hide."""
    paths, names = _index(cfg)
    for f in md_files(cfg, cfg.spec):
        for n, line in lines_outside_fences(f):
            stripped = re.sub(r"\]\([^)\s]*\)", "]()", line)
            for m in MD_TOKEN.finditer(stripped):
                tok = m.group(0)
                if tok in cfg.reference_allow:
                    continue
                if "/" in tok:
                    tail = re.sub(r"^(?:\.\.?/)+", "", tok)
                    resolved = (
                        any(p == tail or p.endswith("/" + tail) for p in paths)
                        or (f.parent / tok).exists()
                    )
                else:
                    resolved = tok in names or any(nm.endswith("." + tok) for nm in names)
                if not resolved:
                    yield rel(cfg, f), n, tok, line.strip()


def check_truncation(cfg: Config):
    """A link cut off mid-target. `links` needs a closing paren to match at all, so it sees
    nothing, and `structure` looks at a file's end, so a truncation mid-file passes both."""
    for f in md_files(cfg, cfg.docs):
        for n, line in lines_outside_fences(f):
            bare = re.sub(r"`[^`]*`", "", line)      # inline code may hold a literal `](`
            for m in re.finditer(r"\]\(", bare):
                if ")" not in bare[m.end():]:
                    yield rel(cfg, f), n, line.strip()[:80], "link target is not closed"


def check_structure(cfg: Config):
    for f in md_files(cfg, cfg.docs):
        eof: dict = {}
        for _ in _walk(f, eof):
            pass
        if eof["open_at"]:
            yield rel(cfg, f), eof["open_at"], "code fence never closed", ""
        block, start = [], 0
        for n, line in lines_outside_fences(f):
            s = line.strip()
            if s.startswith("|") and s.endswith("|"):
                if not block:
                    start = n
                block.append(line)
            else:
                if len(block) >= 3:
                    widths = {len(re.findall(r"(?<!\\)\|", b)) for b in block}
                    if len(widths) > 1:
                        yield rel(cfg, f), start, "ragged table", f"column counts {sorted(widths)}"
                block = []


# Change history, tracking, open questions, notes addressed to a reader or agent, attribution,
# and decision rationale. Each pattern is a phrase, not a word, because the words are ordinary
# spec vocabulary — `raised as` is how an error mapping is written, `was rejected` how a
# refused upload is described, `decided by` how an invariant is located. This is a tripwire
# for unambiguous forms; rationale in particular has no reliable surface form, and the review
# protocol owns the harder cases.
_D = r"`?(?:20\d\d-\d\d|(?:\d{1,2}\s+)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+20\d\d)"

EDITORIAL = [
    # change history — undated ("this entry previously read…") as well as dated, and dated
    # whether or not the date sits in a code span (which `dates` deliberately lets through).
    r"(?i:\b(?:this|it|the (?:row|table|section|file|entry|spec))\s+(?:previously|formerly|once|originally)\s+(?:said|read|stated|specified|carried|listed)\b)",
    r"(?i:\bpreviously (?:said|read|stated)\b|\bused to (?:say|read|state)\b|\bno longer (?:says|reads|states)\b)",
    r"(?i:\buntil\b[^.]{0,60}\bth(?:is|e \w+) (?:said|read|stated|carried)\b)",
    r"(?i:(?<![A-Za-z])last (?:reviewed|updated|verified|reconciled)\b)",   # not \b: `_Last reviewed_` puts a word char before it
    r"(?i:\b(?:corrected|decided|specified|settled|added|removed|renamed|renumbered|changed|updated|reconciled|projected|superseded)(?: (?:on|in|as of|here))?:?\s+" + _D + r")",
    r"(?i:\b(?:as of|since|until|before|after)\s+" + _D + r")",
    r"\*\((?i:added|changed|removed|updated|corrected)\b",
    # tracking and open questions
    r"(?i:\btracked (?:as|under)\b|\btracked in (?:ADO|Azure DevOps|ClickUp|Jira|Linear|the backlog|the board)\b)",
    r"(?i:\b(?:raised|logged|filed) as (?:an? )?(?:bug|defect|issue|ticket|finding|story|task|work item)\b)",
    r"(?i:\bon the (?:ADO |Linear |Jira )?board\b|\bin the backlog\b)",
    r"(?i:\bneeds? a decision\b|\b(?:awaiting|pending) (?:a )?decision\b|\bdecision (?:is )?(?:pending|outstanding|required)\b)",
    r"(?i:\bopen questions?\b|\bto be (?:decided|confirmed|determined)\b)",
    r"\bTBD\b|\bTODO\b|\bFIXME\b|⏳",
    # notes addressed to a reader or an agent
    r"(?i:\btreat (?:this|it|the rest of)\b[^.]*\bas (?:authoritative|unverified)\b|\bdo(?:n'?t| not) propose\b)",
    r"(?i:\bnote to (?:the )?(?:reader|agent|implementer)s?\b|\bAI agents?\b|\bif you are an? (?:agent|AI)\b|\bbefore proposing\b)",
    # attribution — a capitalised name after the verb; "decided by the aggregate" is design, not attribution
    r"\b(?i:decided|agreed|signed off|approved|proposed|requested) (?i:by|with) (?!The\b|A\b|An\b)[A-Z][a-z]+\b",
    r"(?i:\bat the request of\b)",
    r"\b(?i:pending) (?!`)[A-Z][a-z]+\b",
    # rationale and rejected options
    r"(?i:\bwe (?:chose|decided|considered|rejected|opted|went with|picked)\b|\bconsidered and rejected\b|\balternatives considered\b)",
]


def check_editorial(cfg: Config):
    pat = re.compile("|".join(EDITORIAL))
    for f in md_files(cfg, cfg.spec):
        for n, line in lines_outside_fences(f):
            for m in pat.finditer(strip_link_targets(line)):
                yield rel(cfg, f), n, m.group(0).strip(), line.strip()


# Pending-work language addressed to a reader, implementer or future session. A spec file is
# written as if the system is complete; a sentence about what will be built belongs on the
# project tracker or in CLAUDE.md § Known deferred/partial work. `will` on its own is domain
# vocabulary ("the handler will refuse", "two callers will present stale tags") — only the
# delivery sense is pending work.
FUTURE_WORK = [
    r"(?i:\bwill be (?:built|deployed|implemented|shipped|wired|provisioned|rolled out)\b)",
    r"(?i:\bgoing to (?:build|deploy|implement|ship|wire|provision|roll out)\b)",
    r"(?i:\b(?:plans|intends) to (?:build|deploy|implement|ship|wire|provision|roll out)\b)",
    r"(?i:\bwe[' ](?:ll|will) (?:build|deploy|implement|ship|wire|provision)\b)",
    r"(?i:\b(?:future|later|subsequent|follow-up) (?:phase|release|iteration|sprint|milestone)\b)",
]


def check_future_work(cfg: Config):
    pat = re.compile("|".join(FUTURE_WORK))
    for f in md_files(cfg, cfg.spec):
        for n, line in lines_outside_fences(f):
            for m in pat.finditer(strip_link_targets(line)):
                yield rel(cfg, f), n, m.group(0).strip(), line.strip()


# Transition language. A removed feature is simply absent from the spec; a changed shape is
# written in its final form and the migration belongs in CLAUDE.md's § Known deferred/partial
# work. `deprecated` is first-class domain vocabulary (lifecycle, API deprecation policy) and
# never matched. `legacy` matches only when qualified by a noun that names a path to retire,
# not when it is part of a system or standard name.
BACKCOMPAT = [
    r"(?i:\bfor now\b)",
    r"(?i:\bin the interim\b)",
    r"(?i:\blegacy (?:behaviou?r|support|path|flow))\b",
    r"(?i:\btransitional\s+(?:shape|form|period))\b",
]


def check_backcompat(cfg: Config):
    pat = re.compile("|".join(BACKCOMPAT))
    for f in md_files(cfg, cfg.spec):
        for n, line in lines_outside_fences(f):
            for m in pat.finditer(strip_link_targets(line)):
                yield rel(cfg, f), n, m.group(0).strip(), line.strip()


CHECKS = {
    "citations":    check_citations,
    "build-status": check_build_status,
    "dates":        check_dates,
    "editorial":    check_editorial,
    "future-work":  check_future_work,
    "backcompat":   check_backcompat,
    "links":        check_links,
    "references":   check_references,
    "truncation":   check_truncation,
    "structure":    check_structure,
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Enforce the spec-purity rules over docs/.")
    ap.add_argument("--check", help="comma-separated subset of: " + ", ".join(CHECKS))
    args = ap.parse_args()

    cfg = load_config()
    enabled = set(cfg.checks_enabled)
    selected = [c.strip() for c in args.check.split(",")] if args.check else [c for c in CHECKS if c in enabled]
    for c in selected:
        if c not in CHECKS:
            print(f"unknown check: {c}", file=sys.stderr)
            return 2

    found = {name: list(CHECKS[name](cfg)) for name in selected}
    for name, hits in found.items():
        print(f"[{'FAIL' if hits else 'ok':4}] {name:13} {len(hits):4}")

    failures = [(name, hits) for name, hits in found.items() if hits]
    if not failures:
        print("\ndocs-guard: pass")
        return 0

    print()
    for name, hits in failures:
        print(f"── {name} ──")
        for file, line, match, context in hits[:25]:
            where = f"{file}:{line}" if line else file
            shown = context if name == "links" else context[:120]
            print(f"   {where}\n     {match}" + (f"\n     {shown}" if shown else ""))
        if len(hits) > 25:
            print(f"   … and {len(hits) - 25} more")
        print()

    print(f"docs-guard: FAIL — {sum(len(h) for _, h in failures)} violation(s).")
    print("The rule is CLAUDE.md § 'Spec files state the specified system'.")
    print("A legitimate design statement that trips a check gets reworded; a detector that is wrong gets fixed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
