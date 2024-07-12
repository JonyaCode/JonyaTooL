import os
from rich.console import Console
import time

console = Console()

class FileUtils:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def get_text_files_in_folder(self):
        text_files = [f for f in os.listdir(self.folder_path) if f.endswith('.txt')]
        return text_files
    
    def select_file(self, text_files):
        timestamp = time.strftime("%H:%M:%S")
        console.print(f"[{timestamp}] [blue]Choose file[/]\n[blue]Files available:[/]")
        for i, file_name in enumerate(text_files, 1):
            console.print(f"[blue]{i}.[/] [magenta]{file_name}[/]")

        while True:
            try:
                timestamp = time.strftime("%H:%M:%S")
                console.print(f"[{timestamp}] [magenta]Choose file number: [/]")
                choice = int(input())
                if 1 <= choice <= len(text_files):
                    return text_files[choice - 1]
                else:
                    timestamp = time.strftime("%H:%M:%S")
                    console.print(f"[{timestamp}] [red]Incorrect selection. Please, choose again.[/]")
            except ValueError:
                timestamp = time.strftime("%H:%M:%S")
                console.print(f"[{timestamp}] [red]Input correct number.[/]")

    def process_selected_file(self, selected_file):
        tocheck_file = os.path.join(self.folder_path, f"{selected_file[:-4]}.txt")
        timestamp = time.strftime("%H:%M:%S")
        console.print(f"[{timestamp}] [blue]Chosen file:[/] {selected_file}.\n[blue]Proceeding.[/]")
        return tocheck_file
