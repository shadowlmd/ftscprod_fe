#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

from settings import (
    CODE_OFFSET_END,
    CODE_OFFSET_START,
    EOF_MARKER,
    HEADER_SIZE,
    MIN_RECORD_BYTES,
)


def dump_product_database(db_path: str) -> None:
    """Dump binary FTSCPROD.FE database file contents and product codes with integrity checks."""
    path = Path(db_path)
    if not path.exists():
        print(f"Error: Database file {db_path} not found.")
        sys.exit(1)

    raw_bytes = path.read_bytes()
    if len(raw_bytes) < HEADER_SIZE:
        print(f"Error: Database file {db_path} is too small.")
        sys.exit(1)

    header_val = int.from_bytes(raw_bytes[:HEADER_SIZE], "little")
    payload = raw_bytes[HEADER_SIZE:]

    if header_val != len(payload):
        print(f"Error: Database integrity check failed. Header size ({header_val}) does not match payload length ({len(payload)}).")
        sys.exit(1)

    if not payload.endswith(EOF_MARKER):
        print("Error: Database integrity check failed. Missing required End-of-File (EoF) marker.")
        sys.exit(1)

    print(f"File: {db_path}")
    print(f"File size header: {header_val}, Actual payload length: {len(payload)}")
    print("{:<11} | {:<10} | {}".format("Code (Hex)", "Code (Dec)", "Product Name"))
    print("-" * 50)

    records_data = payload[:-len(EOF_MARKER)]
    pos = 0
    count = 0
    skipped = 0

    while pos < len(records_data):
        size_byte = records_data[pos]
        if size_byte == 0:
            pos += 1
            continue

        record_len = size_byte
        if pos + record_len > len(records_data):
            print(f"Error: Record at position {pos} specifies length {record_len}, which exceeds remaining data. Skipping record.")
            skipped += 1
            break

        record_bytes = records_data[pos : pos + record_len]
        if len(record_bytes) < MIN_RECORD_BYTES or record_bytes[-1] != 0x00:
            print(f"Error: Record at position {pos} has invalid format or length {len(record_bytes)}. Skipping record.")
            skipped += 1
            pos += record_len
            continue

        code = int.from_bytes(record_bytes[CODE_OFFSET_START:CODE_OFFSET_END], "little")
        name_bytes = record_bytes[CODE_OFFSET_END:-1]
        name = name_bytes.decode("latin1", errors="replace")

        print(f"{code:04X}        | {code:<10} | {name}")

        pos += record_len
        count += 1

    print(f"\nTotal records dumped: {count}, Skipped/Invalid records: {skipped}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dump binary FTSCPROD.FE database file contents and product codes.")
    parser.add_argument(
        "db_path",
        nargs="?",
        default="FTSCPROD.FE",
        help="Path to the binary FTSCPROD.FE database file (default: FTSCPROD.FE)",
    )
    args = parser.parse_args()
    dump_product_database(args.db_path)
