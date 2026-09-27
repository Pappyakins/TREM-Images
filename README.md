# TREM Toronto — Birthday & Anniversary Wisher

Automated daily birthday and wedding-anniversary checker for the TREM Toronto
family list. Every morning it:

1. Reads the birthday spreadsheet and matches today's date (America/Toronto).
2. Composes a warm, faith-based wish from a rotating set of letter templates.
3. Generates a personalized card (photo + name in script font + TREM logo).
4. Sends the card with the wish as its caption to the WhatsApp group
   (via WhatsApp Web in a managed browser).

## Layout

- `check.py` — matches Month/Day and WedMonth/WedDay against today (Toronto).
- `compose.py` — picks a random template per Service_code group, fills `[NAME]`.
- `make_card.py` — builds the personalized card image.
- `letter_templates/` — 37 birthday (`letter_bd_*.txt`) + 10 wedding (`letter_wd_*.txt`) templates.
- `assets/` — generic `BD.png` / `WD.png` fallbacks and the TREM logo.

## Service codes

1 Male Pastor · 2 Female Pastor · 3 Male Married · 4 Female Married · 5 Twins ·
6 Single Female · 7 Single Male · 8 Children · 9 Grandma · 10 Grandpa

## Usage

```bash
python3 check.py
python3 compose.py --name "Jane Doe" --service-code 4 --kind birthday
python3 make_card.py "<photo url or path>" "Jane Doe" birthday card.jpg
```

Templates are reworded (never sent verbatim): keep the warm faith-based tone,
the scripture verse + reference exactly, and the `TREM TORONTO` sign-off.
