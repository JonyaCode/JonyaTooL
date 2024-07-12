import os
import base64
from datetime import datetime
from rich.console import Console

console = Console()

def load_tokens_from_file(file_path):
    with open(file_path, 'r') as file:
        tokens = [line.strip() for line in file if line.strip()]
    return tokens

def get_creation_date(token):
    try:
        if ":" in token:
            token = token.split(":")[-1]
        userid = base64.b64decode(token.split(".")[0] + "==").decode("utf-8")
        creationdate_unix = int(bin(int(userid))[:-22], 2) + 1420070400000
        creation_date = datetime.fromtimestamp(creationdate_unix / 1000).isoformat()
        return creation_date
    except Exception as e:
        console.print(f"[red]Error decoding token creation date: {e}[/red]")
        return None

def sort_tokens_by_date(tokens):
    tokens_with_dates = [(token, get_creation_date(token)) for token in tokens]
    tokens_with_dates = [t for t in tokens_with_dates if t[1] is not None]
    sorted_tokens = sorted(tokens_with_dates, key=lambda x: x[1])
    return [t[0] for t in sorted_tokens]

def save_sorted_tokens(file_path, tokens):
    with open(file_path, 'w') as file:
        for token in tokens:
            file.write(f"{token}\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        console.print("[red]Usage: python date_sorter.py <file_path>[/red]")
        sys.exit(1)
    file_path = sys.argv[1]
    tokens = load_tokens_from_file(file_path)
    sorted_tokens = sort_tokens_by_date(tokens)
    save_sorted_tokens(file_path, sorted_tokens)
    console.print(f"[green]Tokens sorted by date and saved to {file_path}[/green]")
