#!/usr/bin/env python3

"""
ChromaDB Collection Browser
---------------------------

A nicer terminal browser for viewing ChromaDB collections.

Features:
- Pretty table output
- Pagination
- Metadata display
- Document preview
- Search support
- Collection statistics

Requirements:
    uv pip install chromadb rich

Usage:
    python chroma_browser.py

Optional:
    python chroma_browser.py \
        --db ai_system/data/embeddings/chroma \
        --collection mytinygpt_docs
"""

import argparse
import json
import textwrap

import chromadb

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box


console = Console()


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def truncate(text, width=80):
    if text is None:
        return ""

    text = str(text).replace("\n", " ")

    if len(text) <= width:
        return text

    return text[:width - 3] + "..."


def pretty_metadata(metadata):
    if not metadata:
        return ""

    return json.dumps(metadata, indent=2)


# ---------------------------------------------------------
# Display Functions
# ---------------------------------------------------------

def show_collection_info(collection):
    console.print()

    info = Table(
        title="Collection Information",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan"
    )

    info.add_column("Property", style="bold")
    info.add_column("Value")

    info.add_row("Name", collection.name)
    info.add_row("Documents", str(collection.count()))

    console.print(info)
    console.print()


def show_documents(collection, offset=0, limit=10):
    data = collection.get(
        limit=limit,
        offset=offset,
        include=["documents", "metadatas"]
    )

    ids = data.get("ids", [])
    docs = data.get("documents", [])
    metas = data.get("metadatas", [])

    table = Table(
        title=f"Documents {offset} - {offset + len(ids)}",
        box=box.MINIMAL_DOUBLE_HEAD,
        show_lines=True
    )

    table.add_column("#", style="bold cyan", width=6)
    table.add_column("ID", style="green", width=20)
    table.add_column("Document", width=80)
    table.add_column("Metadata", width=40)

    for idx, doc_id in enumerate(ids):
        doc = truncate(docs[idx], 80)

        meta = truncate(
            pretty_metadata(metas[idx]),
            40
        )

        table.add_row(
            str(offset + idx),
            truncate(doc_id, 20),
            doc,
            meta
        )

    console.print(table)


def show_document_detail(collection, doc_index):
    data = collection.get(
        include=["documents", "metadatas"]
    )

    ids = data.get("ids", [])
    docs = data.get("documents", [])
    metas = data.get("metadatas", [])

    if doc_index >= len(ids):
        console.print("[red]Invalid index[/red]")
        return

    panel_text = f"""
[bold cyan]ID:[/bold cyan]
{ids[doc_index]}

[bold cyan]Document:[/bold cyan]
{textwrap.fill(docs[doc_index], width=100)}

[bold cyan]Metadata:[/bold cyan]
{pretty_metadata(metas[doc_index])}
"""

    console.print(
        Panel(
            panel_text,
            title=f"Document #{doc_index}",
            expand=False
        )
    )


def search_collection(collection, query):
    console.print(f"\n[bold yellow]Searching:[/bold yellow] {query}\n")

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    docs = results.get("documents", [[]])[0]
    ids = results.get("ids", [[]])[0]
    distances = results.get("distances", [[]])[0]

    table = Table(
        title="Search Results",
        box=box.ROUNDED
    )

    table.add_column("Rank", width=6)
    table.add_column("Distance", width=12)
    table.add_column("ID", width=24)
    table.add_column("Document", width=90)

    for i in range(len(ids)):
        table.add_row(
            str(i + 1),
            f"{distances[i]:.4f}",
            truncate(ids[i], 24),
            truncate(docs[i], 90)
        )

    console.print(table)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--db",
        default="ai_system/data/embeddings/chroma",
        help="Path to ChromaDB"
    )

    parser.add_argument(
        "--collection",
        default="mytinygpt_docs",
        help="Collection name"
    )

    args = parser.parse_args()

    console.print("\n[bold green]Connecting to ChromaDB...[/bold green]\n")

    client = chromadb.PersistentClient(path=args.db)

    collections = [c.name for c in client.list_collections()]

    if args.collection not in collections:
        console.print("[red]Collection not found[/red]")
        console.print(f"Available: {collections}")
        return

    collection = client.get_collection(args.collection)

    show_collection_info(collection)

    offset = 0
    page_size = 10

    while True:
        show_documents(collection, offset, page_size)

        console.print("\nCommands:")
        console.print("[cyan]n[/cyan] = next page")
        console.print("[cyan]p[/cyan] = previous page")
        console.print("[cyan]v <index>[/cyan] = view document")
        console.print("[cyan]s[/cyan] = semantic search")
        console.print("[cyan]q[/cyan] = quit")

        cmd = Prompt.ask("\nEnter command").strip()

        if cmd == "q":
            break

        elif cmd == "n":
            offset += page_size

        elif cmd == "p":
            offset = max(0, offset - page_size)

        elif cmd.startswith("v "):
            try:
                idx = int(cmd.split()[1])
                show_document_detail(collection, idx)
                Prompt.ask("\nPress Enter to return to list")
            except:
                console.print("[red]Invalid index[/red]")

        elif cmd == "s":
            query = Prompt.ask("Search query")
            search_collection(collection, query)

        console.print()


if __name__ == "__main__":
    main()