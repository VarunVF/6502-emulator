opcode_map = {
    'LDA': {'immediate': 0xA9, 'zero_page': 0xA5, 'absolute': 0xAD},
    'STA': {'zero_page': 0x85, 'absolute': 0x8D},
    'ADC': {'immediate': 0x69, 'zero_page': 0x65, 'absolute': 0x6D},
    'BEQ': {'relative': 0xF0},
    'JMP': {'absolute': 0x4C},
    'CLC': {'implied': 0x18},
    'NOP': {'implied': 0xEA},
}
