HEADER_SIZE = 2
EOF_MARKER = b"\x00\x00\x00\x00"

MAX_RECORD_SIZE = 255
RECORD_HEADER_SIZE = 4
MIN_RECORD_BYTES = 4

CODE_BYTE_SIZE = 2
CODE_OFFSET_START = 1
CODE_OFFSET_END = 3

MIN_ROW_ELEMENTS = 2

# Exclude non-product placeholder codes:
# 0x00FE: No_product_id_allocated
# 0x00FF: 16-bit_product_id
# 0x0100: Reserved
# 0x0104: None
EXCLUDE_CODES = {0x00FE, 0x00FF, 0x0100, 0x0104}
