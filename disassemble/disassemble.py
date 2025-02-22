import argparse
import os

from mnemonics import mnemonic_map
from io_funcs import write_output, read_binary


def get_args():
    """Setup command-line arguments."""
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to 6502 machine code file')
    parser.add_argument('--output_file', '-o', help='path to write disassembly output')
    parser.add_argument('--debug', '-d', help='print debugging information', action='store_true')
    return parser.parse_args()


def disass_inst(op_info: tuple, code: bytes, position: int) -> tuple[str, int]:
    """Dissassemble a single 6502 instruction"""
    
    name, mode = op_info
    
    try:
        # Special case for BRK: considered a 2-byte instruction
        if name == 'BRK':
            skip_bytes = 1
            signature = code[position + 1]
            return f'{name} #${signature:02x}', skip_bytes
        
        if mode == 'implied':
            skip_bytes = 0
            return f'{name}', skip_bytes
        
        elif mode == 'immediate':
            skip_bytes = 1
            imm_value = code[position + 1]
            return f'{name} #${imm_value:02x}', skip_bytes
        
        elif mode == 'zero_page':
            skip_bytes = 1
            imm_value = code[position + 1]
            return f'{name} ${imm_value:02x}', skip_bytes
        
        elif mode == 'absolute':
            skip_bytes = 2
            addr_lo = code[position + 1]
            addr_hi = code[position + 2]
            address = (addr_hi << 8) | addr_lo
            return f'{name} ${address:04x}', skip_bytes
        
        elif mode == 'relative':
            skip_bytes = 1
            label_offset = code[position + 1]
            if not (-128 <= label_offset <= 127):
                raise ValueError(
                    f'Branch offset {label_offset} for {name} is too far '
                    f'(cannot fit in signed 8-bit), consider using JMP instead')
            
        raise NotImplementedError(f'Dissassembly of mode {mode} has not been implemented')

    except IndexError as e:
        e.add_note(
            f'While disassembling instruction at 0x{position:04x}: '
            f'Expected at least {skip_bytes} byte(s) after {name} instruction in {mode} mode'
        )
        raise e


def disassemble(machine_code: bytes) -> str:
    disassembly = []
    idx = 0
    while idx < len(machine_code):
        try:
            opcode = machine_code[idx]
            op_info = mnemonic_map[opcode]
            as_asm_str, skipped_bytes = disass_inst(op_info, machine_code, idx)
            disassembly.append(as_asm_str)
            idx += skipped_bytes
            idx += 1
        except KeyError as e:
            e.add_note(f'No such legal opcode {machine_code[idx]}')
            raise e
    
    return '\n'.join(disassembly)


def main():
    args = get_args()
    code = read_binary(args.input_file)
    source = disassemble(code)
    
    if args.output_file:
        write_output(source, args.output_file)
    else:
        print(source)


if __name__ == "__main__":
    main()
