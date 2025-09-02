import json
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "animals-data.json"
TEMPLATE_FILE = BASE_DIR / "animals_template.html"
PLACEHOLDER = "REPLACE_ANIMALS_INFO"

def load_data(file_path: Path) -> List[Dict[str, Any]]:
    """Loads a JSON file and returns the parsed Python object."""
    text = file_path.read_text(encoding="utf-8")
    return json.loads(text)

def build_animals_text(data: List[Dict[str, Any]]) -> str:
    """ Builds a text for each animal:
    - Name (top-level 'name')
    - Diet (from characteristics.diet)
    - Location (first element of 'locations' list)
    - Type (from characteristics.type)
    Omits any field that doesn't exist. """

    blocks: List[str] = []

    for animal in data:
        lines: List[str] = []

        name = animal.get("name")
        if name:
            lines.append(f"Name: {name}")

        diet = (animal.get("characteristics") or {}).get("diet")
        if diet:
            lines.append(f"Diet: {diet}")

        locations = animal.get("locations")
        if isinstance(locations, list) and locations:
            lines.append(f"Location: {locations[0]}")

        a_type = (animal.get("characteristics") or {}).get("type")
        if a_type:
            lines.append(f"Type: {a_type}")

        if lines:
            blocks.append("\n".join(lines))

    return "\n\n".join(blocks) + "\n"

def main() -> None:
    animals_data = load_data(JSON_FILE)
    animals_text = build_animals_text(animals_data)
    html = TEMPLATE_FILE.read_text(encoding="utf-8")

    if PLACEHOLDER not in html:
       raise Exception("Placeholder not found in HTML")

    final_html = html.replace(PLACEHOLDER, animals_text)
    TEMPLATE_FILE.write_text(final_html, encoding="utf-8")



if __name__ == "__main__":
    main()