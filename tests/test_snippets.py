import io
import sqlite3
import unittest
from contextlib import redirect_stdout

import snippets


class SnippetsTestCase(unittest.TestCase):
    def setUp(self):
        self.con = sqlite3.connect(":memory:")
        self.con.execute(
            "CREATE TABLE snippets "
            "(id INTEGER PRIMARY KEY, title TEXT, body TEXT, tag TEXT)"
        )

    def tearDown(self):
        self.con.close()

    def test_add_inserts_a_row(self):
        snippets.add(self.con, "reboot a stuck server", "sudo systemctl reboot", "it")
        rows = self.con.execute("SELECT title, body, tag FROM snippets").fetchall()
        self.assertEqual(rows, [("reboot a stuck server", "sudo systemctl reboot", "it")])

    def test_add_commits_so_rows_persist(self):
        snippets.add(self.con, "one", "body", "ops")
        count = self.con.execute("SELECT COUNT(*) FROM snippets").fetchone()[0]
        self.assertEqual(count, 1)

    def test_list_returns_every_row(self):
        snippets.add(self.con, "one", "b1", "it")
        snippets.add(self.con, "two", "b2", "ops")
        with redirect_stdout(io.StringIO()):
            rows = snippets.list_snippets(self.con)
        self.assertEqual(len(rows), 2)

    def test_list_by_tag_returns_matching_rows(self):
        snippets.add(self.con, "one", "b1", "it")
        snippets.add(self.con, "two", "b2", "ops")
        with redirect_stdout(io.StringIO()):
            rows = snippets.list_snippets(self.con, tag="it")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "one")

    def test_share_returns_a_code_for_a_real_snippet(self):
        snippets.add(self.con, "reboot a stuck server", "sudo systemctl reboot", "it")
        row_id = self.con.execute("SELECT id FROM snippets").fetchone()[0]
        with redirect_stdout(io.StringIO()):
            code = snippets.share(self.con, row_id)
        self.assertIsNotNone(code)
        self.assertEqual(len(code), 6)

    def test_share_returns_none_for_a_missing_snippet(self):
        with redirect_stdout(io.StringIO()):
            code = snippets.share(self.con, 999)
        self.assertIsNone(code)


if __name__ == "__main__":
    unittest.main()
