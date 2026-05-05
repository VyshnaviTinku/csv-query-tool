import argparse
import pandas as pd
import json
import sys
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

def load_csv(file_path):
    try:
        console.print(f"[bold green]Loading CSV:[/bold green] {file_path}")
        return pd.read_csv(file_path)
    except Exception as e:
        console.print(f"[bold red]Error loading CSV:[/bold red] {e}")
        sys.exit(1)

def apply_filters(df, filters):
    for f in track(filters, description="Applying filters..."):
        col, val = f.split("=")
        df = df[df[col].astype(str) == val]
    return df

def apply_aggregation(df, agg):
    col, func = agg.split(":")
    if func not in ["sum", "mean", "count", "max", "min"]:
        raise ValueError(f"Unsupported aggregation: {func}")
    return {f"{col}_{func}": getattr(df[col], func)()}

def main():
    parser = argparse.ArgumentParser(description="CSV Query Tool with Rich UI")
    parser.add_argument("csv_file", help="Path to CSV file")
    parser.add_argument("--filter", nargs="*", default=[], help="Filters like col=value")
    parser.add_argument("--agg", nargs="*", default=[], help="Aggregations like col:sum")
    parser.add_argument("--output", default="result.json", help="Output JSON file")
    
    args = parser.parse_args()
    
    df = load_csv(args.csv_file)
    df = apply_filters(df, args.filter)
    
    results = {}
    for agg in track(args.agg, description="Applying aggregations..."):
        results.update(apply_aggregation(df, agg))
    
    with open(args.output, "w") as f:
        json.dump(results, f, indent=4)
    
    # Pretty print results
    table = Table(title="Summary Results")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")
    for k, v in results.items():
        table.add_row(k, str(v))
    console.print(table)
    
    console.print(f"[bold green]Results saved to {args.output}[/bold green]")

if __name__ == "__main__":
    main()
