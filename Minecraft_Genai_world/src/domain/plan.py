from typing import List, Literal, Optional
from pydantic import BaseModel

class BuildingDesign(BaseModel):
    wall_material: str
    roof_material: str
    floor_material: str
    window_material: str
    height: int
    width: int
    length: int
    roof_type: str

class Zone(BaseModel):
    zone_type: str
    name: str
    purpose: str
    design: BuildingDesign

class TerrainSettings(BaseModel):
    theme: str
    roughness: int
    vegetation: int
    base_block: str
    # --- NOWOŚĆ: To pole naprawia błąd ValidationError ---
    path_material: str = "gravel" 

class WorldPlan(BaseModel):
    brand_name: str
    brand_story: Optional[str] = "Witaj w świecie marki."
    terrain: TerrainSettings
    zones: List[Zone]