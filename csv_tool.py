import argparse
import json
from rich.console import Console
from rich.table import Table
from core import load_csv, apply_filters, compute_all_stats

console = Console()

def main():
    parser = argparse.ArgumentParser(description="CSV Tool with Full Stats")
    parser.add_argument("csv_file")
    parser.add_argument("--filter", nargs="*", default=[])
    parser.add_argument("--output", default="result.json")

    args = parser.parse_args()

    console.print("[bold green]Loading CSV...[/bold green]")
    df = load_csv(args.csv_file)

    if args.filter:
        console.print("[yellow]Applying filters...[/yellow]")
        df = apply_filters(df, args.filter)

    console.print("[blue]Computing statistics...[/blue]")
    results = compute_all_stats(df)

    # Save JSON
    with open(args.output, "w") as f:
        json.dump(results, f, indent=4)

    # Pretty output
    table = Table(title="Full Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    for k, v in results.items():
        table.add_row(k, str(v))

    console.print(table)
    console.print(f"[bold green]Saved to {args.output}[/bold green]")

if __name__ == "__main__":
    main()