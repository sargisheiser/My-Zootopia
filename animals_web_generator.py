import json
import re
from html import escape
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = BASE_DIR / "animals_data.json"
TEMPLATE_FILE = BASE_DIR / "animals_template.html"
UL_PATTERN = re.compile(r'(?is)(<ul\s+class="cards"[^>]*>)(.*?)(</ul>)', re.IGNORECASE | re.DOTALL)


def load_data(file_path: Path) -> List[Dict[str, Any]]:
   """
   Loads a JSON file and returns the parsed Python object.
   """
   text = file_path.read_text(encoding="utf-8")
   if not text.strip():
       raise ValueError(f"{file_path.name} is empty.")
   if text.lstrip().startswith("<"):
       raise ValueError(f"{file_path.name} looks like HTML, not JSON.")
   try:
       return json.loads(text)
   except json.decoder.JSONDecodeError:
       raise ValueError(f"Invalid JSON in {file_path.name}: {exc}") from exc


def read_template(path: Path) -> str:
   """
   Read the HTML template as a string.
   """
   return path.read_text(encoding="utf-8")


def write_template(path: Path, content: str) -> None:
   """
   Persist updated HTML back to disk.
   """
   path.write_text(content, encoding="utf-8")


def serialize_animal(animal: Dict[str, Any]) -> str:
   """
   Convert a single animal object
   """
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
       details_html = "\n      ".join(detail_lines)
       return (
           '<li class="cards__item">\n'
           f'  <div class="card__title">{title_html}</div>\n'
           '  <p class="card__text">\n'
           f'      {details_html}\n'
           '  </p>\n'
           '</li>'
       )
   else:
       return (
           '<li class="cards__item">\n'
           f'  <div class="card__title">{title_html}</div>\n'
           '</li>'
       )


def build_animals_text(data: List[Dict[str, Any]]) -> str:
   """
   Serialize the full list of animals by delegating to serialize_animal.
   """
   return "\n".join(serialize_animal(animal) for animal in data)


def inject_into_ul(html: str, inner_html: str) -> str:
   """
   Replace whatever is currently inside <ul class="cards">...</ul> with inner_html,
   preserving the <ul> wrapper. Case-insensitive and tolerant of attributes.
   """
   if not UL_PATTERN.search(html):
       raise RuntimeError('Something went wrong.')


   return UL_PATTERN.sub(r"\1\n" + inner_html + r"\n\3", html)


def main() -> None:
   animals = load_data(JSON_FILE)
   items_html = build_animals_text(animals)
   template = read_template(TEMPLATE_FILE)
   final_html = inject_into_ul(template, items_html)
   write_template(TEMPLATE_FILE, final_html)


if __name__ == "__main__":
   main()
