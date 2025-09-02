import json
import re
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / ("animals_data.json")
TEMPLATE_FILE = BASE_DIR / "animals_template.html"


def load_data(file_path: Path) -> List[Dict[str, Any]]:
   """Loads a JSON file and returns the parsed Python object."""
   text = file_path.read_text(encoding="utf-8")
   if not text.strip():
       raise ValueError(f"{file_path.name} is empty.")
   if text.lstrip().startswith("<"):
       raise ValueError(f"{file_path.name} looks like HTML, not JSON.")
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
           lines.append(f"Name: {name}<br/>")


       diet = (animal.get("characteristics") or {}).get("diet")
       if diet:
           lines.append(f"Diet: {diet}<br/>")


       locations = animal.get("locations")
       if isinstance(locations, list) and locations:
           lines.append(f"Location: {locations[0]}<br/>")


       a_type = (animal.get("characteristics") or {}).get("type")
       if a_type:
           lines.append(f"Type: {a_type}<br/>")


       if lines:
           item_html = '<li class="cards__item">\n' + "\n".join(lines) + "\n</li>"
           blocks.append(item_html)


   return "\n\n".join(blocks) + "\n"


def inject_into_ul(html: str, inner_html: str) -> str:
   pattern = r'(?is)(<ul\s+class="cards"[^>]*>)(.*?)(</ul>)'
   if not re.search(pattern, html):
       raise RuntimeError('Something went wrong.')
   return re.sub(pattern, r"\1\n" + inner_html + r"\n\3", html)


def main() -> None:
   animals_data = load_data(JSON_FILE)
   animals_text = build_animals_text(animals_data)
   html = TEMPLATE_FILE.read_text(encoding="utf-8")


   final_html = inject_into_ul(html, animals_text)
   TEMPLATE_FILE.write_text(final_html, encoding="utf-8")


if __name__ == "__main__":
   main()
