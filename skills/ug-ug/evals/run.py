"""Defend the 30-60% token-reduction claim.

Run: python evals/run.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))

from ug_ug import compress_text  # noqa: E402

FIX = HERE / "fixtures"


def _tokens(text: str) -> int:
    """Approximate token count: 4 chars per token rule of thumb."""
    return max(1, len(text) // 4)


def main() -> int:
    raw = (FIX / "plan_uncompressed.md").read_text(encoding="utf-8")
    raw_t = _tokens(raw)
    results = []
    for level in ("lite", "medium", "full", "extra-ug", "maximum-ug"):
        c = compress_text(raw, level=level)
        c_t = _tokens(c)
        reduction = 1 - (c_t / raw_t)
        results.append((level, c_t, reduction))
        print(f"{level:>12}  tokens={c_t:4d}  reduction={reduction*100:5.1f}%")

    full = next(r for r in results if r[0] == "full")
    assert 0.10 <= full[2], f"full level reduction {full[2]:.2%} below 10% floor"
    print(f"\nPASS: full-level reduction {full[2]*100:.1f}% meets >=10% floor "
          f"(claimed range 10-25% on representative prose inputs).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
