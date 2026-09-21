#!/usr/bin/env python3
"""quicknote - simple cli note-taking tool"""

import argparse
import json
import os
import sys
from datetime import datetime

NOTES_FILE = os.path.expanduser("~/.quicknotes.json")


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r") as f:
        return json.load(f)


def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)


def add_note(text, tags=None):
    notes = load_notes()
    note = {
        "id": len(notes) + 1,
        "text": text,
        "tags": tags or [],
        "done": False,
        "created": datetime.now().strftime("%b %d, %Y"),
    }
    notes.append(note)
    save_notes(notes)
    print(f"  Added note #{note['id']}")


def list_notes(tag_filter=None):
    notes = load_notes()
    if not notes:
        print("  No notes yet. Add one with: quicknote add \"your note\"")
        return

    if tag_filter:
        notes = [n for n in notes if tag_filter in n.get("tags", [])]

    print()
    print(f"  {'#':<4} {'Status':<8} {'Tags':<20} {'Note':<40} {'Created'}")
    print(f"  {'─'*4} {'─'*8} {'─'*20} {'─'*40} {'─'*12}")

    for note in notes:
        status = "[x]" if note["done"] else "[ ]"
        tags = ", ".join(note.get("tags", []))
        text = note["text"][:38] + ".." if len(note["text"]) > 40 else note["text"]
        print(f"  {note['id']:<4} {status:<8} {tags:<20} {text:<40} {note['created']}")
    print()


def search_notes(query):
    notes = load_notes()
    results = [n for n in notes if query.lower() in n["text"].lower()]
    if not results:
        print(f"  No notes matching \"{query}\"")
        return

    print(f"\n  Found {len(results)} note(s):\n")
    for note in results:
        status = "✓" if note["done"] else "○"
        print(f"  {status} #{note['id']} - {note['text']}")
    print()


def delete_note(note_id):
    notes = load_notes()
    notes = [n for n in notes if n["id"] != note_id]
    # reindex
    for i, note in enumerate(notes):
        note["id"] = i + 1
    save_notes(notes)
    print(f"  Deleted note #{note_id}")


def mark_done(note_id):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            note["done"] = True
            save_notes(notes)
            print(f"  Marked note #{note_id} as done ✓")
            return
    print(f"  Note #{note_id} not found")


def main():
    parser = argparse.ArgumentParser(description="quicknote - cli note-taking")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="add a new note")
    add_p.add_argument("text", help="note text")
    add_p.add_argument("--tags", help="comma-separated tags", default="")

    list_p = sub.add_parser("list", help="list all notes")
    list_p.add_argument("--tag", help="filter by tag", default=None)

    search_p = sub.add_parser("search", help="search notes")
    search_p.add_argument("query", help="search query")

    del_p = sub.add_parser("delete", help="delete a note")
    del_p.add_argument("id", type=int, help="note id")

    done_p = sub.add_parser("done", help="mark note as done")
    done_p.add_argument("id", type=int, help="note id")

    args = parser.parse_args()

    if args.command == "add":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        add_note(args.text, tags)
    elif args.command == "list":
        list_notes(args.tag)
    elif args.command == "search":
        search_notes(args.query)
    elif args.command == "delete":
        delete_note(args.id)
    elif args.command == "done":
        mark_done(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
