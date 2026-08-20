#!/usr/bin/env python3
import os
import sys


def dump_fe(filepath="FTSCPROD.FE"):
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found.")
        return

    with open(filepath, "rb") as f:
        file_size_header = int.from_bytes(f.read(2), "little")
        data = f.read()

    print(f"File: {filepath}")
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
    filepath = sys.argv[1] if len(sys.argv) > 1 else "FTSCPROD.FE"
    dump_fe(filepath)
