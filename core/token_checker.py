import httpx
import asyncio
import base64
from datetime import datetime
from rich.console import Console
from core.config_loader import load_config

console = Console()

config = load_config()
CHROME_VERSION = config['settings']['chrome_version']
USERAGENT = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{CHROME_VERSION}.0.0.0 Safari/537.36"
DELAY_BETWEEN_TASKS = config['settings']['delay_between_tasks']

async def get_user_info(token, proxy=None):
    headers = {
        'user-agent': USERAGENT,
        'authorization': token
    }
    try:
        proxies = {"http://": f"http://{proxy}", "https://": f"http://{proxy}"} if proxy else None
        async with httpx.AsyncClient(headers=headers, proxies=proxies) as client:
            response = await client.get('https://discord.com/api/v9/users/@me')
            if response.status_code == 200:
                return response.json()
            else:
                console.print(f"[red]Error checking token: {response.status_code}, message='{response.reason_phrase}', url={response.url}[/red]")
    except httpx.HTTPStatusError as exc:
        console.print(f"[red]HTTP error occurred: {exc.response.status_code} - {exc.response.text}[/red]")
    except Exception as e:
        console.print(f"[red]Error checking token: {e}[/red]")
    return None

async def get_guilds(token, proxy=None):
    headers = {
        'user-agent': USERAGENT,
        'authorization': token
    }
    try:
        proxies = {"http://": f"http://{proxy}", "https://": f"http://{proxy}"} if proxy else None
        async with httpx.AsyncClient(headers=headers, proxies=proxies) as client:
            response = await client.get('https://discord.com/api/v9/users/@me/guilds')
            if response.status_code == 200:
                return response.json()
            else:
                console.print(f"[red]Error checking token: {response.status_code}, message='{response.reason_phrase}', url={response.url}[/red]")
    except httpx.HTTPStatusError as exc:
        console.print(f"[red]HTTP error occurred: {exc.response.status_code} - {exc.response.text}[/red]")
    except Exception as e:
        console.print(f"[red]Error checking token: {e}[/red]")
    return None

async def get_relationships(token, proxy=None):
    headers = {
        'user-agent': USERAGENT,
        'authorization': token
    }
    try:
        proxies = {"http://": f"http://{proxy}", "https://": f"http://{proxy}"} if proxy else None
        async with httpx.AsyncClient(headers=headers, proxies=proxies) as client:
            response = await client.get('https://discord.com/api/v9/users/@me/relationships')
            if response.status_code == 200:
                return response.json()
            else:
                console.print(f"[red]Error checking token: {response.status_code}, message='{response.reason_phrase}', url={response.url}[/red]")
    except httpx.HTTPStatusError as exc:
        console.print(f"[red]HTTP error occurred: {exc.response.status_code} - {exc.response.text}[/red]")
    except Exception as e:
        console.print(f"[red]Error checking token: {e}[/red]")
    return None

async def get_open_dms(token, proxy=None):
    headers = {
        'user-agent': USERAGENT,
        'authorization': token
    }
    try:
        proxies = {"http://": f"http://{proxy}", "https://": f"http://{proxy}"} if proxy else None
        async with httpx.AsyncClient(headers=headers, proxies=proxies) as client:
            response = await client.get('https://discord.com/api/v9/users/@me/channels')
            if response.status_code == 200:
                return response.json()
            else:
                console.print(f"[red]Error getting DMs: {response.status_code}, message='{response.reason_phrase}', url={response.url}[/red]")
                return []
    except httpx.HTTPStatusError as exc:
        console.print(f"[red]HTTP error occurred: {exc.response.status_code} - {exc.response.text}[/red]")
    except Exception as e:
        console.print(f"[red]Error getting DMs: {e}[/red]")
    return []

async def check_token(token, proxy=None):
    user_info = await get_user_info(token, proxy)
    if user_info:
        guilds = await get_guilds(token, proxy)
        relationships = await get_relationships(token, proxy)
        direct_messages = await get_open_dms(token, proxy)
        
        verification_status = "Unverified"
        if user_info.get("verified"):
            verification_status = "Mail"
            if user_info.get("phone"):
                verification_status = "Mail+Phone"
        elif user_info.get("phone"):
            verification_status = "Phone"

        return {
            'token': token,
            'valid': True,
            'verification': verification_status,
            'guilds_count': len(guilds) if guilds else 0,
            'friends_count': len(relationships) if relationships else 0,
            'direct_messages_count': len(direct_messages) if direct_messages else 0,
            'created_at': get_creation_date(token)
        }
    return {'token': token, 'valid': False}

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

async def check_tokens(tokens, proxies=None):
    tasks = []
    for i, token in enumerate(tokens):
        proxy = proxies[i % len(proxies)] if proxies else None
        tasks.append(check_token(token, proxy))
        await asyncio.sleep(DELAY_BETWEEN_TASKS)
    return await asyncio.gather(*tasks)
