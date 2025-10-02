import argparse
from notecli import storage, search

def main():
    parser = argparse.ArgumentParser(description="Simple Note CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_cmd = subparsers.add_parser("add")
    add_cmd.add_argument("text", help="Note content")

    list_cmd = subparsers.add_parser("list")

    read_cmd = subparsers.add_parser("read")
    read_cmd.add_argument("filename")

    search_cmd = subparsers.add_parser("search")
    search_cmd.add_argument("keyword")

    args = parser.parse_args()

    if args.command == "add":
        filename = storage.save_note(args.text)
        print(f"Note saved: {filename}")
    elif args.command == "list":
        for f in storage.list_notes():
            print(f)
    elif args.command == "read":
        content = storage.read_note(args.filename)
        if content:
            print(content)
        else:
            print("Note not found")
    elif args.command == "search":
        results = search.search_notes(args.keyword)
        for file, snippet in results:
            print(f"{file}: {snippet}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
