import os
from rich.console import Console

console = Console()

def extract_token(line):
    parts = line.split(':')
    if len(parts) == 1:
        return parts[0]
    elif len(parts) == 3:
        return parts[2]
    else:
        console.print(f"[yellow]Invalid token format: {line}[/yellow]")
        return None

def load_tokens(file_path='./data/tokens.txt'):
    if not os.path.exists(file_path):
        console.print(f"[red]File {file_path} not found.[/red]")
        raise FileNotFoundError(f"File {file_path} not found.")
    
    tokens = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                token = extract_token(line)
                if token:
                    tokens.append(token)
    
    console.print(f"[green]Loaded {len(tokens)} tokens from {file_path}.[/green]")
    return tokens
