import yaml, os
from rich.console import Console

console = Console()

def load_config(file_path='./config.yaml'):
    if not os.path.exists(file_path):
        console.print(f"[red]Config file {file_path} not found.[/red]")
        raise FileNotFoundError(f"Config file {file_path} not found.")
    
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
