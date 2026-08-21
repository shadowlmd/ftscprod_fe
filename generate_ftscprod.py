#!/usr/bin/env python3

import argparse
import csv
import sys
from pathlib import Path

MAX_RECORD_SIZE = 255
MAX_NAME_LEN = MAX_RECORD_SIZE - 4
EOF_MARKER = b"\x00\x00\x00\x00"
MIN_ROW_ELEMENTS = 2


def parse_ftsc_product_codes(product_codes_path: str) -> list[tuple[int, str]]:
    """Parse FTSC Product Codes CSV file."""
    path = Path(product_codes_path)
    entries: list[tuple[int, str]] = []
    # Exclude non-product placeholder codes:
    # 0x00FE: No_product_id_allocated
    # 0x00FF: 16-bit_product_id
    # 0x0100: Reserved
    # 0x0104: None
    exclude_codes = {0x00FE, 0x00FF, 0x0100, 0x0104}

    if not path.exists():
        print(f"Error: FTSC Product Codes file {product_codes_path} not found.")
        sys.exit(1)

    with path.open("r", encoding="latin1", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < MIN_ROW_ELEMENTS:
                continue
            code_str = row[0].strip()
            name = row[1].strip().replace("_", " ")
            try:
                code = int(code_str, 16)
            except ValueError:
                print(f"Warning: Could not parse product code '{code_str}' in row: {row}")
                continue
            if code in exclude_codes:
                continue
            entries.append((code, name))
    return entries


def generate_product_database(product_codes_path: str, product_db_path: str) -> None:
    """Generate binary FTSCPROD.FE database file from FTSC Product Codes source."""
    entries = parse_ftsc_product_codes(product_codes_path)
    if not entries:
        print(f"No valid entries found in {product_codes_path}.")
        return

    print(f"Generating {product_db_path} from {product_codes_path} with {len(entries)} entries:")

    records_bytes = bytearray()
    for code, name in entries:
        name_bytes = name.encode("latin1", errors="replace")
        size_val = len(name_bytes) + 4
        # Ensure record size fits within 1 byte (max MAX_RECORD_SIZE)
        if size_val > MAX_RECORD_SIZE:
            print(f"WARNING: Record size exceeds {MAX_RECORD_SIZE} for code {code:04X} ({len(name)} chars). Truncating product name.")
            name_bytes = name_bytes[:MAX_NAME_LEN]
            size_val = len(name_bytes) + 4

        size_byte = bytes([size_val])
        code_bytes = code.to_bytes(2, "little")
        null_byte = b"\x00"

        record = size_byte + code_bytes + name_bytes + null_byte
        records_bytes.extend(record)

    final_data = records_bytes + EOF_MARKER
    total_size = len(final_data) + 2
    header_val = len(final_data)

    target_path = Path(product_db_path)
    with target_path.open("wb") as f:
        f.write(header_val.to_bytes(2, "little"))
        f.write(final_data)

    print(f"Successfully generated {product_db_path}. Total file size: {total_size} bytes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate binary FTSCPROD.FE database file from FTSC Product Codes source.")
    parser.add_argument(
        "product_codes_path",
        help="Path to the FTSC Product Codes file (obtained from http://ftsc.org/docs/ under Miscellaneous Administrative Files)",
    )
    parser.add_argument(
        "product_db_path",
        nargs="?",
        default="FTSCPROD.FE",
        help="Path to the output binary FTSCPROD.FE database file (default: FTSCPROD.FE)",
    )
    args = parser.parse_args()
    generate_product_database(args.product_codes_path, args.product_db_path)
