import json
import re
from html import escape
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "animals_data.json"
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
       name = animal.get("name")
       characteristics = animal.get("characteristics") or {}
       diet = characteristics.get("diet")
       a_type = characteristics.get("type")
       locations = animal.get("locations")
       first_loc = locations[0] if isinstance(locations, list) and locations else None


       title_html = escape(name) if name else "Unknown"


       detail_lines: List[str] = []
       if diet:
           detail_lines.append(f"<strong>Diet:</strong> {escape(diet)}<br/>")
       if first_loc:
           detail_lines.append(f"<strong>Location:</strong> {escape(first_loc)}<br/>")
       if a_type:
           detail_lines.append(f"<strong>Type:</strong> {escape(a_type)}<br/>")
       if detail_lines:
           details_html = "\n ".join(detail_lines)
           item_html = (
               '<li class="cards__item">\n'
               f'  <div class="card__title">{title_html}</div>\n'
               '  <p class="card__text">\n'
               f'      {details_html}\n'
               '  </p>\n'
               '</li>'
               )


       else:
           item_html = (
               '<li class="cards__item">\n'
               f' <div class="card__title">{title_html}</div>\n'
               '</li>'
           )
       blocks.append(item_html)


   return "\n".join(blocks)


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
