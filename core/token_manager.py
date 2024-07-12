import asyncio
import os
from rich.console import Console
from core.token_loader import load_tokens
from core.proxy_manager import load_proxies, gen_session_proxy
from core.config_loader import load_config
from core.token_checker import check_tokens
from core.date_sorter import load_tokens_from_file, sort_tokens_by_date, save_sorted_tokens as save_sorted_date_tokens
from core.file_utils import FileUtils

console = Console()

async def worker(token, proxy, valid_tokens_path, invalid_tokens_path, semaphore):
    async with semaphore:
        checked_token = (await check_tokens([token], [proxy] if proxy else None))[0]
        if checked_token['valid']:
            verification = checked_token['verification']
            guilds_count = checked_token['guilds_count']
            friends_count = checked_token['friends_count']
            dms_count = checked_token['direct_messages_count']
            created_at = checked_token['created_at']
            console.print(f"[green]Valid: {checked_token['token']} | V: {verification} | G: {guilds_count} | F: {friends_count} | DMs: {dms_count} | Cr: {created_at}[/green]")
            with open(valid_tokens_path, 'a') as file:
                file.write(f"{checked_token['token']} | Verification: {verification} | Guilds: {guilds_count} | Friends: {friends_count} | Direct Messages: {dms_count} | Created At: {created_at}\n")
        else:
            console.print(f"[red]Token invalid: {token}[/red]")
            with open(invalid_tokens_path, 'a') as file:
                file.write(f"{token}\n")

async def check_tokens_async(tokens, proxies, valid_tokens_path, invalid_tokens_path, max_threads_per_second):
    semaphore = asyncio.Semaphore(max_threads_per_second)
    tasks = []
    for i, token in enumerate(tokens):
        proxy = proxies[i % len(proxies)] if proxies else None
        tasks.append(worker(token, proxy, valid_tokens_path, invalid_tokens_path, semaphore))
    await asyncio.gather(*tasks)

def load_and_prepare():
    config = load_config()
    use_proxies = config['settings']['use_proxies']
    proxy_source = config['settings']['proxy_source']
    num_threads = config['settings']['num_threads']
    max_threads_per_second = 25

    console.print(f"[green]Using proxies: {use_proxies}[/green]")
    console.print(f"[green]Proxy source: {proxy_source}[/green]")
    console.print(f"[green]Number of threads: {num_threads}[/green]")

    valid_tokens_path = './data/checker/valid.txt'
    invalid_tokens_path = './data/checker/invalid.txt'
    os.makedirs(os.path.dirname(valid_tokens_path), exist_ok=True)
    os.makedirs(os.path.dirname(invalid_tokens_path), exist_ok=True)

    try:
        tokens = load_tokens()
        console.print(f"[green]Loaded {len(tokens)} tokens.[/green]")
    except Exception as e:
        console.print(f"[red]Error loading tokens: {e}[/red]")
        return None, None, None, None, None, None

    if use_proxies:
        if proxy_source == "file":
            try:
                proxies = load_proxies()
                console.print(f"[green]Loaded {len(proxies)} proxies from file.[/green]")
            except Exception as e:
                console.print(f"[red]Error loading proxies: {e}[/red]")
                return None, None, None, None, None, None
        elif proxy_source == "generate":
            proxies = [gen_session_proxy() for _ in range(len(tokens))]
            console.print(f"[green]Generated {len(proxies)} session proxies.[/green]")
        else:
            console.print("[red]Invalid proxy source in configuration.[/red]")
            return None, None, None, None, None, None
    else:
        proxies = None
        console.print("[yellow]Proxies are disabled in the configuration.[/yellow]")

    return tokens, proxies, valid_tokens_path, invalid_tokens_path, num_threads, max_threads_per_second

def sort_tokens_by_date_action():
    try:
        file_utils = FileUtils('./data')
        text_files = file_utils.get_text_files_in_folder()
        selected_file = file_utils.select_file(text_files)
        file_path = file_utils.process_selected_file(selected_file)
        
        tokens = load_tokens_from_file(file_path)
        sorted_tokens = sort_tokens_by_date(tokens)
        save_sorted_date_tokens(file_path, sorted_tokens)
        
        console.print(f"[green]Tokens sorted by date and saved to {file_path}[/green]")
    except Exception as e:
        console.print(f"[red]Error sorting tokens: {e}[/red]")
