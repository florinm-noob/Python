import os
import csv
import json
import argparse
import logging
from dataclasses import dataclass
from collections import defaultdict
from typing import Any, Dict, List


# ---------- OOP domain model ----------
@dataclass(frozen=True)
class Person:
    name: str
    city: str
    age: int

# ---------- Processor (OOP) ----------
class PeopleProcessor:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger

    def read_csv(self, path: str) -> list[Person]:
        """
        Citește CSV (name,city,age) și returnează o listă de Person.
        Rândurile invalide sunt ignorate, dar sunt logate cu WARNING.
        """
        people: list[Person] = []

        try:
            with open(path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                # Validare minimă de header
                required = {"name", "city", "age"}
                if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
                    raise ValueError(f"CSV trebuie să aibă coloanele: {sorted(required)}. Găsit: {reader.fieldnames}")

                for idx, row in enumerate(reader, start=2):  # header=1, primul rând de date=2
                    try:
                        person = self._parse_row(row)
                        people.append(person)
                    except ValueError as e:
                        self.logger.warning("Rând invalid la linia %d: %s | row=%s", idx, e, row)

        except FileNotFoundError:
            self.logger.error("Fișierul de input nu a fost găsit: %s", path)
            return []
        except PermissionError:
            self.logger.error("Nu ai permisiuni să citești fișierul: %s", path)
            return []
        except Exception as e:
            self.logger.exception("Eroare neașteptată la citire CSV: %s", e)
            return []

        self.logger.info("Am citit %d persoane valide din %s", len(people), path)
        return people

    def _parse_row(self, row: dict[str, str]) -> Person:
        name = (row.get("name") or "").strip().lower()
        city = (row.get("city") or "").strip().title()
        age_raw = (row.get("age") or "").strip()

        if not name:
            raise ValueError("name lipsă")
        if not city:
            raise ValueError("city lipsă")

        try:
            age = int(age_raw)
        except ValueError:
            raise ValueError(f"age invalid: {age_raw!r}")

        if age < 0 or age > 130:
            raise ValueError(f"age în afara intervalului: {age}")

        return Person(name=name, city=city, age=age)

    def compute_stats(self, people: list[Person]) -> dict[str, Any]:
        """
        Produce un dict JSON-serializabil cu statistici și lista de persoane.
        """
        total = len(people)
        cities = defaultdict(int)
        age_sum = 0

        for p in people:
            cities[p.city] += 1
            age_sum += p.age

        avg_age = round(age_sum / total, 2) if total else 0

        stats: dict[str, Any] = {
            "numar_total_persoane": total,
            "varsta_medie": avg_age,
            "numar_persoane_pe_orase": dict(cities),
            "people": [
                {"name": p.name, "city": p.city, "age": p.age}
                for p in people
            ],
        }

        self.logger.info("Statistici calculate: total=%d, avg_age=%s, orase=%d", total, avg_age, len(cities))
        return stats

    def write_json(self, path: str, data: dict[str, Any]) -> bool:
        """
        Scrie JSON la path. Returnează True dacă a reușit.
        """
        try:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info("Am scris raportul JSON: %s", path)
            return True
        except PermissionError:
            self.logger.error("Nu ai permisiuni să scrii fișierul: %s", path)
            return False
        except Exception as e:
            self.logger.exception("Eroare neașteptată la scriere JSON: %s", e)
            return False


# ---------- Logging setup ----------
def setup_logging(log_path: str, level: str = "INFO") -> logging.Logger:
    os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)

    logger = logging.getLogger("people_app")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.handlers.clear()  # evită dublarea handlerelor în rerun

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    # Log în fișier
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(getattr(logging, level.upper(), logging.INFO))
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # Log și în consolă (util la dev)
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, level.upper(), logging.INFO))
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger

# ---------- CLI ----------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CSV -> JSON report (OOP + logging)")
    parser.add_argument("--input", required=True, help="Calea către fișierul CSV de input")
    parser.add_argument("--output", required=True, help="Calea către fișierul JSON de output")
    parser.add_argument("--log", required=True, help="Calea către fișierul de log")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Nivelul de logare (default: INFO)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logger = setup_logging(args.log, args.log_level)

    logger.info("Pornire aplicație. input=%s output=%s log=%s log_level=%s", args.input, args.output, args.log, args.log_level)

    processor = PeopleProcessor(logger)
    people = processor.read_csv(args.input)
    if not people:
        logger.warning("Nu există persoane valide. Ieșire.")
        return 1

    stats = processor.compute_stats(people)

    # Afișează un rezumat în consolă (nu tot JSON-ul)
    print("Numar total persoane:", stats["numar_total_persoane"])
    print("Varsta medie:", stats["varsta_medie"])
    print("Persoane pe orase:", stats["numar_persoane_pe_orase"])

    ok = processor.write_json(args.output, stats)
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())