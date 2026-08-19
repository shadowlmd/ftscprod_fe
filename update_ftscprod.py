#!/usr/bin/env python3
import os


def parse_fe(filepath="FTSCPROD.FE"):
    existing_codes = set()
    if not os.path.exists(filepath):
        return existing_codes, b""
    with open(filepath, "rb") as f:
        header = f.read(2)
        data = f.read()

    while data and data[-1] == 0:
        data = data[:-1]

    pos = 0
    while pos < len(data):
        size_byte = data[pos]
        if size_byte == 0:
            pos += 1
            continue
        record_len = size_byte
        if pos + record_len > len(data):
            break
        record_data = data[pos : pos + record_len]
        code = int.from_bytes(record_data[1:3], "little")
        existing_codes.add(code)
        pos += record_len

    clean_data = data[:pos]
    return existing_codes, clean_data


def parse_text_list(filepath="ftscprod.020"):
    entries = []
    # Exclude non-product placeholder codes:
    # 0x00FE: No_product_id_allocated
    # 0x00FF: 16-bit_product_id
    # 0x0100: Reserved
    # 0x0104: None
    exclude_codes = {0x00FE, 0x00FF, 0x0100, 0x0104}
    with open(filepath, "r", encoding="latin1") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",", 1)
            if len(parts) < 2:
                continue
            code_str = parts[0].strip()
            name = parts[1].split(",")[0].strip()
            try:
                code = int(code_str, 16)
            except ValueError:
                continue
            if code in exclude_codes:
                continue
            entries.append((code, name))
    return entries


def append_missing_entries(fe_path="FTSCPROD.FE", text_path="ftscprod.020"):
    existing_codes, clean_data = parse_fe(fe_path)
    text_entries = parse_text_list(text_path)

    missing = [(code, name) for code, name in text_entries if code not in existing_codes]
    if not missing:
        print(f"No missing product codes found. [`{fe_path}`](FTSCPROD.FE) is already up to date.")
        return

    print(f"Found {len(missing)} missing product codes to append to [`{fe_path}`](FTSCPROD.FE):")

    new_records_bytes = bytearray()
    for code, name in missing:
        name_bytes = name.encode("latin1", errors="replace")
        size_val = len(name_bytes) + 4
        # Ensure record size fits within 1 byte (max 255)
        if size_val > 255:
            print(f"WARNING: Record size exceeds 255 for code 0x{code:04X} ({len(name)} chars). Truncating product name.")
            max_name_len = 251
            name_bytes = name_bytes[:max_name_len]
            size_val = len(name_bytes) + 4

        size_byte = bytes([size_val])
        code_bytes = code.to_bytes(2, "little")
        null_byte = b"\x00"

        record = size_byte + code_bytes + name_bytes + null_byte
        new_records_bytes.extend(record)
        print(f"Adding code 0x{code:04X}: {name}")

    final_data = clean_data + new_records_bytes
    total_size = len(final_data) + 2
    header_val = len(final_data)

    with open(fe_path, "wb") as f:
        f.write(header_val.to_bytes(2, "little"))
        f.write(final_data)

    print(f"Successfully appended {len(missing)} entries to [`{fe_path}`](FTSCPROD.FE). New file size: {total_size} bytes.")


if __name__ == "__main__":
    append_missing_entries()
