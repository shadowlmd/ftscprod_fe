#!/usr/bin/env python3

import argparse
from pathlib import Path


def dump_product_database(db_path: str) -> None:
    """Dump binary FTSCPROD.FE database file contents and product codes."""
    path = Path(db_path)
    if not path.exists():
        print(f"Error: Database file {db_path} not found.")
        return

    with path.open("rb") as f:
        file_size_header = int.from_bytes(f.read(2), "little")
        data = f.read()

    print(f"File: {db_path}")
    print(f"File size header: {file_size_header}, Actual data length: {len(data)}")
    print(f"{'Code (Hex)':<11} | {'Code (Dec)':<10} | {'Product Name'}")
    print("-" * 50)

    pos = 0
    count = 0
    while pos < len(data):
        size_byte = data[pos]
        if size_byte == 0:
            pos += 1
            continue
        record_len = size_byte
        if pos + record_len > len(data):
            print(f"Warning: Record length {record_len} exceeds remaining data at position {pos}")
            break

        record_data = data[pos : pos + record_len]
        code = int.from_bytes(record_data[1:3], "little")
        name_bytes = record_data[3:]
        null_idx = name_bytes.find(b"\x00")
        if null_idx != -1:
            name_bytes = name_bytes[:null_idx]
        name = name_bytes.decode("latin1", errors="replace")

        print(f"{code:04X}        | {code:<10} | {name}")

        pos += record_len
        count += 1

    print(f"\nTotal records dumped: {count}")


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
