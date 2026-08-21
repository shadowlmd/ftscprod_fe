#!/usr/bin/env python3

import os
import sys


def parse_text_list(filepath):
    """Parse text product list file provided on command line."""
    entries = []
    # Exclude non-product placeholder codes:
    # 0x00FE: No_product_id_allocated
    # 0x00FF: 16-bit_product_id
    # 0x0100: Reserved
    # 0x0104: None
    exclude_codes = {0x00FE, 0x00FF, 0x0100, 0x0104}

    if not os.path.exists(filepath):
        print(f"Error: Text source file {filepath} not found.")
        sys.exit(1)

    with open(filepath, "r", encoding="latin1") as f:
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


def generate_fe(text_path, fe_path="FTSCPROD.FE"):
    entries = parse_text_list(text_path)
    if not entries:
        print(f"No valid entries found in {text_path}.")
        return

    print(f"Generating {fe_path} from {text_path} with {len(entries)} entries:")

    records_bytes = bytearray()
    for code, name in entries:
        name_bytes = name.encode("latin1", errors="replace")
        size_val = len(name_bytes) + 4
        # Ensure record size fits within 1 byte (max 255)
        if size_val > 255:
            print(f"WARNING: Record size exceeds 255 for code {code:04X} ({len(name)} chars). Truncating product name.")
            max_name_len = 251
            name_bytes = name_bytes[:max_name_len]
            size_val = len(name_bytes) + 4

        size_byte = bytes([size_val])
        code_bytes = code.to_bytes(2, "little")
        null_byte = b"\x00"

        record = size_byte + code_bytes + name_bytes + null_byte
        records_bytes.extend(record)

    final_data = records_bytes + b"\x00\x00\x00\x00"
    total_size = len(final_data) + 2
    header_val = len(final_data)

    with open(fe_path, "wb") as f:
        f.write(header_val.to_bytes(2, "little"))
        f.write(final_data)

    print(f"Successfully generated {fe_path}. Total file size: {total_size} bytes.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <product_codes_text_file> [binary_fe_file]")
        print("Error: Product codes source filename must be specified on the command line.")
        sys.exit(1)

    text_source = sys.argv[1]
    fe_target = sys.argv[2] if len(sys.argv) > 2 else "FTSCPROD.FE"
    generate_fe(text_source, fe_target)
