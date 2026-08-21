# FTSC Product Database Tools

Utilities for working with the FastEcho [`FTSCPROD.FE`](FTSCPROD.FE:1) binary product code database.

## Overview

This repository provides Python scripts to generate and inspect the FastEcho product code binary database file [`FTSCPROD.FE`](FTSCPROD.FE:1).

## Scripts

### 1. Dump Database (`dump_ftscprod.py`)
Inspects and dumps contents of the binary [`FTSCPROD.FE`](FTSCPROD.FE:1) file.
```bash
python3 dump_ftscprod.py [filepath]
```
- **Arguments**: Optional path to the binary [`FTSCPROD.FE`](FTSCPROD.FE:1) file (defaults to `FTSCPROD.FE`).

### 2. Generate Database (`generate_ftscprod.py`)
Generates the binary [`FTSCPROD.FE`](FTSCPROD.FE:1) file from a text-based product code list.
```bash
python3 generate_ftscprod.py text_source [fe_target]
```
- **Arguments**:
  - `text_source`: Path to the input product codes text file.
  - `fe_target`: Path to the output binary file (defaults to `FTSCPROD.FE`).

## Implementation Notes

- Non-product placeholder codes (such as `0x00FE`, `0x00FF`, `0x0100`, and `0x0104`) are automatically excluded during database generation.
- Detailed specification of the binary layout can be found in [`FTSCPROD_FORMAT.md`](FTSCPROD_FORMAT.md:1).
