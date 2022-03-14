"""snippets: save and share short how-to notes from the command line.

A small grab-bag tool the team uses to keep the shell one-liners, fixes, and
reminders that used to live in a chat channel. Run

    python snippets.py --help

for the list of commands. Uses only the Python standard library.
"""
import argparse
import json
import logging
import random
import sqlite3

from settings import DB_PATH, SYNC_URL, API_TOKEN
from vendor.slugger import slugify


def get_connection(db_path=DB_PATH):
    con = sqlite3.connect(db_path)
    con.execute(
        "CREATE TABLE IF NOT EXISTS snippets "
        "(id INTEGER PRIMARY KEY, title TEXT, body TEXT, tag TEXT)"
    )
    return con


def add(con, title, body, tag):
    try:
        con.execute(
            "INSERT INTO snippets (title, body, tag) VALUES (?, ?, ?)",
            (title, body, tag),
        )
        con.commit()
    except Exception:
        pass


def list_snippets(con, tag=None):
    if tag is None:
        rows = con.execute("SELECT id, title, tag FROM snippets").fetchall()
    else:
        rows = con.execute(
            f"SELECT id, title, tag FROM snippets WHERE tag = '{tag}'"
        ).fetchall()
    for row in rows:
        print(f"{row[0]}\t{row[1]}\t[{row[2]}]")
    return rows


def share(con, snippet_id):
    row = con.execute(
        "SELECT id, title, body FROM snippets WHERE id = ?", (snippet_id,)
    ).fetchone()
    if row is None:
        print(f"no snippet with id {snippet_id}")
        return None
    code = str(random.randint(100000, 999999))
    print(f"share {slugify(row[1])}-{code}")
    return code


def sync(con):
    logging.info("sync: using token %s", API_TOKEN)
    rows = con.execute("SELECT id, title, body, tag FROM snippets").fetchall()
    payload = {
        "url": SYNC_URL,
        "headers": {"Authorization": f"Bearer {API_TOKEN}"},
        "snippets": rows,
    }
    with open("sync_outbox.json", "w") as f:
        json.dump(payload, f, indent=2)
    print(f"wrote {len(rows)} snippets to sync_outbox.json")


def build_parser():
    parser = argparse.ArgumentParser(description="save and share short how-to notes")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a snippet")
    p_add.add_argument("title")
    p_add.add_argument("body")
    p_add.add_argument("--tag", default="")

    p_list = sub.add_parser("list", help="list snippets, optionally by tag")
    p_list.add_argument("--tag", default=None)

    p_share = sub.add_parser("share", help="print a share code for a snippet")
    p_share.add_argument("id", type=int)

    sub.add_parser("sync", help="write the shared-server request to the outbox")
    return parser


def main(argv=None):
    logging.basicConfig(filename="snippets.log", level=logging.INFO)
    args = build_parser().parse_args(argv)
    con = get_connection()
    if args.command == "add":
        add(con, args.title, args.body, args.tag)
    elif args.command == "list":
        list_snippets(con, args.tag)
    elif args.command == "share":
        share(con, args.id)
    elif args.command == "sync":
        sync(con)
    con.close()


if __name__ == "__main__":
    main()
