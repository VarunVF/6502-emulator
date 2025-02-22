def write_output(filepath: str, output: str):
    with open(filepath, 'w') as f:
        f.write(output)


def read_binary(filepath: str) -> bytes:
    with open(filepath, 'rb') as f:
        code = f.read()
    return code
