import os

from assemble.opcodes import opcode_map


def gen_mnemonic_map():
    mnemonic_map = {}
    for mnemonic, mode_map in opcode_map.items():
        for mode, opcode in mode_map.items():
            opcode_info = (mnemonic, mode)
            mnemonic_map.update({opcode: opcode_info})
    return mnemonic_map


def gen_mnemonics_file(map):
    filepath = os.path.join('disassemble', 'mnemonics.py')
    
    modes = set()
    for op_name, op_mode in map.values():
        modes.add(op_mode)
    
    with open(filepath, 'w') as f:
        f.write('mnemonic_map = {\n')
        for opcode, opcode_info in map.items():
            f.write(f'    0x{f'{opcode:02x}'}: {opcode_info},\n')
        f.write('}\n')
        f.write('\n')
        
        f.write('modes = [')
        for mode in modes:
            f.write(f'{mode!r}, ')
        f.write(']\n')


def main():
    map = gen_mnemonic_map()
    gen_mnemonics_file(map)


if __name__ == "__main__":
    main()
