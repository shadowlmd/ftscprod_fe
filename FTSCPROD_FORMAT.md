# FTSCPROD.FE Binary Format Specification

This document describes the binary file format of [`FTSCPROD.FE`](FTSCPROD.FE:1) used by FastEcho for product code lookup.

## File Structure

[`FTSCPROD.FE`](FTSCPROD.FE:1) consists of:
1. **File Header** (2 bytes):
   - Unsigned 16-bit integer (little-endian) representing the total size of the records payload (total file size minus 2 bytes).
2. **Product Records** (variable length sequence):
   - Each record is laid out contiguously without padding between records.
3. **End of File / End of Data Marker** (4 bytes):
   - A final 4-byte zero marker (`0x00000000`) terminating the records payload.

## Record Format

Each individual product record contains:
- **Size Byte** (`1 byte`): Total length of the record in bytes (including the size byte itself). Calculated as `len(product_name) + 4`. Since the size is stored in a single byte, product names longer than 251 characters must be truncated to ensure the total record size does not exceed 255 bytes.
- **Product Code** (`2 bytes`): Unsigned 16-bit integer (little-endian) representing the FTSC product code (e.g., `0x0000`, `0x010A`).
- **Product Name** (`N bytes`): C-style null-terminated ASCII/Latin1 string representing the product name.
- **Null Terminator** (`1 byte`): `0x00` terminating the string.

## Notes

- Non-product placeholder entries (such as `0x00FE`, `0x00FF`, `0x0100`, and `0x0104`) should be excluded when updating binary databases from [`ftscprod.020`](ftscprod.020:23).
- **Important**: Every valid [`FTSCPROD.FE`](FTSCPROD.FE:1) file must conclude with an essential End-of-File / End-of-Data marker (`b"\x00\x00\x00\x00"`) following the last product record to ensure correct parsing and termination by FastEcho.
