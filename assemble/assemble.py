import argparse
import re


def get_args():
    """Setup command-line arguments."""
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='path to assembly source')
    parser.add_argument('--output_file', '-o', help='path to write binary output', default='out.bin')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    


if __name__ == "__main__":
    main()
