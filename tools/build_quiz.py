from __future__ import annotations
import json
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:
    raise SystemExit("Instale: pip install pyyaml")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "quizzes" / "pop" / "source" / "questions.yml"
OUT = ROOT / "quizzes" / "pop" / "build" / "quiz_pop.json"

def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Arquivo fonte não encontrado: {SRC}")

    data = yaml.safe_load(SRC.read_text(encoding="utf-8"))

    OUT.parent.mkdir(parents=True, exist_ok=True)

    # JSON minificado (menor, mais rápido no fetch)
    OUT.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8"
    )

    print(f"✅ Gerado: {OUT.as_posix()} ({OUT.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
