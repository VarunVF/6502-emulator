import argparse

from io_funcs import write_binary, print_hex
from io_funcs import debug_line, debug_op, debug_mode, debug_code, debug_skip_reason
from opcodes import opcode_map
from parsing import read_lines, parse_line
from parsing import parse_macro_def, parse_macro_end, parse_macro_invoke


def get_args():
    """Setup command-line arguments."""
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to assembly source')
    parser.add_argument('--output_file', '-o', help='path to write binary output', default='out.bin')
    parser.add_argument('--print-bytes', '-p', help='print out the resulting machine code bytes', action='store_true')
    parser.add_argument('--debug', '-d', help='print debugging information', action='store_true')
    return parser.parse_args()


def prefixed_to_decimal(arg: str) -> int:
    if len(arg) == 0:
        raise ValueError('Empty numeric literal')
    
    if arg.startswith('%') and len(arg) > 1:
        return int(arg[1:], 2)  # binary
    elif arg.startswith('$') and len(arg) > 1:
        return int(arg[1:], 16)  # hexadecimal
    elif arg.isdigit():
        return int(arg, 10)  # decimal
    else:
        raise ValueError(f'Unknown prefix for operand: {arg[0]}')


def lo_hi_split(number: int) -> tuple[int, int]:
    """Split a 16-bit number into its low and high bytes."""
    
    if number.bit_length() > 16:
        raise ValueError(f'Number does not fit in 16 bits: {number}')
    
    lo = number & 0x00ff
    hi = number >> 8
    return lo, hi


def to_machine_code(mnemonic: str, operand: str):
    mnemonic = mnemonic.upper()
    
    if mnemonic not in opcode_map:
        raise ValueError(f'Unknown opcode: {mnemonic}')
    
    def ensure_addressing_mode(op, mode: str):
        if mode not in op.keys():
            raise KeyError(f'Instruction {mnemonic} does not support {mode} mode. '
                           f'Supported modes are {list(op.keys())}')
    
    op = opcode_map[mnemonic]
    
    # Special case for BRK: considered a 2-byte instruction
    if mnemonic == 'BRK':
        if not operand:
            print('Warning: BRK not accompanied by signature byte. Inserting 0x00 as operand')
            mode = 'implied'
            signature = 0x00
        else:
            mode = 'immediate'
            signature = prefixed_to_decimal(operand[1:])
        ensure_addressing_mode(op, mode)
        return [op[mode], signature], mode
    
    if not operand:
        mode = 'implied'
        ensure_addressing_mode(op, mode)
        return [op[mode]], mode
    
    elif operand.startswith('#'):
        mode = 'immediate'
        value = prefixed_to_decimal(operand[1:])
        ensure_addressing_mode(op, mode)
        return [op[mode], value], mode

    elif operand.startswith('$') and len(operand) == 3:
        # Zero Page mode, operand in hex
        mode = 'zero_page'
        value = prefixed_to_decimal(operand)
        ensure_addressing_mode(op, mode)
        return [op[mode], value], mode

    elif operand.startswith('$') and len(operand) == 5:
        # Absolute mode, operand in hex
        mode = 'absolute'
        value = prefixed_to_decimal(operand)
        # Address in low-byte, high-byte order (LLHH)
        lo_byte, hi_byte = lo_hi_split(value)
        ensure_addressing_mode(op, mode)
        return [op[mode], lo_byte, hi_byte], mode
    
    elif operand.startswith('$'):
        raise ValueError(f'Invalid address: {operand}')
    
    else:
        raise ValueError(f'Unknown operand format: {operand}')


def assemble(input_file: str, output_file: str, do_debug: bool = False):
    machine_code_decimal = []
    
    lines = read_lines(input_file)
    for idx, line in enumerate(lines):
        inst, operand = parse_line(line)
        if do_debug:
            debug_line(idx + 1, line)
            debug_op(inst, operand)

        codes = []
        
        if inst is not None:
            codes, mode = to_machine_code(inst, operand)
            if do_debug:
                debug_mode(mode)
                debug_code(codes)
            machine_code_decimal.extend(codes)
        else:
            # Didn't find an instruction
            reason = 'unknown'
            if line == '':
                reason = 'empty'
            elif line.startswith(';'):
                reason = 'comment'
            else:
                padding = len(repr(idx + 1)) + 2
                raise SyntaxError(
                    f'Invalid syntax:\n'
                    + f'{idx + 1}| {line}\n'
                    + ' '*padding + '^'*len(line)
                )
            if do_debug:
                debug_skip_reason(line, reason)
    
        if do_debug:
            print()
    
    machine_code = bytes(machine_code_decimal)
    write_binary(output_file, machine_code)
    return machine_code


def preprocess(input_file: str, processed_file: str, do_debug: bool = False):
    macros = dict()
    
    lines = read_lines(input_file)
    for i in range(len(lines)):
        lines[i] = lines[i].split(';')[0]
        lines[i] = lines[i].strip()
    
    idx = 0
    while idx < len(lines):
        macro_name = parse_macro_def(lines[idx])
        if macro_name is not None:
            lines[idx] = ''  # Remove macro def
            idx += 1  # Advance past the @macro line
            macros[macro_name] = []
            if do_debug:
                print(f'Macro definition: {macro_name}')
            while idx < len(lines) and not parse_macro_end(lines[idx]):
                macros[macro_name].append(lines[idx])
                if do_debug:
                    print(f'Add to macro {macro_name}: {lines[idx]}')
                lines[idx] = ''  # Remove macro body
                idx += 1
                continue
            if parse_macro_end(lines[idx]):
                lines[idx] = ''  # Remove macro end
                if do_debug:
                    print(f'End of macro.')
        
        invoked_macro = parse_macro_invoke(lines[idx])
        if invoked_macro is not None:
            lines[idx] = '\n'.join(macros[invoked_macro])
        
        idx += 1

    processed = '\n'.join(lines)
    with open(processed_file, 'w') as f:
        f.write(processed)


def main():
    args = get_args()
    
    if args.debug:
        print(f'Assembling from {args.input_file} and writing to {args.output_file}')
        print()
        print('Preprocessing...')

    preprocessed_file = f'p_{args.input_file}'
    preprocess(args.input_file, preprocessed_file, args.debug)
    
    if args.debug:
        print()
        print('Assembling...')
    
    code = assemble(preprocessed_file, args.output_file, args.debug)
    
    if args.print_bytes:
        print('Full machine code:')
        print_hex(code)


if __name__ == '__main__':
    main()
