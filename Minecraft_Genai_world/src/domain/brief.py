from typing import List, Optional
from pydantic import BaseModel, Field

class BrandGuidelines(BaseModel):
    subtle_branding: bool = True
    primary_colors: List[str] = Field(default_factory=list)

class MarketingBrief(BaseModel):
    brand_name: str
    tone: str = "Immersive"
    
    # 🆕 NOWE POLE: Tutaj trafi całe zdanie wpisane przez gracza
    user_request: str = "Domyślny projekt"
    
    # Zostawiamy keywords dla kompatybilności, ale mogą być puste
    keywords: List[str] = Field(default_factory=list)
    target_audience: str = "General Minecraft Players"