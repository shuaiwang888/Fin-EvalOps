"""Skill loader — discovers Skill protocol files on disk and syncs metadata to DB.

Three families live side-by-side at the project root:
- 自研评测Skill/  (self-eval, 13 skills, primary for MVP)
- 竞品对比Skill/  (competitor-compare, 14 skills, P2)
- 端到端Skill/    (end-to-end, 14 skills, P2)

Each skill subdir contains:
- SKILL_zh.md       (frontmatter: name, description)
- README.md         (optional, more detail)
- scripts/rule.py   (Python rules — peeked for dimensions count)
- references/
    MANIFEST.md
    rubric/_index.md + cap_*.md + <dim>.md
    golden_cases/_index.md
    root-cause/_index.md
    tool_list/_index.md
    output-schema_zh.md

We do NOT mutate any of these files — read-only sync into the `skills` table.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

import frontmatter

from ..db import db_session
from ..models import Skill, TestCategory
from ..utils.trace import get_logger

log = get_logger(__name__)


FAMILY_DIRS = {
    "self": "自研评测Skill",
    "competitor": "竞品对比Skill",
    "e2e": "端到端Skill",
}

# Recognise "01-something" or "01-诊股查数" prefixes
CODE_PREFIX_RE = re.compile(r"^(\d{2})-(.+)$")

# Maps zh dirname to English slug used in 数据测试集 directory names
# (kept here so we can join self-eval skills with test categories)
SELF_SKILL_EN_SLUGS = {
    "01": "event-and-concept-stock-selection",
    "02": "backtesting-data-extraction-and-calculation",
    "03": "stock-diagnosis-and-data-lookup",
    "04": "analysis-evaluation-and-self-judgment",
    "05": "kyc-recommendation-suggestions",
    "06": "compound-intent",
    "07": "interactive-clarification",
    "08": "information-and-knowledge-qa",
    "09": "financial-performance-interpretation",
    "10": "financial-common-sense-and-semantic-understanding",
    "11": "instruction-following-ability",
    "12": "financial-logical-reasoning",
    "13": "time-awareness-ability",
}


@dataclass
class SkillRecord:
    id: str
    family: str
    code: str
    name_zh: str
    name_en: str
    schema_version: str
    description: str
    one_liner: str
    path: str
    dimensions: dict
    caps: dict
    root_causes: dict
    tools: dict
    golden_case_count: int = 0
    raw_files: Dict[str, str] = field(default_factory=dict)  # in-memory cache


# ============================================================================
# Disk scanning
# ============================================================================
class SkillLoader:
    """Scans the three family directories and produces SkillRecord objects.

    Construct once per request OR cache via lru_cache — file mtimes are
    re-checked in `get_skill_files()`.
    """

    def __init__(self, project_root: Path):
        self.root = Path(project_root).resolve()

    # ------------------------- public API -------------------------
    def scan_all(self) -> List[SkillRecord]:
        out: List[SkillRecord] = []
        for family, dirname in FAMILY_DIRS.items():
            base = self.root / dirname
            if not base.exists():
                log.warning("Skill family dir missing: %s", base)
                continue
            for sub in sorted(base.iterdir()):
                if not sub.is_dir():
                    continue
                if sub.name in {"原始文件"}:
                    continue
                m = CODE_PREFIX_RE.match(sub.name)
                if not m:
                    continue
                code, name_rest = m.group(1), m.group(2).strip()
                rec = self._parse_skill_dir(family, code, name_rest, sub)
                if rec:
                    out.append(rec)
        return out

    def scan_family(self, family: str) -> List[SkillRecord]:
        return [r for r in self.scan_all() if r.family == family]

    def get_one(self, skill_id: str) -> Optional[SkillRecord]:
        for r in self.scan_all():
            if r.id == skill_id:
                return r
        return None

    def sync_to_db(self) -> int:
        records = self.scan_all()
        with db_session() as db:
            # Ensure test categories exist (1:1 with self-eval skills 01..13)
            for code, slug in SELF_SKILL_EN_SLUGS.items():
                # find zh name from records (self family)
                cat = db.get(TestCategory, code)
                self_rec = next((r for r in records if r.family == "self" and r.code == code), None)
                if not cat:
                    cat = TestCategory(
                        code=code,
                        slug=slug,
                        name_zh=self_rec.name_zh if self_rec else f"分类 {code}",
                        name_en=self_rec.name_en if self_rec else slug,
                        description=self_rec.one_liner if self_rec else "",
                        mapped_skill_id=f"self/{code}",
                    )
                    db.add(cat)
                else:
                    if self_rec:
                        cat.name_zh = self_rec.name_zh
                        cat.name_en = self_rec.name_en
                        cat.description = self_rec.one_liner or cat.description
                        cat.mapped_skill_id = f"self/{code}"

            for rec in records:
                row = db.get(Skill, rec.id)
                if row is None:
                    row = Skill(id=rec.id)
                    db.add(row)
                row.family = rec.family
                row.code = rec.code
                row.name_zh = rec.name_zh
                row.name_en = rec.name_en
                row.schema_version = rec.schema_version
                row.description = rec.description
                row.one_liner = rec.one_liner
                row.path = rec.path
                row.dimensions = rec.dimensions
                row.caps = rec.caps
                row.root_causes = rec.root_causes
                row.tools = rec.tools
                row.golden_case_count = rec.golden_case_count
                row.updated_at = datetime.now(timezone.utc)
        return len(records)

    # ------------------------- file reading -------------------------
    def read_skill_file(self, skill_id: str, relpath: str) -> str:
        """Read a file relative to a skill's root, cached by (skill_id, relpath, mtime)."""
        rec = self.get_one(skill_id)
        if not rec:
            raise FileNotFoundError(f"Skill {skill_id} not found")
        full = Path(rec.path) / relpath
        if not full.exists():
            return ""
        return _read_cached(str(full), full.stat().st_mtime_ns)

    def load_protocol_bundle(self, skill_id: str) -> Dict[str, str]:
        """Load the full Skill protocol context used by the evaluator prompt.

        Returns a dict keyed by section name; all values are markdown text.
        Missing files become empty strings (not errors) so partially-built
        skills still work.
        """
        rec = self.get_one(skill_id)
        if not rec:
            raise FileNotFoundError(f"Skill {skill_id} not found")
        base = Path(rec.path)
        sections = {
            "skill": _safe_read(base / "SKILL_zh.md"),
            "rubric_index": _safe_read(base / "references/rubric/_index.md"),
            "rubric_raw_scale": _safe_read(base / "references/rubric/raw-score-scale.md"),
            "golden_cases": _safe_read(base / "references/golden_cases/_index.md"),
            "root_cause": _safe_read(base / "references/root-cause/_index.md"),
            "tool_list": _safe_read(base / "references/tool_list/_index.md"),
            "output_schema": _safe_read(base / "references/output-schema_zh.md"),
        }
        # Concatenate all cap_*.md (each Skill has 5-10)
        rubric_dir = base / "references/rubric"
        cap_blocks: List[str] = []
        if rubric_dir.exists():
            for f in sorted(rubric_dir.glob("cap_*.md")):
                cap_blocks.append(f"### {f.stem}\n\n{_safe_read(f)}")
        sections["caps"] = "\n\n".join(cap_blocks)
        return sections

    # ------------------------- private parsers -------------------------
    def _parse_skill_dir(
        self, family: str, code: str, name_rest: str, path: Path
    ) -> Optional[SkillRecord]:
        skill_md = path / "SKILL_zh.md"
        if not skill_md.exists():
            log.warning("SKILL_zh.md missing in %s", path)
            return None
        try:
            post = frontmatter.load(skill_md)
        except Exception as exc:
            # Bad frontmatter / encoding / EOF — don't let one broken skill
            # brick the whole scan.
            log.warning("Skipping skill %s — frontmatter parse failed: %s", path, exc)
            return None

        name_en = (post.metadata.get("name") or "").strip()
        description = (post.metadata.get("description") or "").strip()
        body = post.content
        # Extract one-liner = first non-heading paragraph of body
        one_liner = _extract_one_liner(body)
        # Extract schema_version (look in output-schema_zh.md first, then SKILL body)
        schema_version = _extract_schema_version(path, body)

        dimensions = _parse_index_md(path / "references/rubric/_index.md", kind="rubric")
        caps = _parse_caps(path / "references/rubric")
        root_causes = _parse_index_md(path / "references/root-cause/_index.md", kind="root_cause")
        tools = _parse_index_md(path / "references/tool_list/_index.md", kind="tool")
        golden_count = _count_golden_cases(path / "references/golden_cases/_index.md")

        return SkillRecord(
            id=f"{family}/{code}",
            family=family,
            code=code,
            name_zh=name_rest,
            name_en=name_en or path.name,
            schema_version=schema_version or f"{family}-{code}/v1",
            description=description,
            one_liner=one_liner,
            path=str(path),
            dimensions=dimensions,
            caps=caps,
            root_causes=root_causes,
            tools=tools,
            golden_case_count=golden_count,
        )


# ============================================================================
# Lightweight markdown parsers (best-effort; never raise on malformed files)
# ============================================================================
_SCHEMA_RE = re.compile(r"schema_version[\"'`:\s]*([A-Za-z0-9_\-./]+/v\d+)")
_DIM_LINE_RE = re.compile(
    r"^\s*[\-\*\d.]+\s*\*{0,2}`?([a-zA-Z_][a-zA-Z0-9_]*)`?\*{0,2}\s*[:：]?\s*(.*?)\s*$"
)


def _extract_one_liner(body: str) -> str:
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "<!--", "---", "|", ">")):
            continue
        return s[:200]
    return ""


def _extract_schema_version(skill_dir: Path, skill_body: str) -> str:
    out_schema = skill_dir / "references/output-schema_zh.md"
    if out_schema.exists():
        txt = out_schema.read_text(encoding="utf-8")
        m = _SCHEMA_RE.search(txt)
        if m:
            return m.group(1)
    m = _SCHEMA_RE.search(skill_body)
    return m.group(1) if m else ""


def _parse_index_md(path: Path, kind: str) -> dict:
    if not path.exists():
        return {"count": 0, "items": []}
    text = path.read_text(encoding="utf-8")
    # heuristic: count level-2/3 headers OR list items naming dimensions
    headers = re.findall(r"^#{2,3}\s+([^\n]+)$", text, flags=re.MULTILINE)
    # also include backtick-quoted identifiers
    idents = re.findall(r"`([a-z_][a-z0-9_]*)`", text)
    items: list[dict] = []
    seen: set[str] = set()
    for h in headers:
        key = h.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        items.append({"label": key})
    for ident in idents:
        if ident in seen:
            continue
        seen.add(ident)
        items.append({"key": ident})
    return {"count": len(items), "items": items[:40], "kind": kind}


def _parse_caps(rubric_dir: Path) -> dict:
    if not rubric_dir.exists():
        return {"count": 0, "items": []}
    items = []
    for f in sorted(rubric_dir.glob("cap_*.md")):
        name = f.stem.removeprefix("cap_")
        body = f.read_text(encoding="utf-8")
        # try to extract ceiling number
        m = re.search(r"上限\s*[:：]?\s*(\d+)|ceiling\s*[:：]?\s*(\d+)", body)
        ceiling = int(m.group(1) or m.group(2)) if m else None
        # extract first heading as label
        h = re.search(r"^#+\s+(.+)$", body, flags=re.MULTILINE)
        label = h.group(1).strip() if h else name
        items.append({"key": name, "label": label, "ceiling": ceiling})
    return {"count": len(items), "items": items}


def _count_golden_cases(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    # count "case_XX" identifiers or numbered headings
    cases = re.findall(r"case[_\- ]?\d+|案例\s*\d+|Case\s*\d+", text)
    return len(set(cases))


# ============================================================================
# Cached file reader (mtime-aware)
# ============================================================================
@lru_cache(maxsize=512)
def _read_cached(path: str, mtime_ns: int) -> str:  # noqa: ARG001
    p = Path(path)
    return p.read_text(encoding="utf-8")


def _safe_read(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return _read_cached(str(path), path.stat().st_mtime_ns)
    except Exception as exc:
        log.warning("Could not read %s: %s", path, exc)
        return ""


# ============================================================================
# Module singletons
# ============================================================================
_global_loader: Optional[SkillLoader] = None


def get_loader() -> SkillLoader:
    global _global_loader
    if _global_loader is None:
        from ..config import settings

        _global_loader = SkillLoader(settings.skills_root_abs)
    return _global_loader


def reset_loader() -> None:
    global _global_loader
    _global_loader = None
    _read_cached.cache_clear()
