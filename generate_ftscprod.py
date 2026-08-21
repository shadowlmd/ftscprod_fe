#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

MAX_RECORD_SIZE = 255
MAX_NAME_LEN = MAX_RECORD_SIZE - 4


def parse_text_list(filepath: str) -> list[tuple[int, str]]:
    """Parse text product list file provided."""
    path = Path(filepath)
    entries: list[tuple[int, str]] = []
    # Exclude non-product placeholder codes:
    # 0x00FE: No_product_id_allocated
    # 0x00FF: 16-bit_product_id
    # 0x0100: Reserved
    # 0x0104: None
    exclude_codes = {0x00FE, 0x00FF, 0x0100, 0x0104}

    if not path.exists():
        print(f"Error: Text source file {filepath} not found.")
        sys.exit(1)

    with path.open("r", encoding="latin1") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",", 1)
            if len(parts) < 2:
                continue
            code_str = parts[0].strip()
            name = parts[1].split(",")[0].strip().replace("_", " ")
            try:
                code = int(code_str, 16)
            except ValueError:
                continue
            if code in exclude_codes:
                continue
            entries.append((code, name))
    return entries


def generate_fe(text_path: str, fe_path: str = "FTSCPROD.FE") -> None:
    """Generate binary FTSCPROD.FE file from text product list."""
    entries = parse_text_list(text_path)
    if not entries:
        print(f"No valid entries found in {text_path}.")
        return

    print(f"Generating {fe_path} from {text_path} with {len(entries)} entries:")

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

    final_data = records_bytes + b"\x00\x00\x00\x00"
    total_size = len(final_data) + 2
    header_val = len(final_data)

    target_path = Path(fe_path)
    with target_path.open("wb") as f:
        f.write(header_val.to_bytes(2, "little"))
        f.write(final_data)

    print(f"Successfully generated {fe_path}. Total file size: {total_size} bytes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate binary FTSCPROD.FE file from text product list.")
    parser.add_argument(
        "text_source",
        help="Path to the product codes text file",
    )
    parser.add_argument(
        "fe_target",
        nargs="?",
        default="FTSCPROD.FE",
        help="Path to the output binary FTSCPROD.FE file (default: FTSCPROD.FE)",
    )
    args = parser.parse_args()
    generate_fe(args.text_source, args.fe_target)
