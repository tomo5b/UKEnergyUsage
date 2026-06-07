import os
import httpx
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

CARBON_API = "https://api.carbonintensity.org.uk"
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


def fetch_national() -> None:
    with httpx.Client() as client:
        intensity_resp = client.get(f"{CARBON_API}/intensity")
        intensity_resp.raise_for_status()
        generation_resp = client.get(f"{CARBON_API}/generation")
        generation_resp.raise_for_status()

    intensity_data = intensity_resp.json()["data"][0]
    generation_data = generation_resp.json()["data"]

    ts = intensity_data["from"]
    intensity = intensity_data["intensity"]
    generation_mix = generation_data.get("generationmix", [])

    row = {
        "ts": ts,
        "intensity_forecast": intensity.get("forecast"),
        "intensity_actual": intensity.get("actual"),
        "intensity_index": intensity.get("index"),
        "generation_mix": generation_mix,
    }

    supabase.table("grid_national").upsert(row, on_conflict="ts").execute()
    print(f"national upserted ts={ts} index={row['intensity_index']}")


def fetch_regional() -> None:
    with httpx.Client() as client:
        resp = client.get(f"{CARBON_API}/regional")
        resp.raise_for_status()

    regions = resp.json()["data"][0]["regions"]
    ts = resp.json()["data"][0]["from"]

    rows = [
        {
            "ts": ts,
            "region_shortname": r["shortname"],
            "intensity_forecast": r["intensity"].get("forecast"),
            "intensity_actual": r["intensity"].get("actual"),
            "intensity_index": r["intensity"].get("index"),
        }
        for r in regions
    ]

    supabase.table("grid_regional").upsert(rows, on_conflict="ts,region_shortname").execute()
    print(f"regional upserted ts={ts} regions={len(rows)}")


if __name__ == "__main__":
    fetch_national()
    fetch_regional()
