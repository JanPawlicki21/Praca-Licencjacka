import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.builder.mcfunction_builder import write_datapack


def main() -> None:
    pack_dir = write_datapack(ROOT)
    print(f"✅ Datapack generated at: {pack_dir}")
    print("✅ It should contain:")
    print(f"   - {pack_dir / 'pack.mcmeta'}")
    print(f"   - {pack_dir / 'data' / 'tchibo' / 'functions' / 'build_cafe.mcfunction'}")


if __name__ == "__main__":
    main()
