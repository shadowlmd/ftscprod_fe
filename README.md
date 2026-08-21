# FTSC Product Database Tools

Utilities for working with the FastEcho FTSCPROD database [`FTSCPROD.FE`](FTSCPROD.FE:3).

## Overview

This repository provides Python scripts to generate and inspect the FastEcho FTSCPROD database file [`FTSCPROD.FE`](FTSCPROD.FE:3).

## Source Data

The FTSC Product Codes source text database can be obtained from [FTSC Documentation](http://ftsc.org/docs/) (under **Miscellaneous Administrative Files**, document name: **FTSC Product Codes**).

## Scripts

### 1. Dump Database (`dump_ftscprod.py`)
Inspects and dumps contents of the FastEcho FTSCPROD database [`FTSCPROD.FE`](FTSCPROD.FE:3).
```bash
dump_ftscprod.py [fastecho_db_path]
```
- **Arguments**: Optional path to the FastEcho FTSCPROD database file (defaults to `FTSCPROD.FE`).

### 2. Generate Database (`generate_ftscprod.py`)
Generates the FastEcho FTSCPROD database [`FTSCPROD.FE`](FTSCPROD.FE:3) from the FTSC Product Codes file.
```bash
generate_ftscprod.py product_codes_path [fastecho_db_path]
```
- **Arguments**:
  - `product_codes_path`: Path to the input FTSC Product Codes file.
  - `fastecho_db_path`: Path to the output FastEcho FTSCPROD database file (defaults to `FTSCPROD.FE`).

## Implementation Notes

- Non-product placeholder codes (such as `0x00FE`, `0x00FF`, `0x0100`, and `0x0104`) are automatically excluded during database generation.
- Detailed specification of the binary layout can be found in [`FTSCPROD_FORMAT.md`](FTSCPROD_FORMAT.md:1).
