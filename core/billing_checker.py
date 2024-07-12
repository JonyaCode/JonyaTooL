import httpx
import asyncio
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from core.config_loader import load_config
from core.proxy_manager import load_proxies, gen_session_proxy
import os
import time

console = Console()

config = load_config()
CHROME_VERSION = config['settings']['chrome_version']
USERAGENT = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{CHROME_VERSION}.0.0.0 Safari/537.36"
BILLING_THREADS = config['settings']['billing_threads']

async def get_billing_info(token, proxy=None):
    headers = {
        'user-agent': USERAGENT,
        'authorization': token
    }
    proxies = {"http://": f"http://{proxy}", "https://": f"http://{proxy}"} if proxy else None

    async with httpx.AsyncClient(headers=headers, proxies=proxies) as client:
        response = await client.get('https://discord.com/api/v9/users/@me/billing/payment-sources')
        if response.status_code == 200:
            return response.json()
        else:
            console.print(f"[red]Error checking billing info: {response.status_code}, message='{response.reason_phrase}', url={response.url}[/red]")
            return None

async def check_card(token, valid_tokens_path, invalid_tokens_path, proxy=None):
    billing_info = await get_billing_info(token, proxy)
    if billing_info:
        for source in billing_info:
            if source['type'] == 1:  # Type 1 indicates a credit/debit card
                last_4 = source['brand'] + ' ' + source['last_4']
                console.print(f"[green]Token {token} has a card: {last_4}[/green]")
                save_card_info(valid_tokens_path, token, last_4)
                return last_4
        console.print(f"[yellow]Token {token} has no card[/yellow]")
        save_invalid_token(invalid_tokens_path, token, "No card found")
        return None
    console.print(f"[red]Billing info not found for token {token}[/red]")
    save_invalid_token(invalid_tokens_path, token, "Billing info not found")
    return None

def check_card_sync(token, valid_tokens_path, invalid_tokens_path, proxy=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(check_card(token, valid_tokens_path, invalid_tokens_path, proxy))

def load_tokens(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def save_card_info(file_path, token, card_info):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{token} | card: {card_info}\n")

def save_invalid_token(file_path, token, reason):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{token} | reason: {reason}\n")

def main_card_check():
    tokens = load_tokens('./data/tokens.txt')
    valid_tokens_path = './data/billing/valid.txt'
    invalid_tokens_path = './data/billing/invalid.txt'
    os.makedirs('./data/billing', exist_ok=True)
    console.print(f"[green]Loaded {len(tokens)} tokens.[/green]")

    config = load_config()
    use_proxies = config['settings']['use_proxies']
    proxy_source = config['settings']['proxy_source']
    proxies = []

    if use_proxies:
        if proxy_source == "file":
            proxies = load_proxies()
            console.print(f"[green]Loaded {len(proxies)} proxies from file.[/green]")
        elif proxy_source == "generate":
            proxies = [gen_session_proxy() for _ in range(len(tokens))]
            console.print(f"[green]Generated {len(proxies)} proxies.[/green]")
        else:
            console.print("[red]Invalid proxy source in configuration.[/red]")
            return

    with ThreadPoolExecutor(max_workers=BILLING_THREADS) as executor:
        futures = []
        for i, token in enumerate(tokens):
            proxy = proxies[i % len(proxies)] if proxies else None
            futures.append(executor.submit(check_card_sync, token, valid_tokens_path, invalid_tokens_path, proxy))
            time.sleep(0.1)  # Задержка между запуском потоков, если необходимо

        for future in futures:
            future.result()  # Блокирует до завершения каждого потока

    console.print(f"[green]Card check completed. Results saved to billing/valid.txt and billing/invalid.txt[/green]")

if __name__ == "__main__":
    main_card_check()
