#!/usr/bin/env python3
import json
import sys

def check_notebook(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code':
            if cell['outputs']:
                print(f"Error: Cell {i+1} in {filename} has output. Please clear all outputs before committing.")
                return False
    return True

if __name__ == '__main__':
    all_clear = True
    for filename in sys.argv[1:]:
        if not check_notebook(filename):
            all_clear = False
    if not all_clear:
        sys.exit(1)
