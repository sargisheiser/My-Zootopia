import json
from typing import Any, Dict, List

def load_data(file_path: str) -> List[Dict[str, Any]]:
    """Loads a JSON file and returns the parsed Python object."""
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)

def print_animals(data: List[Dict[str, Any]]) -> None:
    """ Iterates animals and prints:
    - Name (top-level 'name')
    - Diet (from characteristics.diet)
    - Location (first element of 'locations' list)
    - Type (from characteristics.type)
    Omits any field that doesn't exist. """
    for animal in data:
        lines = []
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
            print("\n".join(lines))
            print()


def main() -> None:
    animals_data = load_data("animals-data.json")
    print_animals(animals_data)

if __name__ == "__main__":
    main()