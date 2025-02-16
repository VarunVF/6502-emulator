def read_binary(filepath: str) -> str:
    with open(filepath, 'r') as f:
        doc = f.read()
    return doc


def write_binary(filepath: str, contents: bytes):
    with open(filepath, 'wb') as f:
        f.write(contents)
