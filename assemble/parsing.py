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


def parse_macro_def(line: str) -> str:
    regex_match = re.match(r'@macro[ \t]+([a-zA-Z_]\w+)', line)
    if regex_match:
        macro_name = regex_match.group(1)
        return macro_name
    return None


def parse_macro_end(line: str) -> bool:
    regex_match = re.match(r'^\s*@endmacro\s*$', line)
    if regex_match:
        return True
    return False


def parse_macro_invoke(line: str) -> str:
    regex_match = re.match(r'@([a-zA-Z_]\w+)', line)
    if regex_match:
        macro_name = regex_match.group(1)
    else:
        macro_name = None
    
    if macro_name == 'endmacro':
        return None
    return macro_name
