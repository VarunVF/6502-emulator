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


def debug_line(line_number, line):
    print(f'Current line:\t{line_number}| {line}')


def debug_op(instruction, operand):
    print(f'Found operation \'{instruction}\', operand \'{operand}\'')


def debug_mode(mode):
    print(f'Using {mode} addressing mode')


def debug_code(line_codes):
    print('Converted to machine code: ', end='')
    print_hex(bytes(line_codes))


def debug_skip_reason(line, reason):
    print(f'Skipping line (Reason: {reason})')
