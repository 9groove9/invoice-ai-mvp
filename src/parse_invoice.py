import pandas as pd

from pathlib import Path

def load_invoice(filename):
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = BASE_DIR / 'data' / 'invoices' / filename
    try:
        df = pd.read_excel(path)
        return df
    except Exception as e:
        print(f'Unable to load file: {filename}')
        print(f'Expected path: {path}')
        print(f'Make sure the file exists in /data/invoices/')
        return None