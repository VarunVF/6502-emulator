import argparse

from bin_file_io import write_binary
from opcodes import opcode_map
from parsing import read_lines, parse_line


def get_args():
    """Setup command-line arguments."""
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to assembly source')
    parser.add_argument('--output_file', '-o', help='path to write binary output', default='out.bin')
    parser.add_argument('--print-bytes', '-p', help='print out the resulting machine code bytes', action='store_true')
    parser.add_argument('--debug', '-d', help='print debugging information', action='store_true')
    return parser.parse_args()


def prefixed_to_decimal(arg: str):
    if arg.startswith('%'):
        return int(arg[1:], 2)  # binary
    elif arg.startswith('$'):
        return int(arg[1:], 16)  # hexadecimal
    elif arg.isdigit():
        return int(arg, 10)  # decimal
    else:
        raise ValueError(f'Unknown prefix for operand: {arg[0]}')
    

def to_machine_code(mnemonic: str, operand: str, do_debug: bool = False):
    mnemonic = mnemonic.upper()
    
    if mnemonic not in opcode_map:
        raise ValueError(f'Unknown opcode: {mnemonic}')
    
    def ensure_addressing_mode(op, mode: str):
        if mode not in op.keys():
            raise KeyError(f'Opcode {operand} does not support {mode} mode')
    
    def debug_addr_mode(mode: str, do_debug: bool):
        if do_debug:
            print(f'Using {mode} addressing mode')
    
    op = opcode_map[mnemonic]
    
    if not operand:
        mode = 'implied'
        debug_addr_mode(mode, do_debug)
        ensure_addressing_mode(op, mode)
        return [op[mode]]
    
    if operand.startswith('#'):
        mode = 'immediate'
        debug_addr_mode(mode, do_debug)
        value = prefixed_to_decimal(operand[1:])
        ensure_addressing_mode(op, mode)
        return [op[mode], value]

    elif operand.startswith('$') and len(operand) == 3:
        mode = 'zero_page'
        debug_addr_mode(mode, do_debug)
        value = prefixed_to_decimal(operand)
        ensure_addressing_mode(op, mode)
        return [op[mode], value]

    elif operand.startswith('$'):
        # Absolute mode, operand in hex
        mode = 'absolute'
        debug_addr_mode(mode, do_debug)
        value = prefixed_to_decimal(operand)
        ensure_addressing_mode(op, mode)
        return [op[mode], value]
    else:
        raise ValueError(f'Unknown operand format: {operand}')


def assemble(input_file: str, output_file: str, do_debug: bool = False):
    if do_debug:
        print(f'Assembling from {input_file} and writing to {output_file}')
        print()

    machine_code_decimal = []
    
    lines = read_lines(input_file)
    for idx, line in enumerate(lines):
        inst, operand = parse_line(line)
        
        if do_debug:
            print(f'Current line:\t{idx + 1}| {line}')
            print(f'Found operation \'{inst}\', operand \'{operand}\'')
        
        # No instruction found: full line was a comment
        if inst is None:
            print()
            continue
        
        codes = to_machine_code(inst, operand, do_debug)
        if do_debug:
            print(f'Converted to machine code: {bytes(codes)}')
            print()
        
        machine_code_decimal.extend(codes)
    
    machine_code = bytes(machine_code_decimal)
    write_binary(output_file, machine_code)
    return machine_code

    
def main():
    args = get_args()
    code = assemble(args.input_file, args.output_file, args.debug)
    
    if args.print_bytes:
        print('Full machine code:')
        print(code)


if __name__ == '__main__':
    main()
