import json
import re
from html import escape
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


BASE_DIR: Path = Path(__file__).resolve().parent
JSON_FILE: Path = BASE_DIR / "animals_data.json"
TEMPLATE_FILE: Path = BASE_DIR / "animals_template.html"
OUTPUT_FILE: Path = BASE_DIR / "animals.html"
UL_PATTERN = re.compile(r'(?is)(<ul\s+class="cards"[^>]*>)(.*?)(</ul>)')
ALL = "ALL"
UNKNOWN = "UNKNOWN"




def load_data(file_path: Path) -> List[Dict[str, Any]]:
   """ Load and parse animal data from a JSON file.
   Args: file_path: Path to the JSON file.
   Returns: A list of dictionaries containing animal data.
   Raises: ValueError: If the file is empty, not valid JSON, or looks like HTML. """


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
   """Read the HTML template as a string."""


   return path.read_text(encoding="utf-8")




def write_template(path: Path, content: str) -> None:
   """ Write updated HTML content to disk.
   Args: path: Path where the file should be written. content: The HTML content to write. """


   try:
       path.write_text(content, encoding="utf-8")
       print(f"Successfully wrote output to {path}")
   except OSError as exc:
       print(f"Failed to write {path}: {exc}")
       raise




def get_skin_type(animal: Dict[str, Any]) -> Optional[str]:
   """Extract the skin type from an animal record (if available)."""


   return (animal.get("characteristics") or {}).get("skin_type")




def unique_skin_types(data: Iterable[Dict[str, Any]]) -> List[str]:
   """Return a sorted list of unique skin types from animal data."""


   vals = {(get_skin_type(a) or "").strip() for a in data}
   vals = {v for v in vals if v}
   return sorted(vals, key=str.casefold)




def prompt_skin_type(options: List[str]) -> str:
   """ Ask user to choose a skin type.
   Supports: - Enter/0 → ALL animals
   - Number  → choose from menu
   - Exact text (case-insensitive)
   - "unknown" → animals with no skin_type """


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




def filter_by_skin_type(data: Iterable[Dict[str, Any]], selection: str) -> List[Dict[str, Any]]:
   """Filter animals by the selected skin type."""


   if selection == ALL:
       return list(data)
   if selection == UNKNOWN:
       return [a for a in data if not (get_skin_type(a) or "").strip()]


   return [a for a in data if (get_skin_type(a) or "").strip().lower() == selection.strip().lower()]




def serialize_animal(animal: Dict[str, Any]) -> str:
   """ Convert a single animal record into an HTML <li> block.
   Args: animal: Dictionary with fields such as 'name', 'characteristics', 'locations'.
   Returns: A string of HTML representing the animal in card format. """


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
       for (label, value) in fields if value]


   inner_ul = "\n ".join(items)


   if inner_ul:
       return (
   '<li class="cards__item">\n'
   f' <div class="card__title">{title_html}</div>\n'
   ' <div class="card__text">\n'
   ' <ul class="card__fields">\n'
   f' {inner_ul}\n'
   ' </ul>\n'
   ' </div>\n'
   '</li>')


   return (
       '<li class="cards__item">\n'
       f' <div class="card__title">{title_html}</div>\n'
       '</li>'
   )




def build_animals_html(data: List[Dict[str, Any]]) -> str:
   """Build HTML for all animals as a joined string of <li> cards."""


   return "\n".join(serialize_animal(a) for a in data)




def inject_into_ul(html: str, inner_html: str) -> str:
   """ Replace the content inside <ul class="cards">.</ul> with new animal cards.
   Args: html: The template HTML string. inner_html:
   The generated list items (<li>.</li>).
   Returns: Updated HTML string with injected animal content.
   Raises: RuntimeError: If the <ul class="cards"> block cannot be found. """




   if not UL_PATTERN.search(html):
       raise RuntimeError('Could not find <ul class="cards">...</ul> in template.')


   return UL_PATTERN.sub(r"\1\n" + inner_html + r"\n\3", html)




def main() -> None:


   animals = load_data(JSON_FILE)
   options = unique_skin_types(animals)
   selection = prompt_skin_type(options)
   filtered = filter_by_skin_type(animals, selection)
   print(f"\nSelected: {selection} → rendering {len(filtered)} of {len(animals)} animals.")
   items_html = build_animals_html(filtered)
   template = read_template(TEMPLATE_FILE)
   final_html = inject_into_ul(template, items_html)
   write_template(OUTPUT_FILE, final_html)


if __name__ == "__main__":
   main()
