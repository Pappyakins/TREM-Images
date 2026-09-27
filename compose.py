#!/usr/bin/env python3
"""Compose a birthday/anniversary wish from Pappy's letter templates.

Picks a random template for the celebrant's demographic group
(Service_code -> template range, from Pappy's old script) and
substitutes the celebrant's name for [NAME].

Usage:
  python3 compose.py --name "Sister Adenike Abass" --service-code 4 --kind birthday
  python3 compose.py --name "John & Jane Doe" --kind wedding
"""
import argparse
import random
from pathlib import Path

TEMPLATES = Path(__file__).parent / "letter_templates"

# Service_code -> (first_template, last_template, group label)
SERVICE_GROUPS = {
    1: (1, 4, "Male Pastor"),
    2: (5, 6, "Female Pastor"),
    3: (7, 11, "Male Married"),
    4: (12, 16, "Female Married"),
    5: (17, 18, "Twins"),
    6: (19, 23, "Single Female"),
    7: (24, 28, "Single Male"),
    8: (29, 33, "Children"),
    9: (34, 35, "Grandma"),
    10: (36, 37, "Grandpa"),
}


def pick_template(kind, service_code=None):
    if kind == "wedding":
        n = random.randint(1, 10)
        return TEMPLATES / f"letter_wd_{n}.txt"
    lo, hi, _label = SERVICE_GROUPS[int(service_code)]
    n = random.randint(lo, hi)
    return TEMPLATES / f"letter_bd_{n}.txt"


def compose(name, kind, service_code=None):
    path = pick_template(kind, service_code)
    text = path.read_text(encoding="utf-8")
    return path.name, text.replace("[NAME]", name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--kind", choices=["birthday", "wedding"], required=True)
    ap.add_argument("--service-code", default=None)
    a = ap.parse_args()
    fname, msg = compose(a.name, a.kind, a.service_code)
    print(f"--- template: {fname} ---")
    print(msg)


if __name__ == "__main__":
    main()
