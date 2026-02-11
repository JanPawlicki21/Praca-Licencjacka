import sys
from pathlib import Path
import json

# --- project root (folder, gdzie jest src/, data/, scripts/) ---
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))  # ważniejsze niż append

from src.domain.brief import MarketingBrief
from src.genai.plan_generator import generate_world_plan


def main() -> None:
    brief = MarketingBrief(
        brand_name="Tchibo",
        keywords=["coffee", "cozy", "lifestyle"]
    )

    plan = generate_world_plan(brief)

    # ✅ ZAWSZE zapisuj do folderu projektu (niezależnie od cwd)
    output_path = ROOT / "data" / "plans" / "tchibo_plan.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(plan.model_dump(), f, indent=2, ensure_ascii=False)

    print(f"✅ Saved world plan to: {output_path}")
    print(f"ℹ️ Current working dir: {Path.cwd()}")


if __name__ == "__main__":
    main()
