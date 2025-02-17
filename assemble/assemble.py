import argparse
import re

from bin_file_io import read_binary, write_binary
from opcodes import opcode_map


def get_args():
    """Setup command-line arguments."""
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to assembly source')
    parser.add_argument('--output_file', '-o', help='path to write binary output', default='out.bin')
    parser.add_argument('--print-bytes', '-p', help='print out the resulting machine code bytes', action='store_true')
    parser.add_argument('--debug', '-d', help='print debugging information', action='store_true')
    args = parser.parse_args()
    return args


def read_lines(input_file: str) -> list[str]:
    source = read_binary(input_file)
    return source.splitlines()


def parse_line(line: str) -> tuple[str, str]:
    line = line.split(';')[0]  # Remove comment
    line = line.strip()  # Remove whitespace
    
    # Match mnemonics and operand
    regex_match = re.match(r'([a-zA-Z]+)[ \t]+(\S+)', line)
    if regex_match:
        mnemonic = regex_match.group(1)
        operand = regex_match.group(2)
        return mnemonic, operand
    
    # Otherwise, match mnemonic without operand
    regex_match = re.match(r'([a-zA-Z]+)', line)
    if regex_match:
        mnemonic = regex_match.group(1)
        return mnemonic, None
    
    return None, None


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
        raise NotImplementedError(f'Absolute mode is not yet implemented.')
    else:
        raise ValueError(f'Unknown operand format: {operand}')


def assemble(input_file: str, output_file: str, do_debug: bool = False):
    machine_code_decimal = []
    
    lines = read_lines(input_file)
    for line in lines:
        if do_debug:
            print('Current line:\t', line)
        
        inst, operand = parse_line(line)
        if do_debug:
            print(f'Found operation \'{inst}\', operand \'{operand}\'')
        if inst is None or operand is None:
            continue
        
        codes = to_machine_code(inst, operand, do_debug)
        machine_code_decimal.extend(codes)
    
    machine_code = bytes(machine_code_decimal)
    write_binary(output_file, machine_code)
    return machine_code

    
def main():
    args = get_args()
    if (args.debug):
        print(f'Assembling from {args.input_file} and writing to {args.output_file}')
    
    code = assemble(args.input_file, args.output_file, args.debug)
    
    if args.print_bytes:
        print(code)


if __name__ == '__main__':
    main()
