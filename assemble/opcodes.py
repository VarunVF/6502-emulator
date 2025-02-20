opcode_map = {
    # Access
    'LDA': {'immediate': 0xA9, 'zero_page': 0xA5, 'absolute': 0xAD},
    'STA': {'zero_page': 0x85, 'absolute': 0x8D},
    'LDX': {'immediate': 0xA2, 'zero_page': 0xA6, 'absolute': 0xAE},
    'STX': {'zero_page': 0x86, 'absolute': 0x8E},
    'LDY': {'immediate': 0xA0, 'zero_page': 0xA4, 'absolute': 0xAC},
    'STY': {'zero_page': 0x84, 'absolute': 0x8C},
    
    # Transfer
    'TAX': {'implied': 0xAA},  # Transfer A to X
    'TXA': {'implied': 0x8A},  # Transfer X to A
    'TAY': {'implied': 0xA8},  # Transfer A to Y
    'TYA': {'implied': 0x98},  # Transfer Y to A
    
    # Arithmetic
    'ADC': {'immediate': 0x69, 'zero_page': 0x65, 'absolute': 0x6D},  # Add with carry
    'SBC': {'immediate': 0xE9, 'zero_page': 0xE5, 'absolute': 0xED},  # Subtract with carry
    'INC': {'zero_page': 0xE6, 'absolute': 0xEE},
    'DEC': {'zero_page': 0xC6, 'absolute': 0xCE},
    'INX': {'implied': 0xE8},
    'DEX': {'implied': 0xCA},
    'INY': {'implied': 0xC8},
    'DEY': {'implied': 0x88},
    
    # Shift
    'ASL': {'zero_page': 0x06, 'absolute': 0x0E},  # Arithmetic Shift Left
    'LSR': {'zero_page': 0x46, 'absolute': 0x4E},  # Logical Shift Right
    'ROL': {'zero_page': 0x26, 'absolute': 0x2E},  # Rotate Left
    'ROR': {'zero_page': 0x66, 'absolute': 0x6E},  # Rotate Right
    
    # Bitwise
    'AND': {'immediate': 0x29, 'zero_page': 0x25, 'absolute': 0x2D},  # Bitwise AND with A
    'ORA': {'immediate': 0x09, 'zero_page': 0x05, 'absolute': 0x0D},  # Bitwise OR with A
    'EOR': {'immediate': 0x49, 'zero_page': 0x45, 'absolute': 0x4D},  # Bitwise XOR with A
    'BIT': {'zero_page': 0x24, 'absolute': 0x2C},
    
    # Compare
    'CMP': {'immediate': 0xC9, 'zero_page': 0xC5, 'absolute': 0xCD},  # Compare A
    'CPX': {'immediate': 0xE0, 'zero_page': 0xE4, 'absolute': 0xEC},  # Compare X
    'CPY': {'immediate': 0xC0, 'zero_page': 0xC4, 'absolute': 0xCC},  # Compare Y
    
    # Branch
    'BCC': {'relative': 0x90},  # Branch if Carry Clear
    'BCS': {'relative': 0xB0},  # Branch if Carry Set
    'BEQ': {'relative': 0xF0},  # Branch if Equal (when zero flag set)
    'BNE': {'relative': 0xD0},  # Branch if Not Equal (when zero flag clear)
    'BPL': {'relative': 0x10},  # Branch if Plus (when negative flag clear)
    'BMI': {'relative': 0x30},  # Branch if Minus (when negative flag set)
    'BVC': {'relative': 0x50},  # Branch if Overflow Clear
    'BVS': {'relative': 0x70},  # Branch if Overflow Set
    
    # Jump
    'JMP': {'absolute': 0x4C},
    'JSR': {'absolute': 0x20},  # Jump to Subroutine
    'RTS': {'implied': 0x60},  # Return from Subroutine
    'BRK': {'implied': 0x00, 'immediate': 0x00},  # Break (software IRQ)
    'RTI': {'implied': 0x40},  # Return from Interrupt
    
    # Stack
    'PHA': {'implied': 0x48},  # Push A
    'PLA': {'implied': 0x68},  # Pull A
    'PHP': {'implied': 0x08},  # Push Processor Status (flags)
    'PLP': {'implied': 0x28},  # Pull Processor Status (flags)
    'TXS': {'implied': 0x9A},  # Transfer X to Stack Pointer
    'TSX': {'implied': 0xBA},  # Transfer Stack Pointer to X
    
    # Flags
    'CLC': {'implied': 0x18},  # Clear Carry
    'SEC': {'implied': 0x38},  # Set Carry
    'CLI': {'implied': 0x58},  # Clear Interrupt disable
    'SEI': {'implied': 0x78},  # Set Interrupt disable
    'CLD': {'implied': 0xD8},  # Clear Decimal
    'SED': {'implied': 0xF8},  # Set Decimal
    'CLV': {'implied': 0xB8},  # Clear overflow
    
    # Other
    'NOP': {'implied': 0xEA},  # No Operation
}
