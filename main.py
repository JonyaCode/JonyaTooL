import nest_asyncio
nest_asyncio.apply()

from InquirerPy import prompt
from core.token_manager import check_tokens_async, load_and_prepare, sort_tokens_by_date_action
from core.spammer import main_spam
from core.billing_checker import main_card_check
from rich.console import Console
import asyncio

console = Console()

def main_menu():
    questions = [
        {
            "type": "list",
            "message": "Choose an action:",
            "choices": ["Check Tokens", "Sort Tokens by Date", "Spam Messages for open dms and channels", "Check Cards", "Exit"],
            "name": "action",
        }
    ]
    return prompt(questions)["action"]

def main():
    while True:
        action = main_menu()
        
        if action == "Check Tokens":
            tokens, proxies, valid_tokens_path, invalid_tokens_path, num_threads, max_threads_per_second = load_and_prepare()
            if tokens and proxies is not None:
                try:
                    asyncio.run(check_tokens_async(tokens, proxies, valid_tokens_path, invalid_tokens_path, max_threads_per_second))
                    console.print("[green]Tokens checked and results saved.[/green]")
                except Exception as e:
                    console.print(f"[red]Error checking tokens: {e}[/red]")

        elif action == "Sort Tokens by Date":
            sort_tokens_by_date_action()

        elif action == "Spam Messages for open dms and channels":
            try:
                asyncio.run(main_spam())
                console.print("[green]Messages sent.[/green]")
            except Exception as e:
                console.print(f"[red]Error spamming messages: {e}[/red]")

        elif action == "Check Cards":
            try:
                main_card_check()
                console.print("[green]Card check completed.[/green]")
            except Exception as e:
                console.print(f"[red]Error checking cards: {e}[/red]")

        elif action == "Exit":
            console.print("[yellow]Exiting the program.[/yellow]")
            break

if __name__ == "__main__":
    main()
