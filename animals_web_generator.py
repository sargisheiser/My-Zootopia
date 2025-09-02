import json
import re
from html import escape
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple




BASE_DIR: Path = Path(__file__).resolve().parent
JSON_FILE: Path = BASE_DIR / "animals_data.json"
TEMPLATE_FILE: Path = BASE_DIR / "animals_template.html"
UL_PATTERN = re.compile(r'(?is)(<ul\s+class="cards"[^>]*>)(.*?)(</ul>)')
ALL = "ALL"
UNKNOWN = "UNKNOWN"


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
   except json.JSONDecodeError as exc:
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


def get_skin_type(animal: Dict[str, Any]) -> Optional[str]:
   return (animal.get("characteristics") or {}).get("skin_type")


def unique_skin_types(data: Iterable[Dict[str, Any]]) -> List[str]:
   vals = { (get_skin_type(a) or "").strip()for a in data }
   vals = { v for v in vals if v }
   return sorted(vals, key=str.casefold)


def prompt_skin_type(options: List[str]) -> str:
   """ Prompt user to choose a skin_type.
   Accepts: - number (1..N) - exact text (case-insensitive)
   - 'all' or '' for everything
   - 'unknown' to filter animals missing skin_type
   """
   print("\nAvailable skin_type values:")
   print(f" 0) {ALL} (show all)")
   for i, opt in enumerate(options, start=1):
       print(f" {i}) {opt}")
   print(f" u) {UNKNOWN} (animals without skin_type)")


   raw = input("\nChoose skin_type (number/text, Enter for ALL): ").strip()
   if not raw:
       return ALL


   if raw.isdigit():
       idx = int(raw)
       if idx == 0:
           return ALL
       if 1 <= idx <= len(options):
           return options[idx - 1]
       print("Invalid number; defaulting to ALL.")
       return ALL


   raw_up = raw.upper()
   if raw_up == ALL:
       return ALL
   if raw_up == UNKNOWN:
       return UNKNOWN


   for opt in options:
       if opt.lower() == raw.lower():
           return opt


   print("Unrecognized input; defaulting to ALL.")
   return ALL


def filter_by_skin_type( data: Iterable[Dict[str, Any]], selection: str ) -> List[Dict[str, Any]]:
   if selection == ALL:
       return list(data)
   if selection == UNKNOWN:
       return [a for a in data if not (get_skin_type(a) or "").strip()]


   return [
       a for a in data
       if (get_skin_type(a) or "").strip().lower() == selection.strip().lower()
   ]


def serialize_animal(animal: Dict[str, Any]) -> str:
   """
      Convert a single animal object
   """
   name = animal.get("name")
   c = animal.get("characteristics") or {}
   diet = c.get("diet")
   a_type = c.get("type")
   skin = c.get("skin_type")
   lifespan = c.get("lifespan")
   locations = animal.get("locations")
   first_loc = locations[0] if isinstance(locations, list) and locations else None


   title_html = escape(name) if name else "Unknown"


   fields: List[Tuple[str, Optional[str]]] = [
       ("Diet", diet),
       ("Location", first_loc),
       ("Type", a_type),
       ("Skin", skin),
       ("Lifespan", lifespan),
   ]
   items: List[str] = [
       f'<li class="card__field"><strong>{label}:</strong> {escape(value)}</li>'
       for (label, value) in fields if value
   ]


   inner_ul = "\n ".join(items)


   if inner_ul: return (
       '<li class="cards__item">\n'
       f' <div class="card__title">{title_html}</div>\n'
       ' <div class="card__text">\n'
       ' <ul class="card__fields">\n'
       f' {inner_ul}\n' ' </ul>\n'
       ' </div>\n' '</li>' )


   return (
       '<li class="cards__item">\n'
       f'  <div class="card__title">{title_html}</div>\n'
       '</li>'
   )


def build_animals_html(data: List[Dict[str, Any]]) -> str:
   return "\n".join(serialize_animal(a) for a in data)


def inject_into_ul(html: str, inner_html: str) -> str:
   """
     Replace whatever is currently inside <ul class="cards">...</ul> with inner_html,
     preserving the <ul> wrapper. Case-insensitive and tolerant of attributes.
   """
   if not UL_PATTERN.search(html):
       raise RuntimeError('Could not find <ul class="cards"> </ul> in template.')
   return UL_PATTERN.sub(r"\1\n" + inner_html + r"\n\3", html)


def main() -> None:
   animals = load_data(JSON_FILE)
   options = unique_skin_types(animals)
   selection = prompt_skin_type(options)
   filtered = filter_by_skin_type(animals, selection)
   print(f"\nSelected: {selection} rendering {len(filtered)} of {len(animals)} animals.")
   items_html = build_animals_html(filtered)
   template = read_template(TEMPLATE_FILE)
   final_html = inject_into_ul(template, items_html)
   write_template(TEMPLATE_FILE, final_html)


if __name__ == "__main__":
   main()
