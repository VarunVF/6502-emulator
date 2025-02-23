opcode_map = {
    # Access (Load and Store)
    'LDA': {'immediate': 0xA9, 'zero_page': 0xA5, 'zero_page_x': 0xB5, 'absolute': 0xAD, 
            'absolute_x': 0xBD, 'absolute_y': 0xB9, 'indexed_indirect': 0xA1, 'indirect_indexed': 0xB1},
    'STA': {'zero_page': 0x85, 'zero_page_x': 0x95, 'absolute': 0x8D, 'absolute_x': 0x9D, 
            'absolute_y': 0x99, 'indexed_indirect': 0x81, 'indirect_indexed': 0x91},
    'LDX': {'immediate': 0xA2, 'zero_page': 0xA6, 'zero_page_y': 0xB6, 'absolute': 0xAE, 'absolute_y': 0xBE},
    'STX': {'zero_page': 0x86, 'zero_page_y': 0x96, 'absolute': 0x8E},
    'LDY': {'immediate': 0xA0, 'zero_page': 0xA4, 'zero_page_x': 0xB4, 'absolute': 0xAC, 'absolute_x': 0xBC},
    'STY': {'zero_page': 0x84, 'zero_page_x': 0x94, 'absolute': 0x8C},
    
    # Transfer
    'TAX': {'implied': 0xAA},
    'TXA': {'implied': 0x8A},
    'TAY': {'implied': 0xA8},
    'TYA': {'implied': 0x98},

    # Arithmetic
    'ADC': {'immediate': 0x69, 'zero_page': 0x65, 'zero_page_x': 0x75, 'absolute': 0x6D, 
            'absolute_x': 0x7D, 'absolute_y': 0x79, 'indexed_indirect': 0x61, 'indirect_indexed': 0x71},
    'SBC': {'immediate': 0xE9, 'zero_page': 0xE5, 'zero_page_x': 0xF5, 'absolute': 0xED, 
            'absolute_x': 0xFD, 'absolute_y': 0xF9, 'indexed_indirect': 0xE1, 'indirect_indexed': 0xF1},
    'INC': {'zero_page': 0xE6, 'zero_page_x': 0xF6, 'absolute': 0xEE, 'absolute_x': 0xFE},
    'DEC': {'zero_page': 0xC6, 'zero_page_x': 0xD6, 'absolute': 0xCE, 'absolute_x': 0xDE},
    'INX': {'implied': 0xE8},
    'DEX': {'implied': 0xCA},
    'INY': {'implied': 0xC8},
    'DEY': {'implied': 0x88},

    # Shifts
    'ASL': {'accumulator': 0x0A, 'zero_page': 0x06, 'zero_page_x': 0x16, 'absolute': 0x0E, 'absolute_x': 0x1E},
    'LSR': {'accumulator': 0x4A, 'zero_page': 0x46, 'zero_page_x': 0x56, 'absolute': 0x4E, 'absolute_x': 0x5E},
    'ROL': {'accumulator': 0x2A, 'zero_page': 0x26, 'zero_page_x': 0x36, 'absolute': 0x2E, 'absolute_x': 0x3E},
    'ROR': {'accumulator': 0x6A, 'zero_page': 0x66, 'zero_page_x': 0x76, 'absolute': 0x6E, 'absolute_x': 0x7E},
    
    # Bitwise
    'AND': {'immediate': 0x29, 'zero_page': 0x25, 'zero_page_x': 0x35, 'absolute': 0x2D, 
            'absolute_x': 0x3D, 'absolute_y': 0x39, 'indexed_indirect': 0x21, 'indirect_indexed': 0x31},
    'ORA': {'immediate': 0x09, 'zero_page': 0x05, 'zero_page_x': 0x15, 'absolute': 0x0D, 
            'absolute_x': 0x1D, 'absolute_y': 0x19, 'indexed_indirect': 0x01, 'indirect_indexed': 0x11},
    'EOR': {'immediate': 0x49, 'zero_page': 0x45, 'zero_page_x': 0x55, 'absolute': 0x4D, 
            'absolute_x': 0x5D, 'absolute_y': 0x59, 'indexed_indirect': 0x41, 'indirect_indexed': 0x51},
    'BIT': {'zero_page': 0x24, 'absolute': 0x2C},  # BIT - Test Bits in Memory

    # Comparisons
    'CMP': {'immediate': 0xC9, 'zero_page': 0xC5, 'zero_page_x': 0xD5, 'absolute': 0xCD, 
            'absolute_x': 0xDD, 'absolute_y': 0xD9, 'indexed_indirect': 0xC1, 'indirect_indexed': 0xD1},
    'CPX': {'immediate': 0xE0, 'zero_page': 0xE4, 'absolute': 0xEC},
    'CPY': {'immediate': 0xC0, 'zero_page': 0xC4, 'absolute': 0xCC},

    # Branches
    'BCC': {'relative': 0x90},
    'BCS': {'relative': 0xB0},
    'BEQ': {'relative': 0xF0},
    'BMI': {'relative': 0x30},
    'BNE': {'relative': 0xD0},
    'BPL': {'relative': 0x10},
    'BVC': {'relative': 0x50},
    'BVS': {'relative': 0x70},

    # Jumps and Calls
    'JMP': {'absolute': 0x4C, 'indirect': 0x6C},
    'JSR': {'absolute': 0x20},
    'RTS': {'implied': 0x60},
    'BRK': {'implied': 0x00, 'immediate': 0x00},  # Allow both 'BRK' and 'BRK #...'
    'RTI': {'implied': 0x40},

    # Stack Operations
    'PHA': {'implied': 0x48},
    'PLA': {'implied': 0x68},
    'PHP': {'implied': 0x08},
    'PLP': {'implied': 0x28},
    'TXS': {'implied': 0x9A},
    'TSX': {'implied': 0xBA},
    
    # Flags
    'CLC': {'implied': 0x18},
    'SEC': {'implied': 0x38},
    'CLI': {'implied': 0x58},
    'SEI': {'implied': 0x78},
    'CLD': {'implied': 0xD8},
    'SED': {'implied': 0xF8},
    'CLV': {'implied': 0xB8},

    # Other
    'NOP': {'implied': 0xEA},
}
