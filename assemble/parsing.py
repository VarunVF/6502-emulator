import re

from io_funcs import read_source


def read_lines(input_file: str) -> list[str]:
    source = read_source(input_file)
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
