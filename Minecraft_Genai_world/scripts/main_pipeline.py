import sys
from pathlib import Path

# Setup ścieżek
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.domain.brief import MarketingBrief
from src.orchestrator import Orchestrator

def main():
    # 1. Symulacja wpłynięcia briefu (np. z formularza na stronie)
    brief = MarketingBrief(
        brand_name="Tchibo",
        keywords=["coffee", "nature", "industry", "home"]
    )

    # 2. Uruchomienie Orkiestratora
    app = Orchestrator(ROOT)
    app.run_pipeline(brief)

if __name__ == "__main__":
    main()