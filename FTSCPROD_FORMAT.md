# FTSCPROD.FE Binary Format Specification

This document describes the binary file format of the FastEcho FTSCPROD database [`FTSCPROD.FE`](FTSCPROD.FE:1) used by FastEcho for product code lookup.

## File Structure

The FastEcho FTSCPROD database [`FTSCPROD.FE`](FTSCPROD.FE:1) consists of:
1. **File Header** (2 bytes):
   - Unsigned 16-bit integer (little-endian) representing the total size of the records payload (total file size minus 2 bytes).
2. **Product Records** (variable length sequence):
   - Each record is laid out contiguously without padding between records.
3. **End of File / End of Data Marker** (4 bytes):
   - A final 4-byte zero marker (`0x00000000`) terminating the records payload.

## Record Format

Each individual product record contains:
- **Size Byte** (`1 byte`): Total length of the record in bytes. It covers itself (1 byte), the product code (2 bytes), the product name string length ($N$ bytes), and the null terminator (1 byte), resulting in `len(product_name) + 4`. Since the size is stored in a single byte, product names longer than 251 characters must be truncated to ensure the total record size does not exceed 255 bytes.
- **Product Code** (`2 bytes`): Unsigned 16-bit integer (little-endian) representing the FTSC product code (e.g., `0x00FE`, `0x0100`).
- **Product Name** (`N bytes`): ASCII/Latin1 string representing the product name.
- **Null Terminator** (`1 byte`): `0x00` terminating the string at the end of the record.
