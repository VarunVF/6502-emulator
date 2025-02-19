def read_source(filepath: str) -> str:
    with open(filepath, 'r') as f:
        doc = f.read()
    return doc


def write_binary(filepath: str, contents: bytes):
    with open(filepath, 'wb') as f:
        f.write(contents)


def print_hex(hex_codes: bytes):
    """Human-friendly hex format"""
    
    hex_str = hex_codes.hex().upper()
    for idx in range(0, len(hex_str), 2):
        print(hex_str[idx:idx + 2], end=' ')
    print()


def print_debug_info(line_idx, line, instruction, operand, mode, line_codes):
    line_number = line_idx + 1
    
    print(f'Current line:\t{line_number}| {line}')
    print(f'Found operation \'{instruction}\', operand \'{operand}\'')
    
    if instruction is not None:
        print(f'Using {mode} addressing mode')
        print('Converted to machine code: ', end='')
        print_hex(bytes(line_codes))
    else:
        reason = 'empty' if line == '' else 'comment'
        print(f'Skipping (line is {reason})')
    
    print()
