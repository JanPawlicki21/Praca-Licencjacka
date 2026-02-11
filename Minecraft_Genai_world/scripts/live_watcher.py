import time
import os
import sys
import traceback
from pathlib import Path

# --- KONFIGURACJA ŚCIEŻEK ---
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from src.domain.brief import MarketingBrief
from src.orchestrator import Orchestrator

# ==============================================================================
# ⚙️ KONFIGURACJA
# ==============================================================================
LOG_PATH = r"C:\Users\janpa\AppData\Roaming\.minecraft\logs\latest.log"

class MinecraftWatcher:
    def __init__(self, log_path):
        self.log_path = log_path
        
        # --- BLOKADA DUPLIKATÓW ---
        self.last_trigger_time = 0 
        self.cooldown_seconds = 3.0  # Ignoruj komendy przez 3 sekundy po uruchomieniu
        
        try:
            self.orchestrator = Orchestrator(project_root)
        except Exception as e:
            print(f"❌ BŁĄD KRYTYCZNY: {e}")
            sys.exit(1)

        print("\n" + "="*50)
        print(" 👀 WATCHER GOTOWY (Zabezpieczony przed duplikatami)")
        print("="*50)
        print(f"📂 Logi: {log_path}")
        print("👉 Wpisz w grze np.: !gen Tchibo, wielka futurystyczna baza")
        print("="*50)

    def process_command(self, raw_text):
        # Sprawdzamy, czy minęło wystarczająco dużo czasu od ostatniej komendy
        current_time = time.time()
        if (current_time - self.last_trigger_time) < self.cooldown_seconds:
            print(f"⏳ Ignoruję duplikat (Cooldown aktywny...)")
            return

        # Zapisujemy czas tego uruchomienia
        self.last_trigger_time = current_time

        print(f"1️⃣ Surowy tekst: '{raw_text}'")
        clean_text = raw_text.strip()
        if not clean_text: return

        # Dzielimy na Markę i Opis
        brand = "Nieznana Marka"
        user_prompt = ""

        if "," in clean_text:
            parts = clean_text.split(",", 1)
            brand = parts[0].strip()
            user_prompt = parts[1].strip()
        else:
            parts = clean_text.split(" ", 1)
            brand = parts[0].strip()
            if len(parts) > 1:
                user_prompt = parts[1].strip()
            else:
                user_prompt = "Domyślny projekt"

        print(f"2️⃣ Zinterpretowano -> Marka: [{brand}]")
        print(f"   Opis: [{user_prompt}]")

        try:
            brief = MarketingBrief(
                brand_name=brand,
                user_request=user_prompt,
                keywords=[],
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

        print("🟢 Nasłuchiwanie aktywne...")
        
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
                            # Rozdzielamy linię w miejscu wystąpienia "!gen"
                            chunks = line.split("!gen", 1)
                            if len(chunks) > 1:
                                self.process_command(chunks[1])
                                
            except Exception as e:
                print(f"⚠️ Restart pętli: {e}")
                time.sleep(1)

if __name__ == "__main__":
    watcher = MinecraftWatcher(LOG_PATH)
    watcher.watch()