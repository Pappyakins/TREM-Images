"""Daily birthday / wedding-anniversary checker for Pappy's contact list.

Reads the Excel file, compares Month/Day (birthdays) and WedMonth/WedDay
(anniversaries) against today's date in America/Toronto, and prints matches.
Exit code 0 always; prints a clear "none" line when there is nothing.
"""
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

XLSX_PATH = "/home/hatch/workspace/user/files/birthdays__1__0_g2c7.xlsx"

# From Pappy's old script (sel_text_file_bd) + the legend in the sheet's
# trailing columns: Service_code -> (first_template, last_template, label).
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


def group_label(service_code):
    try:
        return SERVICE_GROUPS[int(service_code)][2]
    except (ValueError, TypeError, KeyError):
        return "Unknown"


def load_rows(path):
    try:
        import openpyxl
    except ImportError:
        sys.exit("openpyxl is not installed")
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    header = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
    idx = {name: i for i, name in enumerate(header)}
    rows = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[idx["Name"]]:
            continue
        rows.append({
            "name": str(r[idx["Name"]]).strip(),
            "email": r[idx["Email"]] or "",
            "phone": str(r[idx["PhoneNumber"]] or "").strip(),
            "month": r[idx["Month"]] or 0,
            "day": r[idx["Day"]] or 0,
            "wed_month": r[idx["WedMonth"]] or 0,
            "wed_day": r[idx["WedDay"]] or 0,
            "image": r[idx["Image"]] or "",
            "image_wed": r[idx["Image_wed"]] or "",
            "service_code": r[idx["Service_code"]] or "",
        })
    return rows


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else XLSX_PATH
    today = datetime.now(ZoneInfo("America/Toronto"))
    m, d = today.month, today.day
    rows = load_rows(path)
    bdays = [r for r in rows if int(r["month"] or 0) == m and int(r["day"] or 0) == d]
    annivs = [r for r in rows if int(r["wed_month"] or 0) == m and int(r["wed_day"] or 0) == d]
    print(f"Date checked: {today:%Y-%m-%d} (America/Toronto) — {len(rows)} contacts")
    if bdays:
        print("BIRTHDAYS TODAY:")
        for r in bdays:
            print(f"  - {r['name']} [{group_label(r['service_code'])}] (phone {r['phone']})")
    if annivs:
        print("ANNIVERSARIES TODAY:")
        for r in annivs:
            print(f"  - {r['name']} (phone {r['phone']})")
    if not bdays and not annivs:
        print("NONE: no birthdays or anniversaries today.")


if __name__ == "__main__":
    main()
