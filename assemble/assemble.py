import argparse
import re

from bin_file_io import read_binary, write_binary


def get_args():
    """Setup command-line arguments."""
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to assembly source')
    parser.add_argument('--output_file', '-o', help='path to write binary output', default='out.bin')
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


def main():
    args = get_args()
    lines = read_lines(args.input_file)
    inst, operand = parse_line(lines[2])
    print((inst, operand))


if __name__ == '__main__':
    main()
