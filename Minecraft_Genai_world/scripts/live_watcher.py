import time
import os
import sys
import traceback
from pathlib import Path

# Setup ścieżek
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from src.domain.brief import MarketingBrief
from src.orchestrator import Orchestrator

# ⚙️ TWOJA ŚCIEŻKA DO LOGÓW
LOG_PATH = r"C:\Users\janpa\AppData\Roaming\.minecraft\logs\latest.log" 

class MinecraftWatcher:
    def __init__(self, log_path):
        self.log_path = log_path
        try:
            self.orchestrator = Orchestrator(project_root)
        except Exception as e:
            print(f"❌ BŁĄD: {e}")
            sys.exit(1)

        print("\n" + "="*50)
        print(" 🗣️  NATURAL LANGUAGE WATCHER")
        print("="*50)
        print(f"📂 Logi: {log_path}")
        print("👉 Wpisz pełne zdanie, np.:")
        print("   !gen Tchibo, wielka futurystyczna baza na Marsie z czerwonego piasku")
        print("="*50)

    def process_command(self, raw_text):
        print(f"1️⃣ Surowy tekst: '{raw_text}'")
        clean_text = raw_text.strip()
        if not clean_text: return

        # --- NOWA LOGIKA DZIELENIA ---
        # Dzielimy tylko na PIERWSZYM przecinku.
        # Format: "!gen MARKA, DOWOLNE DŁUGIE ZDANIE OPISUJĄCE ŚWIAT"
        
        brand = "Nieznana Marka"
        user_prompt = ""

        if "," in clean_text:
            # split(..., 1) oznacza: podziel tylko raz
            parts = clean_text.split(",", 1)
            brand = parts[0].strip()
            user_prompt = parts[1].strip()
        else:
            # Jeśli user nie dał przecinka, bierzemy pierwsze słowo jako markę
            parts = clean_text.split(" ", 1)
            brand = parts[0].strip()
            if len(parts) > 1:
                user_prompt = parts[1].strip()
            else:
                user_prompt = "Domyślny, ładny świat"

        print(f"2️⃣ Zinterpretowano -> Marka: [{brand}]")
        print(f"   Opis: [{user_prompt}]")

        try:
            # Tworzymy Brief z pełnym zdaniem
            brief = MarketingBrief(
                brand_name=brand,
                user_request=user_prompt, # <--- Tu trafia całe zdanie
                keywords=[], # Już nie potrzebujemy słów kluczowych
                tone="Immersive",
                target_audience="Minecraft Players"
            )
            
            print("⚙️ Uruchamiam AI...")
            self.orchestrator.run_pipeline(brief)
            print("\a") # BEEP
            
        except Exception as e:
            print(f"❌ Błąd: {e}")
            traceback.print_exc()

    def watch(self):
        if not os.path.exists(self.log_path):
            print(f"❌ Brak pliku: {self.log_path}")
            return

        while True:
            try:
                with open(self.log_path, "r", encoding="utf-8", errors='ignore') as f:
                    f.seek(0, 2)
                    while True:
                        line = f.readline()
                        if not line:
                            time.sleep(0.1)
                            continue
                        
                        if "!gen" in line:
                            chunks = line.split("!gen", 1)
                            if len(chunks) > 1:
                                self.process_command(chunks[1])
            except Exception as e:
                print(f"⚠️ Restart: {e}")
                time.sleep(1)

if __name__ == "__main__":
    watcher = MinecraftWatcher(LOG_PATH)
    watcher.watch()