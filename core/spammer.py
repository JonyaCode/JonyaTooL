import httpx
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from datetime import datetime
import threading
from rich.console import Console
from core.config_loader import load_config
from core.proxy_manager import load_proxies, gen_session_proxy
import time

console = Console()

config = load_config()
CHROME_VERSION = config['settings']['chrome_version']
USERAGENT = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{CHROME_VERSION}.0.0.0 Safari/537.36"
DELAY_BETWEEN_TASKS = config['settings']['delay_between_tasks']
SPAM_THREADS = config['settings']['spam_threads']

async def get_open_dms(token, proxy):
    headers = {
        'user-agent': USERAGENT,
        'authorization': token
    }
    proxies = {"http://": f"http://{proxy}", "https://": f"http://{proxy}"} if proxy else None

    async with httpx.AsyncClient(headers=headers, proxies=proxies) as client:
        response = await client.get('https://discord.com/api/v9/users/@me/channels')
        if response.status_code == 200:
            return response.json()
        return []

async def get_guild_channels(token, proxy):
    headers = {
        'user-agent': USERAGENT,
        'authorization': token
    }
    proxies = {"http://": f"http://{proxy}", "https://": f"http://{proxy}"} if proxy else None

    async with httpx.AsyncClient(headers=headers, proxies=proxies) as client:
        response = await client.get('https://discord.com/api/v9/users/@me/guilds')
        if response.status_code == 200:
            guilds = response.json()
            channels = []
            for guild in guilds:
                guild_id = guild['id']
                guild_channels_response = await client.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels')
                if guild_channels_response.status_code == 200:
                    channels.extend(guild_channels_response.json())
            return channels
        return []

async def send_message(token, channel_id, message, proxy, thread_id):
    headers = {
        'user-agent': USERAGENT,
        'authorization': token,
        'content-type': 'application/json'
    }
    proxies = {"http://": f"http://{proxy}", "https://": f"http://{proxy}"} if proxy else None
    json_data = {'content': message}

    async with httpx.AsyncClient(headers=headers, proxies=proxies) as client:
        response = await client.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', json=json_data)
        if response.status_code == 200:
            timestamp = time.strftime("%H:%M:%S")
            console.print(f"[green][{timestamp}][Thread {thread_id}] {token} | sent message to user {channel_id}[/]")
            return True
        return False

async def spam_messages(token, message, proxy, thread_id):
    open_dms = await get_open_dms(token, proxy)
    guild_channels = await get_guild_channels(token, proxy)

    sent_count = 0
    for dm in open_dms:
        if await send_message(token, dm['id'], message, proxy, thread_id):
            sent_count += 1

    for channel in guild_channels:
        if channel['type'] == 0:  # Text channel type
            if await send_message(token, channel['id'], message, proxy, thread_id):
                sent_count += 1

    return sent_count

def load_message(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def load_tokens(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def save_used_token(file_path, token, sent_count):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{token} | sent: {sent_count}\n")

def process_token(token, message, proxy, used_tokens_path, thread_id):
    sent_count = asyncio.run(spam_messages(token, message, proxy, thread_id))  # Pass thread_id here
    save_used_token(used_tokens_path, token, sent_count)
    timestamp = time.strftime("%H:%M:%S")
    console.print(f"[green][{timestamp}][Thread {thread_id}] {token} | sent: {sent_count} messages[/]")


async def main_spam():
    tokens = load_tokens('./spamer/tokens.txt')
    message = load_message('./spamer/message.txt')
    used_tokens_path = './spamer/used_tokens.txt'
    config = load_config()
    use_proxies = config['settings']['use_proxies']
    proxy_source = config['settings']['proxy_source']
    proxies = []

    if use_proxies:
        if proxy_source == "file":
            proxies = load_proxies()
        elif proxy_source == "generate":
            proxies = [gen_session_proxy() for _ in range(len(tokens))]
        else:
            console.print("[red]Invalid proxy source in configuration.[/red]")
            return

    with ThreadPoolExecutor(max_workers=SPAM_THREADS) as executor:
        loop = asyncio.get_event_loop()
        tasks = []
        for i, token in enumerate(tokens):
            proxy = proxies[i % len(proxies)] if proxies else None
            tasks.append(loop.run_in_executor(executor, process_token, token, message, proxy, used_tokens_path, i + 1))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main_spam())
