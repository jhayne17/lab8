from adventure.utils import read_events_from_file
import random

# Optional Rich imports (fallback to plain I/O if Rich isn't installed)
try:
    from rich.console import Console
    from rich.prompt import Prompt
    from rich.panel import Panel
    from rich.rule import Rule
except Exception:  # pragma: no cover
    Console = None
    Prompt = None
    Panel = None
    Rule = None


def step(choice: str, events):
    random_event = random.choice(events)

    if choice == "left":
        return left_path(random_event)
    elif choice == "right":
        return right_path(random_event)
    else:
        return "You stand still, unsure what to do. The forest swallows you."


def left_path(event):
    return "You walk left. " + event


def right_path(event):
    return "You walk right. " + event


def _interactive_loop(events):
    """Interactive runner using Rich if available (keeps tests unchanged)."""
    if Console and Prompt:  # Rich path
        console = Console()
        console.print(Rule("[bold green]🌲 The Adventure Begins[/]"))
        console.print(
            Panel.fit(
                "You wake up in a dark forest. You can go [bold]left[/] or [bold]right[/].",
                border_style="green",
            )
        )
        while True:
            choice = Prompt.ask(
                "[bold]Which direction do you choose?[/] ([green]left[/]/[cyan]right[/]/[red]exit[/])",
                choices=["left", "right", "exit"],
                show_choices=False,
            )
            if choice == "exit":
                console.print("[bold yellow]You choose to leave the forest. Goodbye![/]")
                break
            console.print(step(choice.strip().lower(), events))
    else:  # Fallback: standard I/O
        print("You wake up in a dark forest. You can go left or right.")
        while True:
            choice = input("Which direction do you choose? (left/right/exit): ").strip().lower()
            if choice == "exit":
                break
            print(step(choice, events))


if __name__ == "__main__":
    events = read_events_from_file("events.txt")
    try:
        _interactive_loop(events)
    except KeyboardInterrupt:  # graceful exit on Ctrl+C
        if Console:
            Console().print("\n[bold yellow]Exiting…[/]")
        else:
            print("\nExiting…")
