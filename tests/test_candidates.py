import tempfile
import unittest
from pathlib import Path

from wordie.candidates import filter_candidates, load_words

WORDS_PATH = Path(__file__).resolve().parent.parent / "data" / "words.txt"


class LoadWordsTests(unittest.TestCase):
    def test_reads_one_word_per_line_and_skips_blanks(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "words.txt"
            path.write_text("Abide\n\ncrane\n", encoding="utf-8")
            self.assertEqual(load_words(path), ["abide", "crane"])

    def test_shipped_list_holds_only_five_letter_lowercase_words(self):
        words = load_words(WORDS_PATH)
        self.assertTrue(words)
        for word in words:
            self.assertEqual(len(word), 5)
            self.assertTrue(word.isalpha() and word.islower())


class FilterCandidatesTests(unittest.TestCase):
    WORDS = ["abide", "crane", "elate", "slate"]

    def test_keeps_only_words_that_would_give_the_pattern(self):
        self.assertEqual(filter_candidates(self.WORDS, "crane", "BBYBG"), ["abide"])

    def test_all_green_keeps_only_the_answer(self):
        self.assertEqual(filter_candidates(self.WORDS, "slate", "GGGGG"), ["slate"])


if __name__ == "__main__":
    unittest.main()
